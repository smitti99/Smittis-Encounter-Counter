import json
import os

base_path = os.path.dirname(os.path.abspath(__file__))

class PokeTreeNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word = ""

class PokeTree:

    def __init__(self, lang):
        self.root = PokeTreeNode()
        with open(os.path.join(base_path, '../data/localisation_data.json')) as f:
            data = json.load(f)
        pokes = data[lang]["pokes"]
        for poke in pokes:
            self.insert(poke)

    # Insert word into trie
    def insert(self, word):
        node = self.root
        for char in word:
            node = node.children.setdefault(char, PokeTreeNode())
        node.is_end_of_word = True
        node.word = word

    # Search if word exists
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return node.word
            node = node.children[char]
        return node.word
