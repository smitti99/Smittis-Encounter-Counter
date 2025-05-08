import mss
from PIL import Image
#[[288, 784], [1631, 73]]
capture_area = {
    "top": 73,
    "left": 288,
    "width": 1400,
    "height": 200
}

with mss.mss() as sct:
    screenshot = sct.grab(capture_area)
    img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
    img.save("screenshot.jpg")