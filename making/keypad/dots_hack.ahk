+F2::
RunWait python answerKey.py
sleep 1500
loop, read, answers_dots.txt
{
	sleep 300
	pressBtn(A_LoopReadLine)
}
PressBtn("Tab")

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
			Sleep 1600
		Case "Tab":
			Send {Tab down}
			Sleep hold
			Send {Tab up}
	}
}
