#Requires AutoHotkey v2.0
#HotIf WinActive("ahk_class CabinetWClass")
!d::
{
    Send "{F2}"
    Send "^{Home}"
    Send "+{Right 8}"
    ClipboardOld:=A_Clipboard
    SendInput "^c"
    Sleep "100"
    selText:=A_Clipboard
    A_Clipboard:=ClipboardOld
    if selText == "DISABLED"
    {
        Send "{Backspace}"
        Send "{Enter}"
    }
    else{
        Send "^{Home}"
        Send "DISABLED"
        Send "{Enter}"
    }
    return
}
; Nahida

[KeySwapHood]
key = 5
condition = $active == 1
type = cycle
$hood = 	1,0,0
$headH = 	1,0,0
$headNoCrown = 	0,1,0
$earsD = 	0,1,1
$headD = 	0,0,1

[KeySwapThighHighs]
key = 6
condition = $active == 1
type = cycle
$thighHighs = 1,0

; Present ----------------------

[Present]
post $active = 0
run = CommandListCreditInfo

; Constants -------------------------
[Constants]
global $active = 0
global $creditinfo = 0
global $base = 1
global persist $thighHighs = 1
global persist $hood = 1
global persist $earsD = 0
global persist $headH = 1
global persist $headD = 0
global persist $headNoCrown = 0

; Overrides -------------------------

[TextureOverrideNahidaPosition]
hash = 7106f05d
vb0 = ResourceNahidaPosition
$active = 1

[TextureOverrideNahidaBlend]
hash = de60b92f
vb1 = ResourceNahidaBlend
handling = skip
draw = 31457, 0 

[TextureOverrideNahidaTexcoord]
hash = 902b57ef
vb1 = ResourceNahidaTexcoord

[TextureOverrideNahidaVertexLimitRaise]
hash = ee37e2d7

[TextureOverrideNahidaIB]
hash = 9b13c166
;hash = 8b268d05
handling = skip


[TextureOverrideNahidaHead]
hash = 9b13c166
;hash = 8b268d05
match_first_index = 0
ib = ResourceNahidaHeadIB
ps-t0 = ResourceNahidaHeadNormalMap
ps-t1 = ResourceNahidaHeadDiffuse
ps-t2 = ResourceNahidaHeadLightMap
run = CommandList\global\ORFix\ORFix
if $base == 1
  drawindexed = 3, 0, 0
endif
if $thighHighs == 1
  drawindexed = 3, 3, 0
endif
if $hood == 1
  drawindexed = 3, 6, 0
endif
if $earsD == 1
  drawindexed = 3, 9, 0
endif
if $headH == 1
  drawindexed = 11217, 12, 0
endif
if $headD == 1
  drawindexed = 18366, 11229, 0
endif
if $headNoCrown == 1
  drawindexed = 13140, 29595, 0
endif


[TextureOverrideNahidaBody]
hash = 9b13c166
;hash = 8b268d05
match_first_index = 31143
ib = ResourceNahidaBodyIB
ps-t0 = ResourceNahidaBodyNormalMap
ps-t1 = ResourceNahidaBodyDiffuse
ps-t2 = ResourceNahidaBodyLightMap
run = CommandList\global\ORFix\ORFix
if $base == 1
  drawindexed = 75411, 0, 0
endif
if $thighHighs == 1
  drawindexed = 12441, 75411, 0
endif
if $hood == 1
  drawindexed = 12021, 87852, 0
endif
if $earsD == 1
  drawindexed = 693, 99873, 0
endif
if $headH == 1
  drawindexed = 3, 100566, 0
endif
if $headD == 1
  drawindexed = 3, 100569, 0
endif
if $headNoCrown == 1
  drawindexed = 3, 100572, 0
endif


[TextureOverrideNahidaDress]
hash = 9b13c166
;hash = 8b268d05
match_first_index = 71187
ib = null
ps-t0 = ResourceNahidaDressNormalMap
ps-t1 = ResourceNahidaDressDiffuse
ps-t2 = ResourceNahidaDressLightMap
if $base == 1
  drawindexed = 0, 0, 0
endif
if $thighHighs == 1
  drawindexed = 0, 0, 0
endif
if $hood == 1
  drawindexed = 0, 0, 0
endif
if $earsD == 1
  drawindexed = 0, 0, 0
endif
if $headH == 1
  drawindexed = 0, 0, 0
endif
if $headD == 1
  drawindexed = 0, 0, 0
endif
if $headNoCrown == 1
  drawindexed = 0, 0, 0
endif


[TextureOverrideNahidaExtra]
hash = 9b13c166
;hash = 8b268d05
match_first_index = 76875
ib = null
ps-t0 = ResourceNahidaExtraNormalMap
ps-t1 = ResourceNahidaExtraDiffuse
ps-t2 = ResourceNahidaExtraLightMap
if $base == 1
  drawindexed = 0, 0, 0
endif
if $thighHighs == 1
  drawindexed = 0, 0, 0
endif
if $hood == 1
  drawindexed = 0, 0, 0
endif
if $earsD == 1
  drawindexed = 0, 0, 0
endif
if $headH == 1
  drawindexed = 0, 0, 0
endif
if $headD == 1
  drawindexed = 0, 0, 0
endif
if $headNoCrown == 1
  drawindexed = 0, 0, 0
endif


[TextureOverrideNahidaFaceHeadDiffuse]
hash = 895cd4d0
ps-t0 = ResourceNahidaFaceHeadDiffuse


; CommandList -----------------------
[CommandListCreditInfo]
if $creditinfo == 0 && $active == 1
	pre Resource\ShaderFixes\help.ini\Notification = ResourceCreditInfo
	pre run = CustomShader\ShaderFixes\help.ini\FormatText
	pre $\ShaderFixes\help.ini\notification_timeout = time + 5.0
	$creditinfo = 1
endif
; Resources -------------------------

[ResourceNahidaPosition]
type = Buffer
stride = 40
filename = NahidaPosition.buf

[ResourceNahidaBlend]
type = Buffer
stride = 32
filename = NahidaBlend.buf

[ResourceNahidaTexcoord]
type = Buffer
stride = 20
filename = NahidaTexcoord.buf

[ResourceNahidaHeadIB]
type = Buffer
format = DXGI_FORMAT_R32_UINT
filename = NahidaHead.ib

[ResourceNahidaBodyIB]
type = Buffer
format = DXGI_FORMAT_R32_UINT
filename = NahidaBody.ib

[ResourceNahidaDressIB]
type = Buffer
format = DXGI_FORMAT_R32_UINT
filename = NahidaDress.ib

[ResourceNahidaExtraIB]
type = Buffer
format = DXGI_FORMAT_R32_UINT
filename = NahidaExtra.ib

[ResourceNahidaHeadNormalMap]
filename = NahidaHeadNormalMap.dds

[ResourceNahidaHeadDiffuse]
filename = NahidaHeadDiffuse.dds

[ResourceNahidaHeadLightMap]
filename = NahidaHeadLightMap.dds

[ResourceNahidaBodyNormalMap]
filename = NahidaBodyNormalMap.dds

[ResourceNahidaBodyDiffuse]
filename = NahidaBodyDiffuse.dds

[ResourceNahidaBodyLightMap]
filename = NahidaBodyLightMap.dds

[ResourceNahidaDressNormalMap]
filename = NahidaDressNormalMap.dds

[ResourceNahidaDressDiffuse]
filename = NahidaDressDiffuse.dds

[ResourceNahidaDressLightMap]
filename = NahidaDressLightMap.dds

[ResourceNahidaExtraNormalMap]
filename = NahidaExtraNormalMap.dds

[ResourceNahidaExtraDiffuse]
filename = NahidaExtraDiffuse.dds

[ResourceNahidaExtraLightMap]
filename = NahidaExtraLightMap.dds

[ResourceNahidaFaceHeadDiffuse]
filename = NahidaFaceHeadDiffuse.dds

[ResourceCreditInfo]
type = Buffer
data = "created by arakayaya"

; .ini generated by GIMI (Genshin-Impact-Model-Importer)
; If you have any issues or find any bugs, please open a ticket at https://github.com/SilentNightSound/GI-Model-Importer/issues or contact SilentNightSound#7430 on discord
