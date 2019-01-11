import meme_lexer.lexer as lex
import meme_parser.parser as parse
import meme_ast.ast as ast
import meme_ast_printer.printer as printer
import sys
import meme_codegen.generate_code as code_gen
import meme_virtual_machine.virtual_machine as virtual_machine
try:
    with open("{}.meme".format(str(sys.argv[1])), "r") as file:
        string = file.read()
except:
    print("File you are trying to lex was not found. Exiting")
    sys.exit()
with open ("meme_utils/keywords.dat", "r") as file:
    keywordList = file.read().split(",")
with open ("meme_utils/operators.dat", "r") as file:
    operatorList = file.read().split(",")

lexer = lex.Lexer(string, keywordList, operatorList)
lexer.run()
parser = parse.Parser(lexer.tokenList)
result = parser.parse_functions()
printer = printer.ASTPrinter()

try:
    if str(sys.argv[2]) == "lex":
        lexer.printTokens()
    elif str(sys.argv[2]) == "parse":
        result.print(printer)
    elif str(sys.argv[2]) == "resolve":
        root_scope = parse.Scope()
        result.resolve_names(root_scope)
    elif str(sys.argv[2]) == "check_types":
        root_scope = parse.Scope()
        result.resolve_names(root_scope)
        result.check_types()
    elif str(sys.argv[2]) == "generate_code":
        root_scope = parse.Scope()
        result.resolve_names(root_scope)
        if ast.get_error_found_status():
            result.check_types()
        if ast.get_error_found_status():
            result.check_main()
        if ast.get_error_found_status():
            writer = code_gen.CodeWriter()
            result.generate_code(writer)
            writer.dump()
    elif str(sys.argv[2]) == "execute_virtual":
        root_scope = parse.Scope()
        result.resolve_names(root_scope)
        if ast.get_error_found_status():
            result.check_types()
        if ast.get_error_found_status():
            result.check_main()
        if ast.get_error_found_status():
            writer = code_gen.CodeWriter()
            result.generate_code(writer)
            vm = virtual_machine.VirtualMachine(writer.code)
            vm.execute()
    else:
        print("Argument not found. Argument list can be found in the README", file=sys.stderr)

except IndexError:
    lexer.printTokens()
    result.print(printer)
    root_scope = parse.Scope()
    result.resolve_names(root_scope)
    if ast.get_error_found_status():
        result.check_types()
    if ast.get_error_found_status():
        result.check_main()
    if ast.get_error_found_status():
        writer = code_gen.CodeWriter()
        result.generate_code(writer)
        vm = virtual_machine.VirtualMachine(writer.code)
        vm.execute()
