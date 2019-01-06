import lexer.lexer as lex
from myparser.myparser import *
import astPrinter.astPrinter as printer
import sys
import CodeGenerator.generate_code as CodeGen
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
    elif str(sys.argv[2]) == "check_types":
        root_scope = Scope()
        result.resolve_names(root_scope)
        result.check_types()
    elif str(sys.argv[2] == "generate_code"):
        root_scope = Scope()
        result.resolve_names(root_scope)
        if getErrorFoundStatus():
            result.check_types()
        if getErrorFoundStatus():
            result.check_main()
        if getErrorFoundStatus():
            writer = CodeGen.CodeWriter()
            result.generate_code(writer)
            writer.dump()

    else:
        print("Argument not found. Argument list can be found in the README", file=sys.stderr)
except IndexError:
    lexer.printTokens()
    result.print(printer)
    root_scope = Scope()
    result.resolve_names(root_scope)
    result.check_types()
    writer = CodeGen.CodeWriter()
#    result.generate_code(writer)
