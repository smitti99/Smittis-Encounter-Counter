import os

from src.poke_tree import PokeTree


def test_tree():
    assert os.path.exists("../data/localisation_data.json")
    poke_tree = PokeTree('en')
    pkmns = ['Garchomp','Umbreon','Togekiss','Froslass','Luxray','Pidgeotto','Pidgeot']
    for pkmn in pkmns:
        assert poke_tree.search(pkmn) == pkmn
