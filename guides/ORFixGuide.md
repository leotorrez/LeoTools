# How to use this Reflection/Outline FIX

> **Notes:** Since pyro traveler release, you can use ORFix in traveler to fix their broken tattoo & nightsoul effect. Aditionally to mod said tattoo texture, do so by hash. Using ORFix in Natlan characters also fixes their Nightsoul effect being broken.

```ini
run = CommandList\GIMI\SetTexture
```

## Simple Example

```ini
[TextureOverrideLaylaHead]
hash = xxxxxxxx
match_first_index = 0
ib = ResourceLaylaHeadIB
Resource\GIMI\NormalMap = ref ResourceLaylaHeadNormalMap
Resource\GIMI\Diffuse = ref ResourceLaylaHeadDiffuse
Resource\GIMI\LightMap = ref ResourceLaylaHeadLightMap
run = CommandList\GIMI\SetTexture
```

Some characters don't have NormalMap in all of their parts, in which case you can skip that line.

A good example of it is Lynette. She needs the fix in Body and Extra but not Head and Dress.

## Mixed case

```ini
[TextureOverrideLynetteHead]
hash = xxxxxxxx
match_first_index = 0
ib = ResourceLynetteHeadIB
Resource\GIMI\Diffuse = ref ResourceLynetteHeadDiffuse
Resource\GIMI\LightMap = ref ResourceLynetteHeadLightMap
run = CommandList\GIMI\SetTexture

[TextureOverrideLynetteBody]
hash = xxxxxxxx
match_first_index = 16257
ib = ResourceLynetteBodyIB
Resource\GIMI\NormalMap = ref ResourceLynetteBodyNormalMap
Resource\GIMI\Diffuse = ref ResourceLynetteBodyDiffuse
Resource\GIMI\LightMap = ref ResourceLynetteBodyLightMap
run = CommandList\GIMI\SetTexture

[TextureOverrideLynetteDress]
hash = xxxxxxxx
match_first_index = 65223
ib = ResourceLynetteDressIB
Resource\GIMI\Diffuse = ref ResourceLynetteDressDiffuse
Resource\GIMI\LightMap = ref ResourceLynetteDressLightMap
run = CommandList\GIMI\SetTexture

[TextureOverrideLynetteExtra]
hash = xxxxxxxx
match_first_index = 68358
ib = ResourceLynetteExtraIB
Resource\GIMI\NormalMap = ref ResourceLynetteExtraNormalMap
Resource\GIMI\Diffuse = ref ResourceLynetteExtraDiffuse
Resource\GIMI\LightMap = ref ResourceLynetteExtraLightMap
run = CommandList\GIMI\SetTexture
```

## How to post your mod

Mods using this library should let the user know that it requires XXMI to work as intended. Please remember to link the releases page of XXMI in your mod description.
