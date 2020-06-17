#include pressBtn.ahk
SetTimer Click, 100

; shift + ESC: kills the app/script
+Escape::
ExitApp
Return

; Shift + F3: toggle pressing mouse button 1
+F3::Toggle := !Toggle
Click:
    If (!Toggle)
        Return
    Click
return


; Shift + F1: start hacking finger prints
+F1::
setworkingDir, answer
RunWait answer.exe
sleep 100
loop, read, answers.txt
{
	sleep 25
	pressBtn(A_LoopReadLine)
}
PressBtn("Tab")
return

; Shift + F2: start hacking dots
+F2::
return
