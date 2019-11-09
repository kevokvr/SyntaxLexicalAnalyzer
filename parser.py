# CS3210 - Principles of Programming Languages - Fall 2019
# A Syntax Analyzer for an expression
#Carlos Olivas
#Kevin Valenzuela
#Project 1
#09/29/2019

from tree import Tree
from lex import lex
import sys

# reads the given input and returns the grammar as a list of productions
def loadGrammar(input):
    grammar = []
    for line in input:
        grammar.append(line.strip())
    if grammar:
        return grammar
    else:
        raise Exception(errorMessage(4))

# returns the LHS (left hand side) of a given production
def getLHS(production):
    return production.split("->")[0].strip()

# returns the RHS (right hand side) of a given production
def getRHS(production):
    return production.split("->")[1].strip().split(" ")

# prints the productions of a given grammar, one per line
def printGrammar(grammar):
    i = 0
    for production in grammar:
        print(str(i) + ". " + getLHS(production), end = " -> ")
        print(getRHS(production))
        i += 1

# reads the given input containing an SLR parsing table and returns the "actions" and "gotos" as dictionaries
def loadTable(input):
    actions = {}
    gotos = {}
    header = input.readline().strip().split(",")
    end = header.index("$")
    tokens = []
    for field in header[1:end + 1]:
        tokens.append(field)
        # tokens.append(int(field))
    variables = header[end + 1:]
    for line in input:
        row = line.strip().split(",")
        state = int(row[0])
        for i in range(len(tokens)):
            token = tokens[i]
            key = (state, token)
            value = row[i + 1]
            if len(value) == 0:
                value = None
            actions[key] = value
        for i in range(len(variables)):
            variable = variables[i]
            key = (state, variable)
            value = row[i + len(tokens) + 1]
            if len(value) == 0:
                value = None
            gotos[key] = value
    if actions and gotos:
        return actions, gotos
    else:
        raise Exception(errorMessage(5))


# prints the given actions, one per line
def printActions(actions):
    for key in actions:
        print(key, end = " -> ")
        print(actions[key])

# prints the given gotos, one per line
def printGotos(gotos):
    for key in gotos:
        print(key, end = " -> ")
        print(gotos[key])

# given an input (source program), grammar, actions, and gotos, returns true/false depending whether the input should be accepted or not
def parse(code, grammar, actions, gotos):

    # TODOd #1: create a list of trees
    trees = []

    input = []
    code, lexeme, token = lex(code)
    newtoken = str(token)
    input.append(newtoken[6:])

    stack = []
    stack.append(0)
    while True:
        if not input[0]:
            input.pop()
            input.append("$")
            token = "$"
        else:
            token = str(input[0])
        print("stack: ", end = "")
        print(stack, end = " ")
        print("input: ", end = "")
        print(input, end = " ")
        state = stack[-1]
        action = actions[(state, token)]
        print("action: ", end = "")
        print(action)

        if action is None:
            if state == 1:
                raise Exception(errorMessage(7))
            elif state <= 2:
                raise Exception(errorMessage(8))
            elif state == 10:
                raise Exception(errorMessage(6))
            elif state == 32:
                raise Exception(errorMessage(11))
            elif state >= 22 or state >= 40:
                raise Exception(errorMessage(9))
            elif state > 45:
                raise Exception(errorMessage(10))
            return None  # tree building update


        # shift operation , fix for two digits
        if action[0] == 's':
            input.pop(0)
            stack.append(token)
            code, lexeme, token = lex(code)
            newtoken = str(token)
            input.append(newtoken[6:])
            if len(action) > 2:
                ok = int(action[1:3])
                state = ok
            else:
                state = int(action[1])
            stack.append(state)

            # TODOd #2: create a new tree, set data to token, and append it to the list of trees
            tree = Tree()
            tree.data = token
            trees.append(tree)

        # reduce operation
        elif action[0] == 'r':
            if len(action) > 2:
                production = grammar[int(action[1:3])]
            else:
                production = grammar[int(action[1])]
            lhs = getLHS(production)
            rhs = getRHS(production)
            for i in range(len(rhs) * 2):
                stack.pop()
            state = stack[-1]
            stack.append(lhs)
            stack.append(int(gotos[(state, lhs)]))

            # TODOd #3: create a new tree and set data to lhs
            newTree = Tree()
            newTree.data = lhs

            # TODOd #4: get "len(rhs)" trees from the right of the list of trees and add each of them as child of the new tree you created, preserving the left-right order
            for tree in trees[-len(rhs):]:
                newTree.add(tree)

            # TODOd #5: remove "len(rhs)" trees from the right of the list of trees
            trees = trees[:-len(rhs)]

            # TODOd #6: append the new tree to the list of trees
            trees.append(newTree)

        # not a shift or reduce operation, must be an "accept" operation
        else:
            production = grammar[0]
            lhs = getLHS(production)
            rhs = getRHS(production)

            # TODOd #7: same as reduce but using the 1st rule of the grammar
            root = Tree()
            root.data = lhs
            for tree in trees:
                root.add(tree)

            # TODOd #8: return the new tree
            return root


def errorMessage(code):
    msg = "Error " + str(code).zfill(2) + ": "
    if code == 1:
        return msg + "source file missing"
    # -------------------- done
    if code == 2:
        return msg + "couldn't open source file"
    # --------------------- done
    if code == 3:
        return msg + "lexical error"
    # ---------------------
    if code == 4:
        return msg + "couldn't open grammar file"
    # ----------------------- done
    if code == 5:
        return msg + "couldn't open SLR table file"
    # -------------------- done
    if code == 6:
        return msg + "EOF expected"
    # ---------------
    if code == 7:
        return msg + "identifier expected"
    # ------------------
    if code == 8:
        return msg + "special word missing"
    # --------------------
    if code == 9:
        return msg + "symbol missing"
    # -----------------------
    if code == 10:
        return msg + "data type expected"
    # ----------------------
    if code == 11:
        return msg + "identifier or literal value expected"
    return msg + "syntax error"

# main
if __name__ == "__main__":

    input = open("grammar.txt", "rt")
    grammar = loadGrammar(input)
    input.close()

    input = open("slr_table.csv", "rt")
    actions, gotos = loadTable(input)
    input.close()

    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise Exception(errorMessage(1))
    source = open(sys.argv[1], "rt")
    if not source:
        raise Exception(errorMessage(2))
    code = source.read()
    source.close()

    # tree building update
    tree = parse(code, grammar, actions, gotos)
    if tree:
        print("Input is syntactically correct!")
        print("Parse Tree:")
        tree.print()
    else:
        raise Exception(errorMessage(99))
