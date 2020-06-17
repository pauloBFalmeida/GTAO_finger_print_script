SetTimer Click, 100

; shift + ESC: kills the app/script
+Escape::
ExitApp
Return

; Shift + F2: toggle pressing mouse button 1
+F2::Toggle := !Toggle
Click:
    If (!Toggle)
        Return
    Click
return
