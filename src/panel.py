from bpy.types import Panel
from src.settings import EXPORTMODE


class UnityBatchExportPanel(Panel):
    bl_idname = "BATCH_UNITY_EXPORT_PT_main"
    bl_label = "Batch Unity Export"
    bl_category = "Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.unity_batch_export_settings

        # export path
        layout.prop(settings, "export_path")

        layout.prop(settings, "export_mode")

        # collection
        if settings.export_mode in [EXPORTMODE.OBJECT, EXPORTMODE.COLLECTION]:
            collection_field = layout.row()
            collection_field.prop(settings, "collection")

        # auto export
        layout.prop(settings, "auto_export")

        # object types
        layout.use_property_split = True
        layout.column().prop(settings, "object_types")
        layout.use_property_split = False

        # export button
        layout.operator("unity_batch_export.export", text="Export", icon="EXPORT")
