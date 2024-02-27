# UEditingTools for Unreal Engine 5

This widget can:
- Import players, weapons and viewmodels with proper skeletons (currently supports CS2, CSGO, CSS, TF2 and CS 1.6)
- Import cameras (multiple supports too) with correct offset by 1 frame and adjust them
- Place all models to the level and sequencer
- Set bounds with user's value
- Set "Recieve Decals" parameter for all imported assets
- Import the visibility data from blender (you'll need [io_scene_CSGO](https://github.com/adenexvfx/io_scene_CSGO) for blender to use this).
- Attach all models to the EmptyActor automatically and rotate them by 180 degrees

# Download and install
[Download link for the widget](https://github.com/adenexvfx/UEditingTools/releases)

Close Unreal. Merge the ```Content``` folder from archive with the content folder in your project. Open Unreal and go to the Plugins Browser tab and enable following plugins: ```Editor Scripting Utilities```, ```Python Editor Script Plugin``` and ```Sequencer Scripting```. Restart UE, right-click on the widget asset, in the content browser, and select ```Run Editor Utility Widget```. The widget should open immediately. For the full setup of the widget and your library 
To fully configure the widget and your asset library, follow [this tutorial](https://youtu.be/9r7T2mFlLV4). If you need any help with the widget, join my [Discord server](https://discord.gg/CqCHkUCpxq)

![image](https://i.imgur.com/bs9b3Zb.png)
![image](https://user-images.githubusercontent.com/93075018/145672504-1a949cab-4518-4cc1-8443-339a22fbce4d.png)

# Other features
## Map Fixer tab:
- Can remove all light sources from your map
- Clean the whole level and sort all assets by type under one second
- Scale the level in single click
- Spawn cables

## Texture Fixer tab:
- Can convert all normal textures in the selected folder from default compression to normal compression
- Can convert all masks textures in the selected folder from default compression to masks compression

## Camera tab:
This tool can move and rotate selected camera by entered values

## Time Remap helper:
This tool will assits user to create timeremapped sequencer based on TimeRemap asset by kit
