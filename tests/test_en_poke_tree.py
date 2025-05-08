import os

from src.poke_tree import PokeTree


base_path = os.path.dirname(os.path.abspath(__file__))

def test_tree():
    assert os.path.exists(os.path.join(base_path,"../data/localisation_data.json"))
    poke_tree = PokeTree('en')
    pkmns = ['Garchomp','Umbreon','Togekiss','Froslass','Luxray','Pidgeotto','Pidgeot']
    for pkmn in pkmns:
        assert poke_tree.search(pkmn) == pkmn
