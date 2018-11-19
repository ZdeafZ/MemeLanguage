import sys
from myParser.parser import *


class TokenType:

    identifier = "identifier"
    number = "number"
    keyword = "keyword"
    operator = "operator"
    integerType = "type_integer"
    doubleType = "type_double"
    stringType = "type_string"
    characterType = "type_character"
    integerLiteral = "int_lit"
    booleanLiteral = "bool_lit"
    stringLiteral = "string_lit"
    floatLiteral = "float_lit"
    logicalAnd = "logical_and_op"
    logicalOr = "logical_or_op"
    plus = "plus"
    minus = "minus"
    mult = "multiplication"
    div = "division"
    greaterThan = "greater_than"
    greaterThanOrEqual = "greater_than_or_equal"
    lessThan = "less_than"
    lessThanOrEqual = "less_than_or_equal"
    equal = "equal"
    notSomething = "not"
    notEqual = "not_equal"
    assign = "assignment"
    leftParenthesis = "left_parenthesis"
    rightParenthesis = "right_parenthesis"
    leftBrace = "left_brace"
    rightBrace = "right_brace"
    leftBracket = "left_bracket"
    rightBracket = "right_bracket"
    newLine = "new_line"
    endOfFile = "end_of_file"
    commentStart = "comment_start"
    commentEnd = "comment_end"
    comma = "comma"


class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def print(self):
        print("|       {:22}       |        {:15}       |{:5}    |".format(self.type.upper(),self.value,self.line+1))

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def identPosition(self):
        self.position += 1

    def currentToken(self):
        return self.tokens[self.position]


    def accept(self, token):
        curr_token = self.tokens[self.position]
        if curr_token.type == token:
            self.identPosition()
            return curr_token


    def expect(self, token):
        result = self.accept(token)
        if result is not None:
            return result
        else:
            curr_token = self.tokens[self.position]
            print("error")
            print(" found {} expected {} at line {}".format(curr_token.type, token, curr_token.line + 1))
            sys.exit()

    def parse_function(self):
        rtype = self.parse_type()
        identifier = self.parse_ident()
        args = self.parse_args()
        body = self.parse_body()
        return FuncDefinition(rtype, identifier, args, body)

    def parse_functions(self):
        node = Functions()
        while self.currentToken().type is not TokenType.endOfFile:
            self.expect(TokenType.keyword)
            node.appendFunction(self.parse_function())
            self.expect(TokenType.newLine)
        return node

    def parse_type(self):
        result = self.expect(TokenType.keyword)
        if result.value == "integer":
            return Type(result)
        elif result.value == "string":
            return Type(result)
        elif result.value == "boolean":
            return Type(result)
        elif result.value == "float":
            return Type(result)

    def parse_ident(self):
        result = self.expect(TokenType.identifier)
        return ExprIdent(result)

    def parse_args(self):
        args = []
        self.expect(TokenType.leftParenthesis)
        if self.currentToken().type is not TokenType.rightParenthesis:
            args.append(self.parse_arg())
        while self.accept(TokenType.rightParenthesis) is None:
            self.expect(TokenType.comma)
            args.append(self.parse_arg())
        return args

    def parse_arg(self):
        return Arg(self.parse_type(),self.expect(TokenType.identifier))

    def parse_body(self):
        node = StmtBlock()
        self.expect(TokenType.leftBracket)
        while self.accept(TokenType.rightBracket) is None:
            node.appendStmt(self.parse_stmt())
            self.expect(TokenType.newLine)
        return node

    def parse_stmt(self):
        if self.currentToken().type == TokenType.leftBracket:
            return self.parse_body()
        elif self.currentToken().type == TokenType.keyword:
            if self.currentToken().value == "if":
                return Stmt()
            elif self.currentToken().value == "return":
                return self.parse_return_stmt()
            elif self.currentToken().value == "break":
                self.expect(TokenType.keyword)
                return StmtBreak()
            elif self.currentToken().value == "while":
                return Stmt()

    def parse_return_stmt(self):
        self.expect(TokenType.keyword)
        value = None
        if self.currentToken().type is not TokenType.newLine:
            value = self.parse_ident()
        return StmtReturn(value)
