# Under construction
This guide is still under construction. It will be updated as soon as possible. Feel free to read it to get a basic understanding of the innerowrkings of the tool, but keep in mind that some things might change in the future.

# JoinMeshes

This is a tool created to help with the creation of mods in blender. It seeks to simplify the most repetitive and tedious tasks such as joining objects into a few meshes and exporting them to the game. In most cases this is not a big issue, but when you have to undo this joining process after each export it gets tiresome quickly. This automatizes that process and allows to export variants and animations with a single click.

## How to use

The setup in the outline must be as such: 

When you import a model into blender it will have parts like TravelerHead, TravelerBody, etc. These are parts of the main object, in this case `Traveler`. You can create collections named after said parts so their contents are joined into these "containers":

Example image

When you click on Export Mod it will perform several extra tasks in the following order:

1. Make all objects single use to temporarily remove linked data
2. Apply all visible modifiers
3. Apply all shapekeys
4. Remove the vertex groups that contain the word MASK in their name. Why?
5. Join all objects in the collection into a single "container" mesh
6. Export the resulting meshes into a mod folder
7. Undo all the past steps so your project ends up as it was before starting the process

## Exporting single mod and Output Folder 

If you want to export a single mod you can do so by clicking on the Export Mod button. By default it will be exported on the same folder as 
your dump folder is located with the name [Object]Mod. If you set up an output folder on the optional field it will be exported there instead.
(Still called [Object]Mod.)

Example image2

## Exporting animations

The animation method we currently use consists of exporting every frame of the animation as a separate mode, merge them all into a massive toggle and have a script cycle throughout them to simulate movement. Manually the exporting process can be quite tedious, but with this tool it can be done much faster

Internally it will do the same as the Export Mod button, but will repeat it once per each frame of animation in your blender project. It uses start and end frames as inputs so make sure to configure those properly before getting started as the image below.

Example image3

When is done you will end up with a long list of [Object]fxxxxMod folders, each containing a single frame of the animation. You can then use animation scripts to merge them all into a single toggle. (More on scripts down below.)

## Exporting variant mods

Variant mods are toggles that consist of a base mod with small variations of the same such as a different hat, clothing, accesories or even less of them. We can abuse the animation mechanic to achieve this same result. You would simply need to set up a variant per frame of animation and then export as you would any other animation. However in this case you will only need to use the merge script to combine them all into a single toggle.

## Post processing scripts
# ATTENTION!!! TOOL ONLY FOR ADVANCED USERS
The new section of the toolkit will run scripts in your dump folder in whichever order you have them setup(using said dump folder as its working directory). You can include arguments alongside with your script to customize their functionality some more. This will run on parallel to blender so your UI won't be locked during the export process. Feel free to keep working on your project while the scripts run in the background.

example image4

