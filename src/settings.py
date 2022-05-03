from bpy.props import BoolProperty, StringProperty, PointerProperty, EnumProperty
from bpy.types import PropertyGroup, Collection


class UnityBatchExportSettings(PropertyGroup):
    export_path: StringProperty(
        name="Path",
        default="",
        description="Directory to export",
        subtype="DIR_PATH",
    )
    collection: PointerProperty(
        name="Collection",
        type=Collection,
        description='Export from this collection only. Ignored when "Selected Objects" is enabled',
    )
    per_collection: BoolProperty(
        name="Per Collection",
        default=False,
        description="Create a separate file for every non-empty collection",
    )
    selected_only: BoolProperty(
        name="Selected Objects",
        default=False,
        description='Export selected objects only. Ignored when "Per Collection" is enabled',
    )
    auto_export: BoolProperty(
        name="Auto Export",
        default=True,
        description="Automatically export when project is saved",
    )
    object_types: EnumProperty(
        name="Object Types",
        options={"ENUM_FLAG"},
        items=(
            ("EMPTY", "Empty", ""),
            ("CAMERA", "Camera", ""),
            ("LIGHT", "Lamp", ""),
            ("ARMATURE", "Armature", "WARNING: not supported in dupli/group instances"),
            ("MESH", "Mesh", ""),
            (
                "OTHER",
                "Other",
                "Other geometry types, like curve, metaball, etc. (converted to meshes)",
            ),
        ),
        description="Which kind of object to export",
        default={"MESH"},
    )
