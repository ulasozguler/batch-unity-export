import bpy
from bpy.props import BoolProperty, StringProperty, PointerProperty, EnumProperty
from bpy.types import PropertyGroup, Collection


class EXPORTMODE:
    SELECTED = "SELECTED"
    OBJECT = "OBJECT"
    COLLECTION = "COLLECTION"
    SINGLE = "SINGLE"


class UnityBatchExportSettings(PropertyGroup):
    export_path: StringProperty(
        name="Path",
        default="",
        description="Directory to export",
        subtype="DIR_PATH",
    )
    export_mode: EnumProperty(
        name="Mode",
        items=(
            (EXPORTMODE.SELECTED, "Selected Object", ""),
            (EXPORTMODE.OBJECT, "Object", ""),
            (EXPORTMODE.COLLECTION, "Collection", ""),
            (EXPORTMODE.SINGLE, "Active Scene", ""),
        ),
        description="Create an FBX file for every",
        default="OBJECT",
    )
    collection: PointerProperty(
        name="Parent",
        type=Collection,
        description="Export from this collection only",
        poll=lambda _, coll: bpy.context.scene.user_of_id(coll),
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
        default={"MESH", "OTHER"},
    )
