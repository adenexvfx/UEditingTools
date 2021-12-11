import unreal
import re
import time

# -------- variables

'''scaling = False
world_scale = 1
sorting = True
delete_light = True'''


# -----------

level_lib = unreal.EditorLevelLibrary()
log = unreal.log_warning

start_time = time.time()

actor_vector = unreal.Vector(0.0, 0.0, 0.0)
actor_rotator = unreal.Rotator(0.0, 0.0, 0.0)
obj_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor, actor_vector, actor_rotator)  # spawn empty actor
obj_actor.set_actor_label('ACTOR_SCALE')  # set label

root = obj_actor.get_component_by_class(unreal.SceneComponent)
root.set_mobility(unreal.ComponentMobility.STATIC)  # switch MOVABLE state to STATIC

all_actors = level_lib.get_all_level_actors()


def remover_function():
    for i in all_actors:
        directional = unreal.DirectionalLight
        point = unreal.PointLight
        rect = unreal.RectLight
        spot = unreal.SpotLight

        if delete_light:
            if i.__class__ == directional or i.__class__ == point or i.__class__ == rect or i.__class__ == spot:
                i.destroy_actor()
        if i.__class__ == unreal.Note and 'wire' not in i.get_name() and not re.match(r'\d', i.get_name()) and 'cable' not in i.get_name():
            i.destroy_actor()
        if 'Logic' in i.get_name() or 'logic' in i.get_name():
            i.destroy_actor()
        actor_component = i.get_component_by_class(unreal.StaticMeshComponent)
        if hasattr(actor_component, 'static_mesh'):
            if actor_component.static_mesh.get_name() == 'no_triangles_in_brush':
                i.destroy_actor()
        if hasattr(actor_component, 'get_editor_property'):
            actor_asset = actor_component.get_editor_property('static_mesh')
            asset_material = actor_asset.get_material(0)
            if hasattr(asset_material, 'get_name'):
                if asset_material.get_name() == 'M_missingPropMaterial':
                    i.destroy_actor()
        if 'Hammuer' in i.__class__.__name__:
            i.destroy_actor()


def sort_function():
    for i in saved_actors:
        if i.__class__ == unreal.StaticMeshActor and '_prop_' in i.get_name():
            i.set_folder_path('Props')
        if i.__class__ == unreal.StaticMeshActor and '_prop_' not in i.get_name():
            i.set_folder_path('WorldMeshes')
        if 'light' in i.get_name() and i.__class__ is not unreal.StaticMeshActor and delete_light is False:
            i.set_folder_path('Light')
        if re.match(r'\d', i.get_name()) or 'wire' in i.get_name() or 'cable' in i.get_name():
            i.set_folder_path('Wires')
        if i.__class__ == unreal.DecalActor:
            i.set_folder_path('Decals')


def scale_function():
    for i in saved_actors:
        if i is not obj_actor:
            level_lib.set_actor_selection_state(i, True)
            i.attach_to_actor(obj_actor, 'ACTOR_SCALE', unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, True)

    obj_actor.set_actor_scale3d(unreal.Vector(float(world_scale), float(world_scale), float(world_scale)))  # set scale

    for i in saved_actors:
        if i is not obj_actor:
            level_lib.set_actor_selection_state(i, True)
            i.detach_from_actor(unreal.DetachmentRule.KEEP_WORLD, unreal.DetachmentRule.KEEP_WORLD, unreal.DetachmentRule.KEEP_WORLD)


remover_function()
level_lib.clear_actor_selection_set()
saved_actors = level_lib.get_all_level_actors()
if scaling:
    scale_function()
sort_function()
level_lib.clear_actor_selection_set()
obj_actor.destroy_actor()

end_time = time.time()
if scaling:
    unreal.EditorDialog.show_message('CSGO tools', (f'Map cleaned and scaled in {round(end_time - start_time, 2)} seconds'), unreal.AppMsgType.OK, unreal.AppReturnType.OK)
else:
    unreal.EditorDialog.show_message('CSGO tools', (f'Map cleaned in {round(end_time - start_time, 2)} seconds'), unreal.AppMsgType.OK, unreal.AppReturnType.OK)