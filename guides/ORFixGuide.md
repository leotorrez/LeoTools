To use this reflection/outline color shader fix: 

1) Place [this ini](https://github.com/leotorrez/LeoTools/blob/main/releases/ORFix.ini) into the folder `3Dmigoto/Mods/BufferValues `

2) At the bottom of each modded [TextureOverride {Character} {ObjectPart}], type the following command:

```ini
run = CommandList\global\ORFix\ORFix
```
Example:

```ini
[TextureOverrideLaylaHead]
hash = b617aa07
match_first_index = 0
ib = ResourceLaylaHeadIB
ps-t0 = ResourceLaylaHeadDiffuse
ps-t1 = ResourceLaylaHeadLightMap
run = CommandList\global\ORFix\ORFix
```

Some characters might only need this fix on some of their parts but not all. Simply add it to where it seems necesary, leave the rest untouched.

A good example of it is Lynette. She needs the fix in Body and Extra but not Head and Dress.

```ini
[TextureOverrideLynetteHead]
hash = 010cf88a
match_first_index = 0
ib = ResourceLynetteHeadIB
ps-t0 = ResourceLynetteHeadDiffuse
ps-t1 = ResourceLynetteHeadLightMap

[TextureOverrideLynetteBody]
hash = 010cf88a
match_first_index = 16257
ib = ResourceLynetteBodyIB
ps-t0 = ResourceLynetteBodyNormalMap
ps-t1 = ResourceLynetteBodyDiffuse
ps-t2 = ResourceLynetteBodyLightMap
run = CommandList\global\ORFix\ORFix

[TextureOverrideLynetteDress]
hash = 010cf88a
match_first_index = 65223
ib = ResourceLynetteDressIB
ps-t0 = ResourceLynetteDressDiffuse
ps-t1 = ResourceLynetteDressLightMap

[TextureOverrideLynetteExtra]
hash = 010cf88a
match_first_index = 68358
ib = ResourceLynetteExtraIB
ps-t0 = ResourceLynetteExtraNormalMap
ps-t1 = ResourceLynetteExtraDiffuse
ps-t2 = ResourceLynetteExtraLightMap
run = CommandList\global\ORFix\ORFix
```

When including this ini in your Mods. Make sure the user saves [ORFix.ini](https://github.com/leotorrez/LeoTools/blob/main/releases/ORFix.ini) in the right folder.

Instead of including it in your mod folder, is recomended to include the download link to this ini in your mod description. That way, the user always gets the latest version and doesn't come asking you for an updated fix <3

Example:

[Lynettenewcoolmod.zip](fakelink.com)

Required files: [ORFix.ini](https://github.com/leotorrez/LeoTools/blob/main/releases/ORFix.ini)