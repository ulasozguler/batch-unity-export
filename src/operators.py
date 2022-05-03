import bpy
from .settings import UnityBatchExportSettings
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
        human_type = "collection" if settings.per_collection else "object"
        try:
            abs_path = bpy.path.abspath(settings.export_path)

            if settings.per_collection:
                root_coll = bpy.context.scene.collection
                file_count = len(root_coll.children)
                export_collections(
                    settings.collection or root_coll, abs_path, settings.object_types
                )
            else:
                object_list = (
                    bpy.context.selected_objects
                    if settings.selected_only
                    else (
                        settings.collection.all_objects
                        if settings.collection
                        else bpy.context.scene.objects
                    )
                )
                file_count = len(object_list)
                export_objects(object_list, abs_path, settings.object_types)

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
