import os

import cv2

from src import scan_screen
from src.Enums import EncounterType
from src.poke_tree import PokeTree

base_path = os.path.dirname(os.path.abspath(__file__))
def test_single_encounter_extraction():
    scan_screen.poke_tree = PokeTree('en')
    img = cv2.imread(os.path.join(base_path,"screenshots/en/Ponyta-SINGLE.jpg"))
    encounter = scan_screen.extract_encounter_from_picture(img)

    assert encounter[0] == "Ponyta"
    assert encounter[1] == EncounterType.SINGLE

def test_horde_encounter_extraction():
    scan_screen.poke_tree = PokeTree('en')
    img = cv2.imread(os.path.join(base_path,"screenshots/en/Tentacruel_HORDE.jpg"))
    encounter = scan_screen.extract_encounter_from_picture(img)

    assert encounter[0] == "Tentacruel"
    assert encounter[1] == EncounterType.HORDE