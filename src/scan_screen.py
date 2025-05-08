import logging

import mss
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
from src import Enums
from src.poke_tree import PokeTree
from settings import global_settings

battle_window = None
poke_tree = PokeTree


def identify_pkmn(poke_lv_str):
    name = poke_tree.search(poke_lv_str)
    if name in poke_lv_str:
        return name
    return ""


def battle_window_pic():
    with mss.mss() as sct:
        screenshot = sct.grab(battle_window)
        # In ein PIL-Bild umwandeln (damit du es weiterverwenden kannst)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img_np = np.array(img)
        # Zum Testen speichern
        ocr = PaddleOCR(use_angle_cls=True, lang=global_settings["lang"])  # 'de' für Deutsch
        raw_text = (ocr.ocr(img_np, cls=True))
        if raw_text[0] is None:
            return "", Enums.EncounterType.NONE
        poke_strings = []
        for text_block in raw_text[0]:
            poke_str = text_block[1][0]
            if "Lv" in poke_str:
                poke_strings.append(poke_str.replace(" ", ""))
        pokes_in_view = {}
        for poke in poke_strings:
            poke_name = identify_pkmn(poke)
            if poke_name in pokes_in_view:
                pokes_in_view[poke_name] += 1
            else:
                pokes_in_view.update({poke_name: 1})
        num_pokes_in_view = np.sum(np.fromiter(pokes_in_view.values(), int))
        if num_pokes_in_view == 1:
            return next(iter(pokes_in_view.keys())), Enums.EncounterType.SINGLE
        if num_pokes_in_view == 3:
            return next(iter(pokes_in_view.keys())), Enums.EncounterType.SMALL_HORDE
        if num_pokes_in_view >= 4:
            return next(iter(pokes_in_view.keys())), Enums.EncounterType.HORDE
        return "", Enums.EncounterType.NONE


def get_encounter():
    global battle_window
    if global_settings["battle_box"] is not None:
        box = global_settings["battle_box"]
        battle_window = {"top": box[1][1], "left": box[0][0], "height": int((box[0][1] - box[1][1]) / 3.0),
                         "width": box[1][0] - box[0][0]}
        return battle_window_pic()
    return "", Enums.EncounterType.NONE


if __name__ == "__main__":
    logging.getLogger('ppocr').setLevel(logging.INFO)
    with mss.mss() as sct:
        bb_min = [0, 0, 0, 0, 0, 0, 0, 0]
        bb_max = [0, 0, 0, 0, 0, 0, 0, 0]
        box = [[288, 784], [1631, 73]]
        for i in range(50):
            screenshot = sct.grab({"top": box[1][1], "left": box[0][0], "height": int((box[0][1] - box[1][1]) / 3.0),
                                   "width": box[1][0] - box[0][0]})
            # In ein PIL-Bild umwandeln (damit du es weiterverwenden kannst)
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            img_np = np.array(img)
            # Zum Testen speichern
            ocr = PaddleOCR(use_angle_cls=True, lang="en")  # 'de' für Deutsch
            raw_text = (ocr.ocr(img_np, cls=True))
            for text_block in raw_text[0]:
                if 'Tentacruel Lv. 40' in text_block[1][0]:
                    bbox = text_block[0]
                    if i == 0:
                        for j in range(8):
                            bb_max[j] = bbox[j // 2][j % 2]
                            bb_min[j] = bbox[j // 2][j % 2]
                    else:
                        for j in range(8):
                            if bb_max[j] < bbox[j // 2][j % 2]:
                                bb_max[j] = bbox[j // 2][j % 2]
                            elif bb_min[j] > bbox[j // 2][j % 2]:
                                bb_min[j] = bbox[j // 2][j % 2]
        print("min" + str(bb_min))
        print("max" + str(bb_max))
