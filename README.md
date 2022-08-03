# UEditingTools for Unreal Engine 4.27 and 5.0

This widget can:
- Import players, weapons and viewmodels with proper skeletons (currently supports CSGO, CSS, TF2 and CS 1.6)
- Import cameras (multiple supports too) with correct offset by 1 frame and adjust them
- Place all models to the level and sequencer
- Set bounds with user's value
- Set "Recieve Decals" parameter for all imported assets
- Import the visibility data from blender (you'll need [io_scene_CSGO](https://github.com/adenexvfx/io_scene_CSGO) for blender to use this).
- Attach all models to the EmptyActor automatically and rotate them by 180 degrees

# Download and install
[Download link for the widget](https://github.com/adenexvfx/UEditingTools/releases/download/v1.2.2/UEditingTools.zip)

Close Unreal. Merge the ```Content``` folder from archive with the content folder in your project. Open Unreal and go to the Plugins Browser tab and enable following plugins: ```Editor Scripting Utilities```, ```Python Editor Script Plugin``` and ```Sequencer Scripting```. Restart UE, right-click on the widget asset, in the content browser, and select ```Run Editor Utility Widget```. The widget should open immediately. For the full setup of the widget and your library 
To fully configure the widget and your asset library, follow [this tutorial](https://youtu.be/9r7T2mFlLV4). If you need any help with the widget, join my [Discord server](https://discord.gg/CqCHkUCpxq)

![image](https://i.imgur.com/b6cdmxX.png)
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

## POV tab:
This tool can spawn unlimited amount of meshes for your POV, add it to the sequencer and hide them depending on the focal length of your main POV camera (useful for sniper POVs)

# Changelog
- ```v1.2.0```
CS:S is now supported. Code in all modules was rewritten to improve performance. POV section is moved from exprimental feautures to the normal state. Added spawn cables function to the Map fixing module. Now cleaner will leave all unreal.Note actors needed for cables and sky_camera. Changed the method of scaling levels.

- ```v1.1.0```
CS 1.6 and TF2 are now supported.  The widget supports only 4.27 and the latest release of 5.0 (Preview 2). The interface changed.  Better performance in MasterSkeleton mode. The sequencer will be automatically opened when the import is completed. AfxCam is now supported. The camera's settings will be automatically set to 'do not override' and 16:9 DSLR. Added the 'experimental' tab

- ```v1.0.1```
Some minor bugs were fixed. Now you can choose fps in settings (if you recorded AGR file with 100 fps, set here 100 fps). Also i've added 'S' (select) buttons next to Players and Gloves skeletons fields in OneSkeleton mode. So now you can select skeleton in Content Browser, hit the 'S' button and it's path will setup automatically.
