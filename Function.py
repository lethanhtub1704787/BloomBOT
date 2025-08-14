import datetime
import io
import os

import cv2
import easyocr
import keyboard
import mss
import numpy as np
import pyautogui
import pygetwindow as gw
import requests
from PIL import Image

import Constant


def Terminate_all():
    keyboard.press_and_release("f5")


def toggle_bot():
    keyboard.press_and_release("F6")




def ld_contains(string: str, substring="Lie Detector"):
    return str(substring) in str(string)


def cut_LD_code(s):
    s = str(s)
    parts = s.split(":", 1)
    return str(parts[1].strip()) if len(parts) > 1 else ""


def extract_letters(s):
    s = str(s)
    return str("".join(c for c in s if c.isalpha()))

def check_ld(ld_image="lie.png", conf=0.7):
    if not os.path.exists(ld_image):
        print("Ảnh LD không tồn tại")
    else:
        return pyautogui.locateOnScreen(ld_image, confidence=conf)


def get_LD_code(ocr_results):
    for bbox, text, conf in ocr_results:
        if ld_contains(text):
            return extract_letters(cut_LD_code(text))


def check_is_online():
    window_title = Constant.window_title
    if window_title in gw.getAllTitles():
        return True
    else:
        return False


def is_someone_chat():
    check = pixel_search_region()
    if isinstance(check, tuple):
        return True
    return False
    # window_title = Constant.window_title
    # if window_title in gw.getAllTitles():
    #     return True
    # else:
    #     return False


def is_someone_wanna_join():
    return False
    # window_title = Constant.window_title
    # if window_title in gw.getAllTitles():
    #     return True
    # else:
    #     return False


def hex_to_rgb(hex_color):
    if isinstance(hex_color, str):
        hex_color = int(hex_color, 16)
    r = (hex_color >> 16) & 0xFF
    g = (hex_color >> 8) & 0xFF
    b = hex_color & 0xFF
    return (r, g, b)


def pixel_search_region(
    target_color=Constant.chat_color,
    x1=Constant.chat_check_position[0],
    y1=Constant.chat_check_position[1],
    x2=Constant.chat_check_position[2],
    y2=Constant.chat_check_position[3],
    tolerance=0,
):
    target_color = hex_to_rgb(target_color)

    def is_similar(c1, c2, tol):
        return all(abs(a - b) <= tol for a, b in zip(c1, c2))

    with mss.mss() as sct:
        monitor = {"left": x1, "top": y1, "width": x2 - x1, "height": y2 - y1}
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        width, height = img.size
        pixels = img.load()

        for y in range(height):
            for x in range(width):
                color = pixels[x, y]
                if tolerance == 0:
                    if color == target_color:
                        return (
                            x + x1,
                            y + y1,
                        )  # cộng lại để ra vị trí thật trên màn hình
                else:
                    if is_similar(color, target_color, tolerance):
                        return (x + x1, y + y1)
    return None


def save_LD():
    # Tên thư mục lưu ảnh
    folder_name = "LD_collection"

    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"📁 Đã tạo thư mục: {folder_name}")

    # Chụp màn hình
    screenshot = pyautogui.screenshot()

    # Tạo tên file theo thời gian
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(folder_name, filename)

    # Lưu ảnh
    screenshot.save(filepath)
    print(f"✅ Ảnh đã lưu vào: {filepath}")


def save_Predicted(image):
    # Tên thư mục lưu ảnh
    folder_name = "Predicted_collection"

    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"📁 Đã tạo thư mục: {folder_name}")

    # Tạo tên file theo thời gian
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = f"predicted_{timestamp}.png"
    filepath = os.path.join(folder_name, filename)
    # Lưu ảnh đã annotate
    cv2.imwrite(filepath, image)


def crop_and_show(image, start_point, end_point, window_name="Cropped"):
    """
    Cắt ảnh từ tọa độ đã xác định và hiển thị.

    Params:
        image (numpy.ndarray): ảnh đầu vào (ví dụ ảnh từ YOLO hoặc màn hình)
        start_point (tuple): (x1, y1) — góc trên bên trái
        end_point (tuple): (x2, y2) — góc dưới bên phải
        window_name (str): tên cửa sổ hiển thị
    """
    x1, y1 = int(start_point[0]), int(start_point[1])
    x2, y2 = int(end_point[0]), int(end_point[1])

    cropped = image[y1:y2, x1:x2]

    cv2.imshow(window_name, cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def crop_this(screen_shot, start_point, end_point):
    """
    Cắt vùng ảnh trực tiếp từ biến screen_shot (numpy array).

    Params:
        screen_shot (numpy.ndarray): ảnh đã chụp từ màn hình
        start_point (tuple): (x1, y1)
        end_point (tuple): (x2, y2)

    Returns:
        cropped_image (numpy.ndarray): vùng ảnh đã cắt
    """
    x1, y1 = start_point
    x2, y2 = end_point
    cropped_image = screen_shot[int(y1) : int(y2), int(x1) : int(x2)]
    return cropped_image


def blend_numpy_images(np_images, alpha=0.2):
    # Chuyển ảnh đầu tiên sang PIL
    base = Image.fromarray(np_images[0], mode="RGBA")

    for arr in np_images[1:]:
        img = Image.fromarray(arr, mode="RGBA")
        base = Image.blend(base, img, alpha)

    base.save("overlayed2.png")

    return base


def print_ocr_this(image):
    reader = easyocr.Reader(["en"], gpu=True)
    results = reader.readtext(image)
    for bbox, text, confidence in results:
        print(f"📝 LD Code: {text}")
        print(f"🔎 Độ tin cậy: {confidence:.2f}")


def overlay(folder, alpha=0.2):
    # folder name is a timestamp created by the time screenshot and crop image
    path = "LD_code_collection/"
    full_path = path + folder + "/"
    image_list = os.listdir(full_path)
    fisrt_image = full_path + image_list[0]
    # print(fisrt_image)
    final = Image.open(fisrt_image)

    for image_name in image_list:
        overlay = Image.open(full_path + image_name)
        overlay = overlay.convert("RGBA")
        final = Image.blend(final, overlay, alpha)
    # return final
    final.save(f"{full_path}/final.png", "PNG")


def call_me():
    id = "@tonyle172"
    url = f"https://api.callmebot.com/start.php?source=web&user={id}&text=Lie%20Detected&lang=en-US-Standard-B"
    x = requests.get(url)


def send_msg(text):
    token = Constant.token
    chat_id = Constant.chat_id
    url_req = (
        f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
    )
    requests.get(url_req)


def send_image(np_image):
    # Chuyển thành ảnh bằng Pillow
    image = Image.fromarray(np_image)
    # Lưu ảnh vào buffer để gửi mà không cần ghi ra file
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    token = Constant.token
    chat_id = Constant.chat_id
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    files = {"photo": buffer}
    data = {"chat_id": chat_id}

    response = requests.post(url, files=files, data=data)


def save_LD_code(timestamp, image, index):
    # Tên thư mục lưu ảnh
    folder_name = "LD_code_collection"

    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"📁 Đã tạo thư mục: {folder_name}")

    folder_name = folder_name + "/" + timestamp
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"📁 Đã tạo thư mục: {folder_name}")

    # Tạo tên file theo thời gian

    filename = f"{folder_name}/screenshot_{index}.png"
    # Lưu ảnh
    cv2.imwrite(filename, image)
    print(f"✅ Ảnh đã lưu vào: {filename}")
