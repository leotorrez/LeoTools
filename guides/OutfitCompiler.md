# Deprecated    
The functionality of this tool now comes built in XXMITools. Do not use this tool any further

# Use case and applications
This tool is intended to reduce the filesize of merged mods by not exporting the same parts of your model every time you wanna add an accesory or hairstyle. It also makes it easier for your toggle to be merged with other merged mods made with this same tool. To avoid confusion we will call merged the ones made with the classic tool and compiled the ones made with this one.

# Workspace and set-up

With traditional merged mods you had to set one each variant of your mods as a frame of animation in blender's timeline.
In compiled mods you set each part of your mod as a frame of the animation instead. This means that you will have to set up your workspace differently.

For example:

Let's say your mod has a base body, a skirt, a hat, a shirt and a pair of shoes. In the traditional method you would have to set up 5 frames of animation in blender's timeline, one for each variant of your mod(wich would be 16 variants). In the compiled method you would have to set up 5 frames of animation in blender's timeline, one for each part of your mod.

Frame 1: Base body
Frame 2: Skirt
Frame 3: Hat
Frame 4: Shirt
Frame 5: Shoes

The more toggles your mod has the less complex this new setup becomes and the more troublesome the old one becomes. So the tool to chose will depend on the complexity of your mod, the amount of toggles and the amount of merged mods you want to compile.

# How to use

1. Download the script from the repository.
2. Place it in the same folder as your exported "animation frames".
3. Run the script.

That's it. The script will create a new folder called "Results" and place the compiled mod there. You can now use this folder as a mod in your game.

By default it sets the numpad keys as the toggle triggers. But you can customize those with the -k flag, the name of the variables used within the ini to control those can also be customized with the -c flag by listing all the elements you want to compile in the order they were exported. Use -h to see all the flags you can use, they are all quite useful and make this tool more powerful.

If you have troubles using this tool feel free to contact me in discord at leotorrez, I will be glad to help you.


## Warning
This tool was made and tested in genshin, hence it's use in other games might need adjustments (but the underlaying logic should apply to all 3dm games). The tool is intended to be used with mods freshly exported from the export script, I don't guarantee it will work with mods that have been modified in any way.