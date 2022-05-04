import bpy
from .settings import UnityBatchExportSettings, EXPORTMODE
from .core import *


class BatchUnityExportOp(bpy.types.Operator):
    bl_idname = "unity_batch_export.export"
    bl_label = "Batch Unity Export"

    def execute(self, context):
        settings: UnityBatchExportSettings = context.scene.unity_batch_export_settings

        if not settings.export_path:
            self.report({"ERROR"}, "Path not set")
            return {"FINISHED"}

        self.report({"INFO"}, "Exporting...")
        try:
            abs_path = bpy.path.abspath(settings.export_path)

            common = {"folder": abs_path, "object_types": settings.object_types}

            if settings.export_mode == EXPORTMODE.SELECTED:
                file_count = len(bpy.context.selected_objects)
                human_type = "selected object"
                export_objects(bpy.context.selected_objects, **common)

            elif settings.export_mode == EXPORTMODE.OBJECT:
                object_list = (
                    settings.collection.all_objects
                    if settings.collection
                    else bpy.context.scene.objects
                )
                file_count = len(object_list)
                human_type = "object"
                export_objects(object_list, **common)

            elif settings.export_mode == EXPORTMODE.COLLECTION:
                coll = settings.collection or bpy.context.scene.collection
                file_count = len(coll.children)
                human_type = "collection"
                export_collections(coll, **common)

            elif settings.export_mode == EXPORTMODE.SINGLE:
                file_count = 1
                human_type = "scene"
                export_scene(bpy.context.scene, **common)

            else:
                self.report({"ERROR"}, "Unknown export mode: %s" % settings.export_mode)

        except Exception as ex:
            self.report({"ERROR"}, "Error occured during export: %s" % ex)
        else:
            if file_count == 0:
                self.report({"WARNING"}, "No %s(s) are exported." % human_type)
            else:
                self.report(
                    {"INFO"}, "%s %s(s) are exported." % (file_count, human_type)
                )

        return {"FINISHED"}
