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
RunWait answer.exe 1
sleep 100
loop, read, answers_finger.txt
{
	sleep 25
	pressBtn(A_LoopReadLine)
}
PressBtn("Tab")
return

; Shift + F2: start hacking dots
+F2::
setworkingDir, answer
RunWait answer.exe 2
sleep 2000
loop, read, answers_dots.txt
{
	sleep 200
	line := A_LoopReadLine
	pressBtn(line)
	if line contains Enter
		Sleep 2000
}
PressBtn("Tab")
return



; press the key on keyboard
PressBtn(btn, hold:=10)
{
	Switch, btn
	{
		Case "Left":
			Send {Left down}
			Sleep hold
			Send {Left up}
		Case "Right":
			Send {Right down}
			Sleep hold
			Send {Right up}
		Case "Up":
			Send {Up down}
			Sleep hold
			Send {Up up}
		Case "Down":
			Send {Down down}
			Sleep hold
			Send {Down up}
		Case "Enter":
			Send {Enter down}
			Sleep hold
			Send {Enter up}
		Case "Tab":
			Send {Tab down}
			Sleep hold
			Send {Tab up}
	}
}
