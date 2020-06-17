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
		Case "w":
			Send {w down}
			Sleep hold
			Send {w up}
		Case "a":
			Send {a down}
			Sleep hold
			Send {a up}
		Case "s":
			Send {s down}
			Sleep hold
			Send {s up}
		Case "d":
			Send {d down}
			Sleep hold
			Send {d up}
		Case "q":
			Send {q down}
			Sleep hold
			Send {q up}
		Case "e":
			Send {e down}
			Sleep hold
			Send {e up}
	}
}
