[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F1F7ULKBY)
# 4.4 NEWS

- The new optimization feature (a lazy filter) breaks all mods while active. Go to the bottom of your graphics config in game to turn it off and keep enjoying mods.
- Some mods broke, general fix [HERE!](https://github.com/leotorrez/LeoTools/blob/main/Fix4.4.py).
- ORFix needed a minor update to work with 4.4. It's already updated in the repo. Please updated and it will fix your mods.

# LeoTools
Modding tools for GIMI, SRMI and HIMI (Most likely applicable to 3dmigoto modding in general yet not directly supported)

## XXMI Modding tools

Specific tools for mod makers to use on their mods. Users may also take advantage of these to fix half-finished mods.

- **ORFix.ini:** This is a global ini to fix reflection and outline in 3.0+ characters. [Read this guide to know how to use it in your mods.](https://github.com/leotorrez/LeoTools/blob/main/guides/ORFixGuide.md) 

- **Region(.ini) Check:** A tracking global ini to detect which region your character walks into or teleports to. Useful to toggle mods based on said regions. [For a guide click here](https://github.com/leotorrez/LeoTools/blob/main/guides/RegionCheckGuide.md)

- **FixDash.ini:** My pride and joy. It fixes ALL Yelan and Lynette mods without the need to apply a script to your mods. Now you simply need to drop this file to `/Mods/BufferValues` and problem solved. Compatible with script methods.

- **multiplyweight.py:** Blender plugin that multiplies the weight of all vertices in a model. Useful to scale up your mod. [Read this guide to change character sizes](https://github.com/leotorrez/LeoTools/blob/main/guides/ChangeSizeGuide.md) 

- **speedControl.py:** Complementary task for animation mods. After merging all the frames, run this script in the animation folder to generate the animation controller and optimize the RAM usage of the animated mod.

- **FixXXXX.py:** Specific scripts to fix mods that have been broken by updates or complex shaders like dashes, 4.0 characters and so on.

## 3DMigoto tools
These can be applied to any 3DM install.

- **Outfit Compiler:** A script that compiles all the mods in a folder into a single mod. This allows you to export your toggles as single mods and lately compile them into a single mod alongside your base body. [For a quick guide click here](https://github.com/leotorrez/LeoTools/blob/main/guides/OutfitCompiler.md)

- **DailyLumine.py:** Despite its name is not only for lumine. It's a script meant to deactivate all the folders within a specific directory(assuming you have your mods organized by character folder) and randomly reactivate only one of them, hence swapping active mod on launch. It is better to use this script in the launch =  clause of your 3DM and then have the script launch the game for you. You might need to set Python as the default exe for .py files.

- **.ModManager v2.ahk** is an AutoHotKey v2 script that speeds up the process of adding and removing the word DISABLED from the start of folders to speed up mod handling. If you don't have experience with AutoHotKey is better to avoid it.
ALT + D to toggle folder

## Blender addons and scripts

- **JoinMeshes.py:** Blender plugin that eases the repetitive tasks of mod exporting. Includes auto modifier application, shapekeys and even exporting every frame of animation as a unique mod folder. Useful for advanced modding and faster workflows. [For a guide click here](https://github.com/leotorrez/LeoTools/blob/main/guides/JoinMeshesGuide.md)

- **quickBlenderImport.py:** Eases the process of importing models from dumps, applies materials to each corresponding meshes and does some clean-up tasks on the mesh leaving it in nice quads. 
