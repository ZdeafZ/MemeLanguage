import sys
from lexer.lexer import *
from myparser.myparser import *
from astPrinter.astPrinter import ASTPrinter
try:
    with open("{}.meme".format(str(sys.argv[1])), "r") as file:
        string = file.read()
except:
    print("File you are trying to lex was not found. Exiting")
    sys.exit()
with open ("lexer/keywords.txt", "r") as file:
    keywordList = file.read().split(",")
with open ("lexer/operators.txt", "r") as file:
    operatorList = file.read().split(",")

lexer = Lexer(string, keywordList, operatorList)
lexer.run()
parser = Parser(lexer.tokenList)
result = parser.parse_functions()
printer = ASTPrinter()
result.print(printer)