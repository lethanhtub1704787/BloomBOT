#include <ScreenCapture.au3>
#include <VariableSet.au3>
#include <ImageSearch.au3>
#RequireAdmin

Func myLocation()
	$MyLocation = PixelSearch(9, 50,255, 165,0xFFDD44)
	If IsArray($MyLocation) Then
		Return $MyLocation
	EndIf
EndFunc

Func showLocation()
	$MyLocation = myLocation()
	If IsArray($MyLocation) Then
 		MsgBox("","",$MyLocation[0]&","&$MyLocation[1])
		Return $MyLocation
	EndIf
EndFunc

Func jump()
	Send("c")
EndFunc

Func attack()
	Send("x")
EndFunc

Func jump_down()
	Send("{DOWN down}")
	Send("{c 3}")
	Send("{DOWN up}")
EndFunc

Func down_flash()
	Send("{DOWN down}")
	teleport()
	Send("{DOWN up}")
EndFunc

Func left_flash()
	Send("{LEFT down}")
	teleport()
	Send("{LEFT up}")
EndFunc

Func right_flash()
	Send("{RIGHT down}")
	teleport()
	Send("{RIGHT up}")
EndFunc

Func teleport()
	Send("d")
EndFunc

Func move_left()
	Send("{LEFT down}")
EndFunc

Func move_right()
	Send("{RIGHT down}")
EndFunc

Func release_right()
	Send("{RIGHT up}")
EndFunc

Func release_left()
	Send("{LEFT up}")
EndFunc

Func release_all()
	Send("{LEFT up}")
	Send("{RIGHT up}")
EndFunc

Func sell_equip()
	Send("{ENTER}")
	Sleep(300)
	Send("@sell eq 1 100")
	Sleep(300)
	Send("{ENTER}")
	Sleep(100)
	Send("{ENTER}")
EndFunc

Func right_hit()
	right_flash()
	attack()
EndFunc

Func left_hit()
	left_flash()
	attack()
EndFunc

Func high_jump()
	jump()
	Send("{UP down}")
	Sleep(200)
	teleport()
	Sleep(100)
	Send("{UP up}")
EndFunc


Func turn_right()
	Send("{RIGHT down}")
	Sleep(100)
	Send("{RIGHT up}")
EndFunc

Func turn_left()
	Send("{LEFT down}")
	Sleep(100)
	Send("{LEFT up}")
EndFunc

Func go_to($x,$y,$move_type,$demon=False)
	ToolTip("",0,0,"Coming to rune")
	$x1_box = $x - 1
	$y1_box = $y - 3
	$x2_box = $x + 1
	$y2_box = $y + 3

	$time = TimerInit()
	While 1
		$myLocation = myLocation()
		If Not IsArray($myLocation) Then
			Return
		EndIf
		$check_box = PixelSearch( $x1_box,  $y1_box, $x2_box, $y2_box,0xFFDD44)
		Select
			Case TimerDiff($time) > 10000
				down_flash()
				Sleep(1000)
				move_right()
				Sleep(300)
				release_all()
				$time = TimerInit()
				Sleep(1000)

			Case IsArray($check_box)
				release_all()
				Sleep(100)
				$check_box = PixelSearch( $x1_box,  $y1_box, $x2_box, $y2_box,0xFFDD44)
				If Not IsArray($check_box) Then
					ContinueLoop
				EndIf
				ExitLoop

			Case $myLocation[0] < $x1_box
				release_left()
				If $x1_box - $myLocation[0] >= 25 Then
					right_flash()
				Else
					move_right()
				EndIf

			Case $myLocation[0] > $x2_box
				release_right()
				If $myLocation[0] - $x2_box >= 25 Then
					left_flash()
				Else
					move_left()
				EndIf

			Case $myLocation[1] < $y1_box
				release_all()
				jump_down()
				Sleep(300)
				down_flash()
				Sleep(400)

			Case $myLocation[1] > $y2_box
				release_all()
				Sleep(200)
				high_jump()
				Sleep(100)
		EndSelect
		Sleep(100)
	WEnd
EndFunc



