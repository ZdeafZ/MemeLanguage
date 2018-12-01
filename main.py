import lexer.lexer as lex
from myparser.myparser import *
import astPrinter.astPrinter as printer
import sys
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

lexer = lex.Lexer(string, keywordList, operatorList)
lexer.run()
parser = Parser(lexer.tokenList)
result = parser.parse_functions()
printer = printer.ASTPrinter()

try:
    if str(sys.argv[2]) == "lex":
        lexer.printTokens()
    elif str(sys.argv[2]) == "parse":
        result.print(printer)
    elif str(sys.argv[2]) == "resolve":
        root_scope = Scope()
        result.resolve_names(root_scope)
    else:
        print("Argument not found. Argument list can be found in the README", file=sys.stderr)
except IndexError:
    lexer.printTokens()
    result.print(printer)

