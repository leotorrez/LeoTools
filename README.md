# 4.2 NEWS
ORFif and offset have been fixed for the current version.
Offset fix is no longer backward compatible with pre-4.1 if you play an older version get 2.3 or below.
Your mods need to have `drawindexed = auto` within their IB block to work with the new offset fix.

Example:
```
[TextureOverrideShenheIB]
hash = 0b7d4e4d
handling = skip
drawindexed = auto
```

# LeoTools
Modding tools for GIMI, SRMI and HIMI (Most likely applicable to 3dmigoto modding in general yet not directly supported)

## XXMI Modding tools

Specific tools for mod makers to use on their mods. Users may also take advantage of these to fix half-finished mods.

- **ORFix.ini:** This is a global ini to fix reflection and outline in 3.0+ characters. [Read this guide to know how to use it in your mods.](https://github.com/leotorrez/LeoTools/blob/main/guides/ORFixGuide.md)  

- **multiplyweight.py:** Blender plugin that multiplies the weight of all vertices in a model. Useful to scale up your mod. [Read this guide to change character sizes](https://github.com/leotorrez/LeoTools/blob/main/guides/ChangeSizeGuide.md) 

- **speedControl.py:** Complementary task for animation mods. After merging all the frames, run this script in the animation folder to generate the animation controller and optimize the RAM usage of the animated mod.

- **FixXXXX.py:** Specific scripts to fix mods that have been broken by updates or complex shaders like dashes, 4.0 characters and so on.

## Blender addons and scripts

- **JoinMeshes.py:** Blender plugin that eases the repetitive tasks of mod exporting. Includes auto modifier application, shapekeys and even exporting every frame of animation as a unique mod folder.

- **quickBlenderImport.py:** Eases the process of importing models from dumps, applies materials to each corresponding meshes and does some clean-up tasks on the mesh leaving it in nice quads.

## 3DMigoto tools
These can be applied to any 3DM install.

- **DailyLumine.py**:** Despite its name is not only for lumine. It's a script meant to deactivate all the folders within a specific directory(assuming you have your mods organized by character folder) and randomly reactivate only one of them, hence swapping active mod on launch. It is better to use this script in the launch =  clause of your 3dm and then have the script launch the game for you. You might need to set Python as the default exe for .py files.