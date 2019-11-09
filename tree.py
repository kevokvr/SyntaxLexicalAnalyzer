# CS3210 - Principles of Programming Languages - Fall 2019
# A tree data-structure
# Author: Thyago tmota
# Date: 09/09/19

class Tree:

    TAB = "   "

    def __init__(self):
        self.data = None
        self.children = []

    def add(self, child):
        self.children.append(child)

    def print(self, tab = ""):
        if self.data != None:
            print(tab + str(self.data))
            tab += Tree.TAB
            for child in self.children:
                if isinstance(child, Tree):
                    child.print(tab)
                else:
                    print(tab + child)

# main
if __name__ == "__main__":

    root = Tree()
    root.data = "term"

    term = Tree()
    term.data = "term"

    factor = Tree()
    factor.data = "factor"

    term.add(factor)
    root.add(term)

    div = Tree()
    div.data = "/"
    root.add(div)

    factor = Tree()
    factor.data = "factor"
    root.add(factor)

    root.print()
