
#include <ActionFunc.au3>
#include <MsgBoxConstants.au3>
#include <Date.au3>
#RequireAdmin

; Press Esc to terminate script, Pause/Break to "pause"

Global $g_bPaused = False
Global $x1,$y1,$x2,$y2,$x3,$y3,$x4,$y4,$x5,$y5
Global $watcher = ShellExecute("BloomWatcher.py","","","",@SW_MINIMIZE)
HotKeySet("{PAUSE}", "TogglePause")
HotKeySet("{F6}", "SelfTogglePause")
HotKeySet("{F5}", "Terminate")
HotKeySet("{F4}", "showLocation")
HotKeySet("{F3}", "test")
HotKeySet("{F2}", "play")
HotKeySet("{F1}", "high_jump")
HotKeySet("+!d", "ShowMessage") ; Shift-Alt-d


Func TogglePause()
    $g_bPaused = Not $g_bPaused
    While $g_bPaused
        Sleep(100)
        ToolTip('BOT is "Paused"', 0, 0)
    WEnd
    ToolTip("")
EndFunc   ;==>TogglePause

Func SelfTogglePause()
	$g_bPaused = Not $g_bPaused
    While $g_bPaused
        Sleep(100)
        ToolTip('BOT is "Paused"', 0, 0)
    WEnd
    ToolTip("")
EndFunc

Func SelfTerminate()
    Exit
EndFunc   ;==>Terminate

Func Terminate()
 	ProcessClose($watcher)
    Exit
EndFunc   ;==>Terminate

Func ShowMessage()
    MsgBox($MB_SYSTEMMODAL, "", "This is a message.")
EndFunc   ;==>ShowMessage

;~ Func test()
;~ 	$runeLocation = runeLocation()
;~ 	If IsArray($runeLocation) Then
;~ 		go_to($runelocation[0],$runelocation[1],"jump")
;~ 	EndIf
;~ EndFunc

Func test()
	high_jump()
EndFunc

Func buff()
	Send("{PGUP}")
	Sleep(3000)
EndFunc

Func buff2()
	Send("1")
	Sleep(1000)
EndFunc

Func buff3()
	Send("2")
	Sleep(1500)
	Send("3")
	Sleep(1000)
	Send("4")
EndFunc
ToolTip("Bag here",1115, 170)
While 1
	Sleep(100)
WEnd

Func play()
	Local $x, $y
	Local $left_x = 27, $left_y = 107
	Local $right_x = 124, $right_y = 107
	$attack_direct = "left"
	buff()
	buff2()
	buff3()
	$buff = TimerInit()
	$buff2 = TimerInit()
	$buff3 = TimerInit()
	Sleep(1000)
	While 1
		$box = PixelSearch($left_x, $left_y-3,$right_x, $right_y+3,$charColor)
		$left = PixelSearch($left_x, $left_y-3,$left_x+10, $left_y+3,$charColor)
		$right = PixelSearch($right_x-10, $right_y-3,$right_x, $right_y+3,$charColor)
		$full_equip = _ImageSearchArea(@ScriptDir&'\images\empty_equip.bmp',1,1229, 394,1262, 427,$x,$y,10,10)
		If IsArray($left) And $attack_direct = "left" Then
			$attack_direct = "right"
		EndIf

		If IsArray($right) And $attack_direct = "right" Then
			$attack_direct = "left"
		EndIf
		Select
			Case Not IsArray($box)
				ToolTip("Returning box",0,0)
				go_to($right_x,$right_y,"flash")
			Case $full_equip == 0
				Sleep(1000)
				sell_equip()

			Case TimerDiff($buff) > 190000
				Sleep(1000)
				buff()
				$buff = TimerInit()

			Case TimerDiff($buff2) > 590000
				Sleep(1500)
				buff2()
				$buff2 = TimerInit()

			Case TimerDiff($buff3) > 290000
				Sleep(1000)
				buff3()
				$buff3 = TimerInit()

			Case $attack_direct == "left"
				left_hit()

			Case $attack_direct == "right"
				right_hit()
		EndSelect
		Sleep(100)
	WEnd
EndFunc
