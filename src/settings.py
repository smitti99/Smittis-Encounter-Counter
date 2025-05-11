import json
import logging
import os

try:
    from pynput import mouse
except ImportError:
    mouse = None  # Oder eine Mock-Klasse
logger = logging.getLogger("EncounterCounter")
mouse_pos = []
global_settings = {"version": "1.0", "lang": "en", "battle_box": [[288, 784], [1631, 73]], "lvl-str" : "Lv."}

base_path = os.path.dirname(os.path.abspath(__file__))
def load_settings(): # pragma: no cover
    try:
        with open(os.path.join(base_path,'../data/config.json')) as f:
            data = json.load(f)
            global_settings.update(data)
    except FileNotFoundError:
       logger.warning('Config not found. Using default settings')

def save_settings(): # pragma: no cover
    with open(os.path.join(base_path,'../data/config.json', "w")) as f:
        json.dump(global_settings, f)


def on_click(x, y, button, pressed): # pragma: no cover
    if pressed:
        global mouse_pos
        mouse_pos = [x, y]
        return False  # Stop listener after first click
    return None


def set_battle_box(): # pragma: no cover

    with mouse.Listener(on_click=on_click) as listener:
        print("Select bottom left corner of Battle Box")
        listener.join()
    pos1 = mouse_pos
    with mouse.Listener(on_click=on_click) as listener:
        print("Select upper right corner of Battle Box")
        listener.join()
    pos2 = mouse_pos

    if pos1[0] < pos2[0]:
        global_settings.update({"battle_box": [pos1, pos2]})
    else:
        global_settings.update({"battle_box": [pos2, pos1]})

    save_settings()


if __name__ == "__main__": # pragma: no cover
    set_battle_box()
