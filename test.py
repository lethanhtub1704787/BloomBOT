import os

import cv2
import easyocr
import numpy as np
import pyautogui
from mss import mss

sct = mss()
# LD_code_area = {"top": 825, "left": 0, "width": 300, "height": 885}
LD_code_area = {"top": 825, "left": 0, "width": 300, "height": 58}


def extract_letters(s):
    return "".join(c for c in s if c.isalpha())


def ld_contains(string, substring="Lie Detector"):
    return substring in string


def cut_LD_code(s):
    parts = s.split(":", 1)
    return parts[1].strip() if len(parts) > 1 else ""


def check_ld(ld_image="lie.png", conf=0.6):
    if not os.path.exists(ld_image):
        print("Ảnh LD không tồn tại")
    else:
        return pyautogui.locateOnScreen(ld_image, confidence=conf)


def get_LD_code(ocr_results):
    for bbox, text, conf in ocr_results:
        if ld_contains(text):
            return extract_letters(cut_LD_code(text))


# try:
#     ld_confirm = check_ld()
#     if ld_confirm:
#         pyautogui.click(pyautogui.center(ld_confirm))
# except Exception as e:
#     print(e)
reader = easyocr.Reader(["en"], gpu=True)
img = "ld.png"
image = preprocess_image(img)
# image = cv2.cvtColor(np.array(sct.grab(LD_code_area)), cv2.COLOR_BGRA2BGR)
# cv2.imshow("grab", image)
# cv2.waitKey()
# cv2.destroyAllWindows()
ocr_results = reader.readtext(image)

print(get_LD_code(ocr_results))
