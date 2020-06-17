; shift + ESC: kills the app/script
+Escape::
ExitApp
Return

+F1::
ChangePlayerCut(1)
ChangeSelfCut(1)
StartHeist(1)
return

+F2::
ChangePlayerCut(2)
ChangeSelfCut(2)
StartHeist(2)
return

+F3::
ChangePlayerCut(3)
ChangeSelfCut(3)
StartHeist(3)
return


StartHeist(num)
{
	loop, %num%
	{
		PressBtn("Down")
	}
	PressBtn("Down")
	PressBtn("Enter")
}

ChangeSelfCut(num)
{
	PressBtn("Enter")
	loop, %num%
	{
		PressBtn("Right")
		PressBtn("Right")
	}
	PressBtn("Enter")
}

ChangePlayerCut(num)
{
	loop, %num%
	{
		; msgbox, oie
		PressBtn("Enter")
		PressBtn("Left")
		PressBtn("Left")
		PressBtn("Enter")
		PressBtn("Up")
		; sleep 500
	}
}


PressBtn(btn)
{
	min_time := 5
	Switch, btn
	{
		Case "Left":
			Send {Left down}
			Sleep min_time
			Send {Left up}
		Case "Right":
			Send {Right down}
			Sleep min_time
			Send {Right up}
		Case "Up":
			Send {Up down}
			Sleep min_time
			Send {Up up}
		Case "Down":
			Send {Down down}
			Sleep min_time
			Send {Down up}
		Case "Enter":
			Send {Enter down}
			Sleep min_time
			Send {Enter up}
		Case "Tab":
			Send {Tab down}
			Sleep min_time
			Send {Tab up}
		Default:
			; msgbox, nada
	}
}
