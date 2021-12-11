import os
import re
import unreal
import time
import json

# ------------------- CONFIG -------------------------

agr_path = r'E:\10_AGR\de_dust2\14_deagle_4k_A_T'  # FBX folder to import
destination_path = r'/Game/LAST_TESTS'  # folder in UE to import
models_path = r'/Game/Meshes/CSGO'  # folder in UE with your models
sequence_name = '14_deagle_4k_A_T'  # your sequence name

import_cameras = True  # import cameras?
import_players = True  # import players?
import_pov = True  # import pov?
import_weapons = True  # import world weapons?
import_visibility = False  # import visibility from generated JSON file

save_current_level = False  # save current level before import?
clean_names = True  # fix '_mdl' at the end of the animation's name?
cleanup = True  # this will create 3 folders (POV, Weapons and Players) and distribute animations assets between them

rotate_by_180 = True
bounds_scale = 50
receives_decals = True

# since python is case-sensitive, you must type True or False in the config
# ---------------------------------------------------------

SequencePath = destination_path + '/' + sequence_name  # set sequence path
ue_ver = float(unreal.SystemLibrary.get_engine_version()[0:4].replace('5.0.', '5.0'))
editor_asset_lib = unreal.EditorAssetLibrary()
string_lib = unreal.StringLibrary()
assets = editor_asset_lib.list_assets(models_path, recursive=True)
imported_assets = editor_asset_lib.list_assets(destination_path, recursive=False)
AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
u_path = unreal.Paths
log = unreal.log_warning
log_e = unreal.log_error
start_time = time.time()

actor_location = unreal.Vector(0.0, 0.0, 0.0)
actor_rotation = unreal.Rotator(0.0, 0.0, 0.0)
obj_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor, actor_location, actor_rotation)  # spawn empty actor
obj_actor.set_actor_label('A_' + sequence_name)

seq_players_folder, seq_weapons_folder, seq_pov_folder = 0, 0, 0


def fbxcount(prefix):
    file_list = []
    for dirpath, dirs, files in os.walk(agr_path):
        for filename in files:
            all_files = os.path.join(dirpath, filename)
            if prefix in all_files and filename.endswith('.mdl.fbx'):
                file_list.append(os.path.join(dirpath, filename))
    return len(file_list)


total_fbx_to_import = 0
total_imported = 0
v_models_count = 0
w_models_count = 0
players_models_count = 0

if import_pov:
    v_models_count = fbxcount(' v_')  # get count of v* fbx in OS folder

if import_weapons:
    w_models_count = fbxcount(' w_')  # get count of v* fbx in OS folder

if import_players:
    players_models_count = fbxcount('tm_')  # get count of v* fbx in OS folder

total_fbx_to_import = v_models_count + w_models_count + players_models_count  # count of all models to import

text_label = 'Importing ' + str(total_fbx_to_import) + ' animations'


def sequence_creator():
    AssetTools.create_asset(sequence_name, destination_path, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())  # creating new sequencer
    mesh_location = unreal.Vector(0.0, 0.0, 0.0)
    mesh_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    mesh = unreal.load_asset(SequencePath)
    mesh.set_playback_start_seconds(0)
    unreal.EditorLevelLibrary.spawn_actor_from_object(mesh, mesh_location, mesh_rotation)
    global seq_players_folder
    seq_players_folder = unreal.MovieSceneSequenceExtensions.add_root_folder_to_sequence(mesh, 'Players')
    global seq_weapons_folder
    seq_weapons_folder = unreal.MovieSceneSequenceExtensions.add_root_folder_to_sequence(mesh, 'Weapons')
    global seq_pov_folder
    seq_pov_folder = unreal.MovieSceneSequenceExtensions.add_root_folder_to_sequence(mesh, 'POV')


def camera_importer():
    def camera_ue_options():
        import_options = unreal.MovieSceneUserImportFBXSettings()
        import_options.set_editor_property('create_cameras', False)
        import_options.set_editor_property('force_front_x_axis', False)
        import_options.set_editor_property('match_by_name_only', True)
        import_options.set_editor_property('reduce_keys', True)
        import_options.set_editor_property('reduce_keys_tolerance', 0.001)
        return import_options

    world = unreal.EditorLevelLibrary.get_editor_world()
    for dirpath, dirs, files in os.walk(agr_path):
        for filename in files:
            os_camera = os.path.join(dirpath, filename)
            sequence = unreal.load_asset(SequencePath)
            if 'camera' in os_camera:
                import_cameraname = os.path.join(dirpath, filename)
                log('found camera files: {}'.format(import_cameraname))
                camera_actor = unreal.EditorLevelLibrary().spawn_actor_from_class(unreal.CineCameraActor, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))  # spawn camera
                camera_actor.set_actor_label(filename.replace('.fbx', ''))  # change cameras name
                camera_component = camera_actor.get_cine_camera_component()
                binding = sequence.add_possessable(camera_actor)  # camera bindings
                binding_component = sequence.add_possessable(camera_component)  # camera component bindings
                camera_id = unreal.MovieSceneObjectBindingID()
                camera_id.set_editor_property('guid', binding.get_id())
                camera_cut_track = sequence.add_master_track(unreal.MovieSceneCameraCutTrack)
                camera_section = camera_cut_track.add_section()
                camera_section.set_camera_binding_id(camera_id)

                if ue_ver < 4.27 or ue_ver >= 5:
                    unreal.SequencerTools.import_fbx(world, sequence, [binding], camera_ue_options(), import_cameraname)  # 4.26 camera

                else:
                    unreal.SequencerTools.import_level_sequence_fbx(world, sequence, [binding], camera_ue_options(), import_cameraname)  # 4.27 camera

                find_focal_length_section = binding_component.find_tracks_by_type(unreal.MovieSceneFloatTrack)  # find Focal length section
                focal_length_section = find_focal_length_section[0].get_sections()  # gets it
                channel_focal_length = focal_length_section[0].get_channels()[0]  # select focal length channel
                keys_focal_length = channel_focal_length.get_keys()  # get all keys in the channel

                find_transform_section = binding.find_tracks_by_type(unreal.MovieScene3DTransformTrack)  # find Transform section
                transform_section = find_transform_section[0].get_sections()  # gets it
                channel_scale_x = transform_section[0].get_channels()[6]  # select Scale X channel
                keys_scale_x = channel_scale_x.get_keys()  # get all keys in the channel
                key_time = keys_scale_x[-1].get_time()  # get frame time of the last keyframe
                frame_number = key_time.get_editor_property('frame_number')
                channel_scale_x_last_keyframe = frame_number.to_tuple()[0]  # last keyframe number
                camera_section.set_range(0.0, channel_scale_x_last_keyframe - 1)  # set last keyframe in  master cut track and offset it by -1

                channel_location_x = transform_section[0].get_channels()[0]  # location X
                keys_location_x = channel_location_x.get_keys()
                channel_location_y = transform_section[0].get_channels()[1]  # location y
                keys_location_y = channel_location_y.get_keys()
                channel_location_z = transform_section[0].get_channels()[2]  # location z
                keys_location_z = channel_location_z.get_keys()
                channel_rotation_x = transform_section[0].get_channels()[3]  # rotation X
                keys_rotation_x = channel_rotation_x.get_keys()
                channel_rotation_y = transform_section[0].get_channels()[4]  # rotation y
                keys_rotation_y = channel_rotation_y.get_keys()
                channel_rotation_z = transform_section[0].get_channels()[5]  # rotation z
                keys_rotation_z = channel_rotation_z.get_keys()
                channel_scale_y = transform_section[0].get_channels()[7]  # scale y
                keys_scale_y = channel_scale_y.get_keys()
                channel_scale_z = transform_section[0].get_channels()[8]  # scale z
                keys_scale_z = channel_scale_z.get_keys()

                def camera_channels_offset(channel_keys):  # make offset
                    for key, value in enumerate(channel_keys):
                        t_frame_time = channel_keys[key].get_time()  # get frame time of keyframe
                        t_frame_number = t_frame_time.get_editor_property('frame_number')  # get frame number
                        channel_keys[key].set_time(t_frame_number - 1, 0.0, unreal.SequenceTimeUnit.DISPLAY_RATE)  # set offset

                camera_channels_offset(keys_focal_length)
                camera_channels_offset(keys_location_x)
                camera_channels_offset(keys_location_y)
                camera_channels_offset(keys_location_z)
                camera_channels_offset(keys_rotation_x)
                camera_channels_offset(keys_rotation_y)
                camera_channels_offset(keys_rotation_z)
                camera_channels_offset(keys_scale_x)
                camera_channels_offset(keys_scale_y)
                camera_channels_offset(keys_scale_z)

                sequence.set_playback_end(channel_scale_x_last_keyframe - 1)
                sequence.set_view_range_end((channel_scale_x_last_keyframe - 1) / 30 + 1)

                camera_actor.attach_to_actor(obj_actor, 'A_' + sequence_name, unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.SNAP_TO_TARGET, False)


def agr_importer(prefix, foldername):
    def skeleton_finder(s_pattern, replace):
        print('Importing .fbx file: {}'.format(os_animation_fullname))
        low_name = os_animation_fullname.lower()
        basename = os.path.basename(low_name)
        for assets_count, asset_name in enumerate(assets):
            if re.sub(s_pattern, replace, basename) in assets[assets_count]:
                skeleton_path = assets[assets_count]
                skeleton_asset = editor_asset_lib.load_asset(skeleton_path)
                log('Skeleton found: {}'.format(skeleton_path))
                if skeleton_path is None:
                    log_e('Skeleton was not found')
                return skeleton_path, skeleton_asset

    def skeleton_finder_custom(skeleton_name):
        print('Importing .fbx file: {}'.format(os_animation_fullname))
        for assets_count, asset_name in enumerate(assets):
            if skeleton_name in assets[assets_count]:
                skeleton_path = assets[assets_count]
                skeleton_asset = editor_asset_lib.load_asset(skeleton_path)
                log('Skeleton found: {}'.format(skeleton_path))
                return skeleton_path, skeleton_asset

    def fbx_importer(os_file, skeleton, obj):
        taskoptions = unreal.FbxImportUI()
        editor_asset_lib.checkout_asset(skeleton)
        taskoptions.set_editor_property('skeleton', obj)
        taskoptions.set_editor_property('import_materials', False)
        taskoptions.set_editor_property('import_textures', False)
        taskoptions.set_editor_property('import_animations', True)
        taskoptions.set_editor_property('import_mesh', False)
        taskoptions.set_editor_property('create_physics_asset', False)
        taskoptions.skeletal_mesh_import_data.set_editor_property('import_morph_targets', False)
        taskoptions.set_editor_property('automated_import_should_detect_type', True)
        task = unreal.AssetImportTask()
        task.filename = os_file
        task.destination_path = destination_path
        task.automated = True
        task.save = True
        task.replace_existing = True
        task.set_editor_property('options', taskoptions)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task, ])
        return os_file, skeleton, obj

    def ue_mesh_placer(animation_path):
        visibility_name = filename.replace('.fbx', '')
        mesh = unreal.load_asset(animation_path)  # load animation asset
        mesh_location = unreal.Vector(0.0, 0.0, 0.0)
        mesh_rotation = unreal.Rotator(0.0, 0.0, 0.0)
        animation_mesh = unreal.EditorLevelLibrary.spawn_actor_from_object(mesh, mesh_location, mesh_rotation)  # placing anim's mesh to world at 0,0,0
        animation_mesh.attach_to_actor(obj_actor, 'A_' + sequence_name, unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.SNAP_TO_TARGET, False)
        mesh_component = animation_mesh.get_component_by_class(unreal.SkeletalMeshComponent)
        mesh_component.set_bounds_scale(bounds_scale)
        if receives_decals:
            mesh_component.set_receives_decals(False)
        sequence = unreal.load_asset(SequencePath)
        animation_asset = unreal.AnimSequence.cast(mesh)
        params = unreal.MovieSceneSkeletalAnimationParams()
        params.set_editor_property('Animation', animation_asset)
        animation_binding = sequence.add_possessable(animation_mesh)  # get binding for animation's asset
        animation_track = animation_binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)  # add animation to sequencer
        animation_section = animation_track.add_section()
        animation_section.set_range(0, 30 * animation_asset.get_editor_property('sequence_length'))  # set animations length, 30 = fps
        animation_section.set_editor_property('Params', params)
        if import_visibility and prefix is not 'tm_':
            visibility_track = animation_binding.add_track(unreal.MovieSceneVisibilityTrack)  # add visibility track to sequencer
            visibility_section = visibility_track.add_section().get_channels()[0]

            for jdirpath, jdirs, jfiles in os.walk(agr_path):
                for jfilename in jfiles:
                    if os.path.splitext(jfilename)[1] == '.json':
                        json_filepath = os.path.join(jdirpath, jfilename)
                        with open(json_filepath) as json_file:
                            data = json.loads(json_file.read())
                            visibility_json = data[visibility_name]
                            for keyframe in visibility_json:
                                vis_keyframe = visibility_json[keyframe].lower()
                                if vis_keyframe == 'false':  # invert keyframes
                                    visibility_section.add_key(unreal.FrameNumber(int(keyframe) - 1), True, 0.0, unreal.SequenceTimeUnit.DISPLAY_RATE)
                                elif vis_keyframe == 'true':
                                    visibility_section.add_key(unreal.FrameNumber(int(keyframe) - 1), False, 0.0, unreal.SequenceTimeUnit.DISPLAY_RATE)

        if prefix is 'tm_':
            seq_players_folder.add_child_object_binding(animation_binding)
        if ' w_' in os_animation_fullname and prefix in os_animation_fullname:
            seq_weapons_folder.add_child_object_binding(animation_binding)
        if ' v_' in os_animation_fullname and prefix in os_animation_fullname:
            seq_pov_folder.add_child_object_binding(animation_binding)

    def main_importer(skeleton_p):
        fbx_importer(os_animation_fullname, skeleton_p[0], skeleton_p[1])
        anim_filename = u_path.get_clean_filename(os_animation_fullname.replace('.fbx', '').replace(' ', '_').replace('.', '_'))
        full_anim_path = destination_path + '/' + anim_filename
        if clean_names:
            editor_asset_lib.rename_asset(full_anim_path, destination_path + '/' + anim_filename.replace('_mdl', ''))
            nice_path = destination_path + '/' + anim_filename.replace('_mdl', '')
            ue_mesh_placer(nice_path)
            if cleanup:
                editor_asset_lib.rename_asset(nice_path, (destination_path + '/' + foldername + '/' + u_path.get_base_filename(nice_path, remove_path=True)))
        else:
            ue_mesh_placer(full_anim_path)
            if cleanup:
                editor_asset_lib.rename_asset(full_anim_path, (destination_path + '/' + foldername + '/' + u_path.get_base_filename(full_anim_path, remove_path=True)))
        editor_asset_lib.save_asset(SequencePath, only_if_is_dirty=True)
        slow_task.enter_progress_frame(1)
        global total_imported
        total_imported += 1

    for dirpath, dirs, files in os.walk(agr_path):
        for filename in files:
            if filename.endswith('.mdl.fbx'):
                os_animation_fullname = os.path.join(dirpath, filename)
                if slow_task.should_cancel():
                    break
                if prefix in os_animation_fullname and 'glove' not in os_animation_fullname and 'sleeve' not in os_animation_fullname:
                    pattern = 'afx.(\\d|\\d+) (.+)(.mdl.fbx)'
                    replacement = '\\2_Skeleton'
                    main_importer(skeleton_finder(pattern, replacement))

                elif 'glove' in os_animation_fullname and prefix in os_animation_fullname:
                    if '_hardknuckle' in os_animation_fullname and prefix in os_animation_fullname:  # find the skeleton, if user have one skeleton for hardknuckle gloves
                        for assets_count_g, asset_name_g in enumerate(assets):
                            g_skeleton = 'agr_v_glove_hardknuckle_Skeleton'
                            g_skeleton_black = 'agr_v_glove_hardknuckle_black_Skeleton'
                            g_skeleton_blue = 'agr_v_glove_hardknuckle_blue_Skeleton'
                            if g_skeleton in assets[assets_count_g]:
                                main_importer(skeleton_finder_custom(g_skeleton))
                            elif g_skeleton_black in assets[assets_count_g]:
                                main_importer(skeleton_finder_custom(g_skeleton_black))
                            elif g_skeleton_blue in assets[assets_count_g]:
                                main_importer(skeleton_finder_custom(g_skeleton_blue))

                    else:
                        pattern = 'afx.(\\d|\\d+) (.+)(.mdl.fbx)'
                        replacement = 'agr_\\2_Skeleton'
                        main_importer(skeleton_finder(pattern, replacement))

                elif 'sleeve' in os_animation_fullname and prefix in os_animation_fullname:
                    pattern = 'afx.(\\d|\\d+) (v_sleeve).+'
                    replacement = 'agr_\\2_Skeleton'
                    main_importer(skeleton_finder(pattern, replacement))


log('------- \nIMPORT STARTED... \nDetected {} UE version'.format(ue_ver))

if save_current_level:
    unreal.EditorLevelLibrary.save_current_level()  # saves level before import

with unreal.ScopedSlowTask(total_fbx_to_import, text_label) as slow_task:
    slow_task.make_dialog(True)

    sequence_creator()

    if import_cameras:
        camera_importer()

    if import_players:
        agr_importer('tm_', 'Players')

    if import_weapons:
        agr_importer(' w_', 'Weapons')

    if import_pov:
        agr_importer(' v_', 'POV')

    if rotate_by_180:
        obj_actor.set_actor_rotation(unreal.Rotator(0.0, 0.0, -180), False)  # rotate actor by 180 deg

end_time = time.time()
unreal.EditorDialog.show_message('CSGO tools', ('{} animations were imported in {} seconds'.format(str(total_imported), round(end_time - start_time))), unreal.AppMsgType.OK, unreal.AppReturnType.OK)

# shitcoded by adenex
