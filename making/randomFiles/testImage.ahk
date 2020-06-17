#NoEnv
#SingleInstance Force
SetTitleMatchMode 2

;;Variables

SetWorkingDir, cuts
image1	:= "clone.jpg"
image2	:= "components.jpg"
image3	:= "decyphered.jpg"
return

F3::
	CoordMode, Pixel, Window
	index	:= 1
	SetTimer, SearchIt, On
return

SearchIt:
	index	:= ((index > 3) ? index++ : 0)
	ImageSearch, FoundX, FoundY, 0, 0, % A_ScreenWidth, % A_ScreenHeight, % "*80 " image%index%  ;;imagesearch using the image variable containing the image file    location

	MsgBox, 49, Continue?, %image% at %FoundX%x%FoundY%.`nPress OK to continue.  ;;message to test if its working
	IfMsgBox, Cancel
		SetTimer, SearchIt, Off
return



F5::
Loop
{
    CoordMode, Pixel, Window
    ImageSearch, FoundX, FoundY, 0, 0, % A_ScreenWidth, % A_ScreenHeight, *80 %image3%
    Sleep, 25
}
Until ErrorLevel = 0
If ErrorLevel = 0
{
    MsgBox, %image% at %FoundX%x%FoundY%.
}
