import unreal
import time

convert_masks = True
convert_normals = True


source_dir = '/Game/CSGO/Textures/brick/hr_brick/venice'  # path for textures

editor_asset_lib = unreal.EditorAssetLibrary()
string_lib = unreal.StringLibrary()
assets = editor_asset_lib.list_assets(source_dir, recursive=True)
changed = 0


def textures(value, compression):
    masks_patterns = [value]
    for asset in assets:
        for pattern in masks_patterns:
            if string_lib.ends_with(asset, pattern):
                asset_obj = editor_asset_lib.load_asset(asset)
                asset_obj.set_editor_property('sRGB', False)
                asset_obj.set_editor_property('CompressionSettings', compression)
                unreal.EditorAssetLibrary.save_asset(asset, only_if_is_dirty=True)
                global changed
                changed += 1
                break


start_time = time.time()
if convert_masks is True:
    textures('_masks', unreal.TextureCompressionSettings.TC_MASKS)
    textures('_exp', unreal.TextureCompressionSettings.TC_MASKS)

if convert_normals is True:
    textures('_normal', unreal.TextureCompressionSettings.TC_NORMALMAP)
    textures('_normals', unreal.TextureCompressionSettings.TC_NORMALMAP)
    textures('_n', unreal.TextureCompressionSettings.TC_NORMALMAP)

end_time = time.time()
unreal.EditorDialog.show_message('CSGO tools', (f'{str(changed)} textures converted in {round(end_time - start_time, 2)} seconds'), unreal.AppMsgType.OK, unreal.AppReturnType.OK)
