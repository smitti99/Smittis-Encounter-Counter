import mss
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
import Enums

# Definiere den Bereich, den du capturen willst (x, y, Breite, Höhe)
single_capture_area = {
    "top": 125,  # y
    "left": 290,  # x
    "width": 150,  # Breite
    "height": 30  # Höhe
}

horde_capture_area = {
    "top": 115,  # y
    "left": 570,  # x
    "width": 150,  # Breite
    "height": 30  # Höhe
}

fullscreen = {
    "top": 0,  # y
    "left": 0,  # x
    "width": 1920,  # Breite
    "height": 1080  # Höhe
}

battle_window = {
    "top": 25,  # y
    "left": 200,  # x
    "width": 1200,  # Breite
    "height": 250  # Höhe
}


def horde_pic():
    with mss.mss() as sct:
        screenshot = sct.grab(battle_window)
        # In ein PIL-Bild umwandeln (damit du es weiterverwenden kannst)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img_np = np.array(img)
        # Zum Testen speichern
        ocr = PaddleOCR(use_angle_cls=True, lang='en')  # 'de' für Deutsch
        return (ocr.ocr(img_np, cls=True))


def single_pic():
    with mss.mss() as sct:
        screenshot = sct.grab(single_capture_area)
        # In ein PIL-Bild umwandeln (damit du es weiterverwenden kannst)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img_np = np.array(img)
        # Zum Testen speichern
        ocr = PaddleOCR(use_angle_cls=True, lang='en')  # 'de' für Deutsch
        return (ocr.ocr(img_np, cls=True))



def get_encounter():

        # Screenshot des definierten Bereichs
        results = horde_pic()
        encounter_type = Enums.EncounterType.HORDE
        if results[0] is None:
            results = single_pic()
            encounter_type = Enums.EncounterType.SINGLE
            if results[0] is None:
                return "None", Enums.EncounterType.NONE


        return results[0][0][1][0], encounter_type