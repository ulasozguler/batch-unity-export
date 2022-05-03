from bpy.types import Panel


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

        # collection
        collection_field = layout.row()
        collection_field.prop(settings, "collection")
        if settings.selected_only and not settings.per_collection:
            collection_field.enabled = False

        # per collection
        layout.prop(settings, "per_collection")

        # selected only
        selected_only_field = layout.row()
        selected_only_field.prop(settings, "selected_only")
        if settings.per_collection:
            selected_only_field.enabled = False

        # auto export
        layout.prop(settings, "auto_export")

        # object types
        layout.use_property_split = True
        layout.column().prop(settings, "object_types")
        layout.use_property_split = False

        # export button
        layout.operator("unity_batch_export.export", text="Export", icon="EXPORT")
