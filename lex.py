# CS3210 - Principles of Programming Languages - Fall 2019
# A Lexical Analyzer for an expression
#Carlos Olivas
#Kevin Valenzuela
#Project 1
#09/29/2019

from enum import Enum
import sys

# all char classes
class CharClass(Enum):
    EOF        = 1
    LETTER     = 2
    DIGIT      = 3
    OPERATOR   = 4
    PUNCTUATOR = 5
    QUOTE      = 6
    BLANK      = 7
    OTHER      = 8
    ASSIGNMENT = 9

# reads the next char from input and returns its class
def getChar(input):
    if len(input) == 0:
        return (None, CharClass.EOF)
    c = input[0].lower()
    if c.isalpha():
        return (c, CharClass.LETTER)
    if c.isdigit():
        return (c, CharClass.DIGIT)
    if c == '"':
        return (c, CharClass.QUOTE)
    if c in [':=']:
        return (c,CharClass.ASSIGNMENT)
    if c in ['+', '-', '*', '/', '=','<','<=','>','>=']:
        return (c, CharClass.OPERATOR)
    if c in ['.', ':', ',', ';']:
        return (c, CharClass.PUNCTUATOR)
    if c in [' ', '\n', '\t']:
        return (c, CharClass.BLANK)
    return (c, CharClass.OTHER)

# calls getChar and getChar until it returns a non-blank
def getNonBlank(input):
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input

# adds the next char from input to lexeme, advancing the input by one char
def addChar(input, lexeme):
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)

# all tokens
class Token(Enum):
    ADDITION        = 1
    ASSIGNMENT      = 2
    BEGIN           = 3
    BOOLEAN_TYPE    = 4
    COLON           = 5
    DO              = 6
    ELSE            = 7
    END             = 8
    EQUAL           = 9
    FALSE           = 10
    GREATER         = 11
    GREATER_EQUAL   = 12
    IDENTIFIER      = 13
    IF              = 14
    INTEGER_LITERAL = 15
    INTEGER_TYPE    = 16
    LESS            = 17
    LESS_EQUAL      = 18
    MULTIPLICATION  = 19
    PERIOD          = 20
    PROGRAM         = 21
    READ            = 22
    SEMICOLON       = 23
    SUBTRACTION     = 24
    THEN            = 25
    TRUE            = 26
    VAR             = 27
    WHILE           = 28
    WRITE           = 29


# lexeme to token conversion
lookup = {
    "+"          : Token.ADDITION,
    "-"          : Token.SUBTRACTION,
    "*"          : Token.MULTIPLICATION,
    "<"          : Token.LESS,
    "<="         : Token.LESS_EQUAL,
    ">"          : Token.GREATER,
    ">="         : Token.GREATER_EQUAL,
    "program"    : Token.PROGRAM,
    "."          : Token.PERIOD,
    "var"        : Token.VAR,
    ";"          : Token.SEMICOLON,
    "integer"    : Token.INTEGER_TYPE,
    "boolean"    : Token.BOOLEAN_TYPE,
    "begin"      : Token.BEGIN,
    ":"          : Token.COLON,
    "end"        : Token.END,
    "read"       : Token.READ,
    "write"      : Token.WRITE,
    "if"         : Token.IF,
    "then"       : Token.THEN,
    "else"       : Token.ELSE,
    "while"      : Token.WHILE,
    "do"         : Token.DO,
    "true"       : Token.TRUE,
    "false"      : Token.FALSE,
    ":="         : Token.ASSIGNMENT,

}

# returns the next (lexeme, token) pair or None if EOF is reached
def lex(input):
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # check EOF first
    if charClass == CharClass.EOF:
        return (input, None, None)

    # TODO: reading letters
    if charClass == CharClass.LETTER:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if lexeme in lookup:
                return (input, lexeme, lookup[lexeme])
            if charClass != CharClass.LETTER and charClass != CharClass.DIGIT:
                break
        return (input, lexeme, Token.IDENTIFIER)

    # TODO: reading digits
    if charClass == CharClass.DIGIT:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if charClass != CharClass.DIGIT:
                break
        return (input, lexeme, Token.INTEGER_LITERAL)

    # TODO: reading an operator

    if charClass == CharClass.OPERATOR:
        input, lexeme = addChar(input, lexeme)
        c, charClass = getChar(input)
        if c == '=':
            input, lexeme = addChar(input, lexeme)
            return (input, lexeme, lookup[lexeme])
        if lexeme in lookup:
            return (input, lexeme, lookup[lexeme])

    # TODO: reading a punctuator
    if charClass == CharClass.PUNCTUATOR:
        input, lexeme = addChar(input, lexeme)
        c, charClass = getChar(input)
        if c == '=' and lexeme == ':':
            input, lexeme = addChar(input, lexeme)
            return (input, lexeme, lookup[lexeme])
        if lexeme in lookup:
            return (input, lexeme, lookup[lexeme])


    # TODO: anything else, raise an exception
    raise Exception("Lexical Analyzer Error: unrecognized symbol was found")

# main
if __name__ == "__main__":

    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError("Couldn't open source file")
    input = source.read()
    source.close()


    output = []
    # main loop
    while True:
        input, lexeme, token = lex(input)
        if lexeme == None:
            break
        output.append((lexeme, token))

    # prints the output
    for (lexeme, token) in output:
        print(lexeme, token)
