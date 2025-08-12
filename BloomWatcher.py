import datetime
import os
import sys
import time

import cv2
import easyocr
import keyboard
import numpy as np
import pyautogui
from mss import mss
from ultralytics import YOLO

import Function

width, height = pyautogui.size()

# # Khởi tạo mô hình YOLOv11
# model = YOLO("best.pt")

# Load OCR model
reader = easyocr.Reader(["en"], gpu=True)
# Thiết lập vùng chụp màn hình (toàn màn hình)
monitor = {"top": 0, "left": 0, "width": width, "height": height}
LD_code_area = {"top": 825, "left": 0, "width": 300, "height": 58}
sct = mss()
exit_flag = False
pause_flag = False


def exit_program():
    global exit_flag
    print("🛑 Đã nhấn F5 — chương trình sẽ thoát.")
    exit_flag = True
    sys.exit()


def pause_program():
    global pause_flag
    pause_flag = not pause_flag
    if pause_flag == True:
        print("Chương trình tạm dừng!")
    else:
        print("Chương trình đã tiếp tục!")


keyboard.add_hotkey("f5", exit_program)
keyboard.add_hotkey("pause", pause_program)

# LD_attempt = 1
# last_LD_time = time.time()
player_chat_time = time.time()
while not exit_flag:
    # while pause_flag:
    #     if exit_flag:
    #         sys.exit()
    #     time.sleep(1)

    # if time.time() - last_LD_time > 600:
    #     LD_attempt = 1

    # 1 LD CHECKING
    try:
        ld_confirm = Function.check_ld()
        if ld_confirm:
            print("Đã phát hiện LD!")
            # Dừng bot
            Function.toggle_bot()
            # Gửi notify
            Function.send_msg(
                f"{Function.Constant.window_title}, {Function.Constant.character_name}: Lie Code Detected"  # send LD notify
            )
            image = np.array(sct.grab(LD_code_area))
            ocr_results = reader.readtext(image)
            text = Function.get_LD_code(ocr_results)
            print("LD code: " + text)
            pyautogui.click(pyautogui.center(ld_confirm))
            time.sleep(0.5)
            keyboard.write(text)
            Function.call_me()
            sys.exit()
    except Exception as e:
        print(e)

    # 1 CHECK IF GAME IS OFFLINE
    # if Function.check_is_online() == False:
    #     Function.send_msg(
    #         f"{Function.Constant.window_title}, {Function.Constant.character_name}: Offline"
    #     )
    #     sys.exit()
    #     # Function.Terminate_all()

    # # 2 CHECK IF SOMEONE CHAT TO ME:
    # if Function.is_someone_chat() == True and time.time() - player_chat_time > 120:
    #     print("Phát hiện player chat")
    #     Function.send_msg(
    #         f"{Function.Constant.window_title}, {Function.Constant.character_name}: Someone chat"
    #     )
    #     player_chat_time = time.time()
    # # reply?
    # Chuyển từ BGRA sang BGR (loại bỏ kênh alpha)
    time.sleep(1)

print("✅ Đã kết thúc.")
