# LeoTools
Modding tools for GIMI, SRMI and HIMI

**DailyLumine.py:** Despite it's name is not only for lumine. It's a script meant to deactivate all the folders within a specific directory(assuming you have your mods orginized by character folder) and randomly reactivating only one of them, hence swapping active mod on launch. It is better to use this script in the launch =  clause of your 3dm and then have the script launch the game for you. You might need to set python as the default exe for .py files.

**FixXXXX.py:** Specific scripts to fix mods that have been broken by updates or complex shaders like dashes, 4.0 characters and so on.

**JoinMeshes.py:** Blender plugin that eases the repeatetive tasks of mod exporting. Includes auto modifier application, shapekeys and even exporting every frame of an animation as an unique mod folder.

**multiplyweight.py:** Blender plugin that multiplies the weight of all vertices in a model. Useful to scale up your mod. Check offset tools in releases for complemetary tools.

**quickBlenderImport.py:** Eases the process of importing models from dumps, applies materials to each corresponding meshes and does some clean up tasks on the mesh leaving it in nice quads.

**speedControl.py:** Complementary task for animation mods. After merging all the frames together, run this script in the animation folder to generate the animation controller and optimize the ram usage of the animated mod.