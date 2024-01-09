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
