# CS:GO tools for Unreal Engine 4.26+

Download link for the widget: [Mediafire](https://www.mediafire.com/file/dfnxljuyf70xiq8/CSGO_Tools.rar/file). Source files: [GitHub](https://github.com/adenexvfx/CSGOtools)

This widget have 3 modules.

The first one (AGR importer) can:
- Import players, weapons and viewmodels with proper skeletons
- Import with 'one skeleton' mode (single skeleton for player models and single skeleton for gloves/sleeve)
- Import cameras (yes, multiple supports too) with correct offset by 1 frame
- Set sequencer length from camera's length
- Place all models to world and sequencer and sort them between 3 folders by type
- Attach all models to the EmpyActor automatically and rotate them by 180
- Set bounds with user's value
- Set "Recieve Decals" parameter for all imported assets
- Import visibility from blender (you'll need [this addon for blender](https://github.com/adenexvfx/CSGOtools/blob/main/agr_tools_for_blender.zip) to use this: 

The second (Map Fixer) module was created to help you with fresh imported maps from Hammuer. It can:
- Remove all light sources from your map
- Clean the whole level and sort all assets by type under one second
- Scale all map in single click

The third one (Texture Fixer) can convert all normals and masks textures to correct compression in selected folder.

Here's the tutorial how to use it: https://youtu.be/fbwMt57fvCI

![image](https://user-images.githubusercontent.com/93075018/145672495-001f1e72-86e9-461b-9b22-16bd22dfc636.png)

![image](https://user-images.githubusercontent.com/93075018/145672504-1a949cab-4518-4cc1-8443-339a22fbce4d.png)

# AGR tools addon for Blender

[This addon](https://github.com/adenexvfx/CSGOtools/blob/main/agr_tools_for_blender.zip) will help you clean up your scene after importing animations from .agr file. It works in pair with the **CS:GO tools** widget and will export visibility for it. After installation, you'll find this addon at the right-side docked panel. Also it can place all your animation to 0,0,0 just for the first frame (will take some time to execute). This option prevents meshes from other sequences from being displayed.

![image](https://user-images.githubusercontent.com/93075018/145672896-09ffa7cd-68c4-4d76-92fd-1d36704641cf.png)
