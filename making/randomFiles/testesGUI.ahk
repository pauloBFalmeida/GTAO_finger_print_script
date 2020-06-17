Gui, -caption -Border +alwaysontop
Gui, color,red
Gui, show,w40 h40  x50 y50

OnMessage(0x201,"WM_LBUTTONDOWN")
return

!esc::exitapp

WM_LBUTTONDOWN(wParam,lParam,msg,hwnd){
PostMessage, 0xA1, 2
}
