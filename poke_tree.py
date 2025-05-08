import json

class PokeTreeNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word = ""

class PokeTree:

    def __init__(self, lang):
        self.root = PokeTreeNode()
        with open('localisation_data.json') as f:
            data = json.load(f)
        pokes = data[lang]["pokes"]
        for poke in pokes:
            self.insert(poke)
        #self.compress()

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

    def compress(self):
        def compress_node(node):
            while len(node.children) == 1 and not node.is_end_of_word:
                (child_char, child_node) = next(iter(node.children.items()))
                # Merge the child node into current node
                node_char_list.append(child_char)
                node.children = child_node.children
                node.is_end_of_word = child_node.is_end_of_word
                node.word = child_node.word
            for child in node.children.values():
                compress_node(child)

        node_char_list = []
        compress_node(self.root)
        return node_char_list

if __name__ == "__main__":
    tree = PokeTree("en")
    print(tree.search("Pidgeotto"))
    print(tree.search("Pidgeot"))