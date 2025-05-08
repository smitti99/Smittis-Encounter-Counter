import json
from pynput import mouse

from poke_tree import PokeTree

mouse_pos = []
global_settings = {"version": "1.0", "lang": "en", "battle_box": None}

def load_settings():
    global global_settings
    with open('config.json') as f:
        data = json.load(f)
        global_settings.update(data)

def save_settings():
    global global_settings
    with open('config.json', "w") as f:
        json.dump(global_settings, f)


def on_click(x, y, button, pressed):
    if pressed:
        global mouse_pos
        mouse_pos = [x, y]
        return False  # Stop listener after first click
    return None


def set_battle_box():
    global mouse_pos
    global global_settings

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


if __name__ == "__main__":
    set_battle_box()
