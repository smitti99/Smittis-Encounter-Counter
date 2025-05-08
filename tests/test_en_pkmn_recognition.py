from src import scan_screen
from src.Enums import EncounterType
from src.poke_tree import PokeTree


def test_encounter_extraction():
    scan_screen.poke_tree = PokeTree('en')
    encounter = scan_screen.extract_encounter_from_picture("screenshots/en/Ponyta-SINGLE.jpg")
    assert encounter[0] == "Ponyta"
    assert encounter[1] == EncounterType.SINGLE