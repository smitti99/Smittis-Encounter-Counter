import mss
from PIL import Image
from paddleocr import PaddleOCR

# Definiere den Bereich, den du capturen willst (x, y, Breite, Höhe)
single_capture_area = {
    "top": 125,  # y
    "left": 290,  # x
    "width": 150,  # Breite
    "height": 20  # Höhe
}

horde_capture_area = {
    "top": 115,  # y
    "left": 570,  # x
    "width": 150,  # Breite
    "height": 20  # Höhe
}

fullscreen = {
    "top": 0,  # y
    "left": 0,  # x
    "width": 1920,  # Breite
    "height": 1080  # Höhe
}



if __name__ == "__main__" :
    with mss.mss() as sct:
        # Screenshot des definierten Bereichs
        screenshot = sct.grab(horde_capture_area)

        # In ein PIL-Bild umwandeln (damit du es weiterverwenden kannst)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        # Zum Testen speichern
        img.save("screenshot.jpg")

        ocr = PaddleOCR(use_angle_cls=True, lang='en')  # 'de' für Deutsch
        results = ocr.ocr('screenshot.jpg', cls=True)

        for line in results[0]:
            for word in line:
                print(f"Gefundener Text: {word[1][0]} (Confidence: {word[1][1]:.2f})")