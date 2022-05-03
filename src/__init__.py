bl_info = {
    "name": "Batch Unity Export",
    "author": "Ulas Ozguler",
    "description": "Export objects or collections separately for Unity.",
    "blender": (3, 1, 0),
    "version": (0, 0, 1),
    "location": "View3D",
    "category": "Exporter",
}

import bpy
from .panel import UnityBatchExportPanel
from .settings import UnityBatchExportSettings
from .operators import BatchUnityExportOp
from bpy.props import PointerProperty
from bpy.app.handlers import persistent


load_classes, unload_classes = bpy.utils.register_classes_factory(
    [
        UnityBatchExportSettings,
        BatchUnityExportOp,
        UnityBatchExportPanel,
    ]
)


def show_message(title, message, icon):
    def draw_func(self, _):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw_func, title=title, icon=icon)


@persistent
def on_save_hook(_):
    if bpy.context.scene.unity_batch_export_settings.auto_export:
        bpy.ops.unity_batch_export.export("EXEC_DEFAULT")
    pass


def register():
    load_classes()
    bpy.types.Scene.unity_batch_export_settings = PointerProperty(
        type=UnityBatchExportSettings
    )
    if on_save_hook not in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.append(on_save_hook)


def unregister():
    del bpy.types.Scene.unity_batch_export_settings
    unload_classes()
    if on_save_hook in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(on_save_hook)
