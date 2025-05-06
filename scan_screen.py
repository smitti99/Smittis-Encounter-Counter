import mss
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
import Enums
import settings

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

battle_window = None

def identify_pkmn(poke_lv_str):
    name = settings.global_settings.poke_tree.search(poke_lv_str)
    if name in poke_lv_str:
        return name
    return ""


def horde_pic():
    with mss.mss() as sct:
        screenshot = sct.grab(horde_capture_area)
        # In ein PIL-Bild umwandeln (damit du es weiterverwenden kannst)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img_np = np.array(img)
        # Zum Testen speichern
        ocr = PaddleOCR(use_angle_cls=True, lang=global_settings.global_settings["lang"])  # 'de' für Deutsch
        return (ocr.ocr(img_np, cls=True))


def single_pic():
    with mss.mss() as sct:
        screenshot = sct.grab(single_capture_area)
        # In ein PIL-Bild umwandeln (damit du es weiterverwenden kannst)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img_np = np.array(img)
        # Zum Testen speichern
        ocr = PaddleOCR(use_angle_cls=True, lang=global_settings.global_settings["lang"])  # 'de' für Deutsch
        return (ocr.ocr(img_np, cls=True))

def battle_window_pic():
    with mss.mss() as sct:
        screenshot = sct.grab(battle_window)
        # In ein PIL-Bild umwandeln (damit du es weiterverwenden kannst)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img_np = np.array(img)
        # Zum Testen speichern
        ocr = PaddleOCR(use_angle_cls=True, lang=global_settings.global_settings["lang"])  # 'de' für Deutsch
        raw_text = (ocr.ocr(img_np, cls=True))
        if raw_text[0] is None:
            return "",Enums.EncounterType.NONE
        poke_strings = []
        for text_block in raw_text[0]:
            poke_str = text_block[1][0]
            if "Lv" in poke_str:
                poke_strings.append(poke_str.replace(" ", ""))
        pokes_in_view = {}
        for poke in poke_strings:
            poke_name= identify_pkmn(poke)
            if poke_name in pokes_in_view:
                pokes_in_view[poke_name] += 1
            else:
                pokes_in_view.update({poke_name:1})
        num_pokes_in_view = np.sum(np.fromiter(pokes_in_view.values(),int))
        if num_pokes_in_view == 1:
            return next(iter(pokes_in_view.keys())), Enums.EncounterType.SINGLE
        if num_pokes_in_view == 5:
            return next(iter(pokes_in_view.keys())), Enums.EncounterType.HORDE
        return "",Enums.EncounterType.NONE


def get_encounter():
        global battle_window
        if global_settings.global_settings["battle_box"] is not None:
            box = global_settings.global_settings["battle_box"]
            battle_window = {"top": box[1][1], "left": box[0][0], "height": int((box[0][1] - box[1][1]) / 3.0),
             "width": box[1][0] - box[0][0]}
            return battle_window_pic()

        # Screenshot des definierten Bereichs
        results = horde_pic()
        encounter_type = Enums.EncounterType.HORDE
        if results[0] is None:
            results = single_pic()
            encounter_type = Enums.EncounterType.SINGLE
            if results[0] is None:
                return "None", Enums.EncounterType.NONE


        return results[0][0][1][0], encounter_type