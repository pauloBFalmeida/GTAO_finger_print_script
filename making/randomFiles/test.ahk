; shift + ESC: kills the app/script
+Escape::
ExitApp
Return

; Shift + F1: start hacking finger prints
+F1::
RunWait, python answer.py
Sleep, 200
return

; Shift + F2: start hacking dots
+F2::
run cmd.exe
WinWait, ahk_exe cmd.exe ; Wait for CMD to start
; Send c:{enter} ; Go to C drive
; Send cd C:\python\blog\{enter} ; go to script's folder
Send python answer.py{enter}
return
