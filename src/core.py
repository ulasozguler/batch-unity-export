import os
import bpy


def preserve_selection(func):
    def inner(*args, **kwargs):
        orig_selected_objs = bpy.context.selected_objects
        try:
            return func(*args, **kwargs)
        finally:
            bpy.ops.object.select_all(action="DESELECT")
            for o in orig_selected_objs:
                o.select_set(True)

    return inner


@preserve_selection
def export_objects(objects, folder, object_types):
    for an_obj in objects:
        bpy.ops.object.select_all(action="DESELECT")
        print("exporting: %s" % an_obj)

        # create a duplicate of object and add to root
        obj = an_obj.copy()
        obj.data = an_obj.data.copy()
        bpy.context.scene.collection.objects.link(obj)

        # deselect original object
        an_obj.select_set(False)

        # unhide and select new object
        obj.hide_set(False)
        obj.select_set(True)

        # apply scale and move to origin
        obj.location = (0, 0, 0)
        bpy.ops.object.transform_apply()

        # export and delete
        fbx(folder, an_obj.name, object_types)
        bpy.ops.object.delete()


@preserve_selection
def export_collections(parent_collection, folder, object_types):

    for coll in parent_collection.children:
        if len(coll.all_objects) == 0:  # skip empty collections
            continue

        print("exporting: %s" % coll)

        # select all objects in this collection
        bpy.ops.object.select_all(action="DESELECT")
        for obj in coll.all_objects:
            obj.select_set(True)

        # export
        fbx(folder, coll.name, object_types)


def export_scene(scene, folder, object_types):
    fbx(folder, scene.name, object_types, use_selection=False)


def fbx(path, name, object_types, use_selection=True):
    obj_path = os.path.join(path, name + ".fbx")
    bpy.ops.export_scene.fbx(
        filepath=obj_path,
        use_selection=use_selection,
        use_space_transform=True,
        apply_unit_scale=True,
        global_scale=1,
        apply_scale_options="FBX_SCALE_NONE",
        axis_forward="-Z",
        axis_up="Y",
        bake_space_transform=True,
        object_types=object_types,
    )
