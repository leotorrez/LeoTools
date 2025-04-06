# How to use this Reflection/Outline FIX

> **Notes:** Since pyro traveler release, you can use ORFix in traveler to fix their broken tattoo & nightsoul effect. Aditionally to mod said tattoo texture, do so by hash. Using ORFix in Natlan characters also fixes their Nightsoul effect being broken.

1) Place [this ini](https://github.com/leotorrez/LeoTools/blob/main/releases/ORFix.ini) into the folder `3Dmigoto/Mods/BufferValues`

2) At the bottom of each modded [TextureOverride {Character} {ObjectPart}], type the following command:

```ini
run = CommandList\global\ORFix\ORFix
```

## Simple Example

```ini
[TextureOverrideLaylaHead]
hash = xxxxxxxx
match_first_index = 0
ib = ResourceLaylaHeadIB
ps-t1 = ResourceLaylaHeadNormalMap
ps-t1 = ResourceLaylaHeadDiffuse
ps-t2 = ResourceLaylaHeadLightMap
run = CommandList\global\ORFix\ORFix
```

Some characters might only need this fix on some of their parts but not all. Simply add it to where it seems necesary, leave the rest untouched.

A good example of it is Lynette. She needs the fix in Body and Extra but not Head and Dress.

Note: a good way to tell if the fix is needed is to check if the slot 0 is a NormalMap texture as in the example above.

## Mixed case

```ini
[TextureOverrideLynetteHead]
hash = xxxxxxxx
match_first_index = 0
ib = ResourceLynetteHeadIB
ps-t0 = ResourceLynetteHeadDiffuse
ps-t1 = ResourceLynetteHeadLightMap

[TextureOverrideLynetteBody]
hash = xxxxxxxx
match_first_index = 16257
ib = ResourceLynetteBodyIB
ps-t0 = ResourceLynetteBodyNormalMap
ps-t1 = ResourceLynetteBodyDiffuse
ps-t2 = ResourceLynetteBodyLightMap
run = CommandList\global\ORFix\ORFix

[TextureOverrideLynetteDress]
hash = xxxxxxxx
match_first_index = 65223
ib = ResourceLynetteDressIB
ps-t0 = ResourceLynetteDressDiffuse
ps-t1 = ResourceLynetteDressLightMap

[TextureOverrideLynetteExtra]
hash = xxxxxxxx
match_first_index = 68358
ib = ResourceLynetteExtraIB
ps-t0 = ResourceLynetteExtraNormalMap
ps-t1 = ResourceLynetteExtraDiffuse
ps-t2 = ResourceLynetteExtraLightMap
run = CommandList\global\ORFix\ORFix
```

## How to post your mod

When including this ini in your Mods. Make sure the user saves [ORFix.ini](https://github.com/leotorrez/LeoTools/blob/main/releases/ORFix.ini) in the right folder. (in the case of XXMI it comes already installed, configured and gets auto updated)

Instead of including it in your mod folder, is recomended to include the download link to this ini in your mod description. That way, the user always gets the latest version and doesn't come asking you for an updated fix <3

[Lynettenewcoolmod.zip](fakelink.com)

Required files: [ORFix.ini](https://github.com/leotorrez/LeoTools/blob/main/releases/ORFix.ini)
