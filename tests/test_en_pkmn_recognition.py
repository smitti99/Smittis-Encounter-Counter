import os

import cv2

from src import scan_screen
from src.Enums import EncounterType
from src.poke_tree import PokeTree

base_path = os.path.dirname(os.path.abspath(__file__))
def test_encounter_extraction():
    scan_screen.poke_tree = PokeTree('en')

    img = cv2.imread(os.path.join(base_path, "screenshots/en/Ponyta-SINGLE.jpg"))
    encounter = scan_screen.extract_encounter_from_picture(img)

    assert encounter[0] == "Ponyta"
    assert encounter[1] == EncounterType.SINGLE

    #TODO Double Encounter

    img = cv2.imread(os.path.join(base_path, "screenshots/en/Stunky-SMALL_HORDE.jpg"))
    encounter = scan_screen.extract_encounter_from_picture(img)

    assert encounter[0] == "Stunky"
    assert encounter[1] == EncounterType.SMALL_HORDE


    img = cv2.imread(os.path.join(base_path,"screenshots/en/Tentacruel_HORDE.jpg"))
    encounter = scan_screen.extract_encounter_from_picture(img)

    assert encounter[0] == "Tentacruel"
    assert encounter[1] == EncounterType.HORDE

    img = cv2.imread(os.path.join(base_path, "screenshots/out_of_combat.jpg"))
    encounter = scan_screen.extract_encounter_from_picture(img)

    assert encounter[0] == ""
    assert encounter[1] == EncounterType.NONE

def test_identify_pokemon():
    scan_screen.poke_tree = PokeTree('en')
    assert scan_screen.identify_pkmn("Lucario Lv. 32")== "Lucario"
    assert scan_screen.identify_pkmn("Licario Lv. 32")== ""