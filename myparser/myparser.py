import sys
from myparser.myast import *

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
    plus = "plus_op"
    minus = "minus_op"
    mult = "multiplication_op"
    div = "division_op"
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
        self.compOperators = [
            TokenType.greaterThan,
            TokenType.greaterThanOrEqual,
            TokenType.lessThan,
            TokenType.lessThanOrEqual,
            TokenType.equal,
            TokenType.notEqual
        ]
        self.addOperators = [
            TokenType.plus,
            TokenType.minus
        ]
        self.multOperators = [
            TokenType.mult,
            TokenType.div
        ]
        self.unaryOperators = [
            TokenType.notSomething
        ]
    def peekAtTokens(self):
        if self.position < len(self.tokens)-1:
            return self.tokens[self.position+1]


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
            print("error",file=sys.stderr)
            print("{}.meme:{}:error:found {} expected {}".format(sys.argv[1],curr_token.line + 1,curr_token.type, token), file=sys.stderr)
            sys.exit()

    def expectKeyword(self,value):
        if self.currentToken().value == value:
            return self.expect(TokenType.keyword)
        else:
            curr_token = self.tokens[self.position]
            print("error",file=sys.stderr)
            print("{}.meme:{}:error:found {} with value {} expected value {}".format(sys.argv[1],curr_token.line + 1, curr_token.type, self.currentToken().value, value,),file=sys.stderr)
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
            temp = self.parse_function()
            node.appendFunction(temp)
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
        elif result.value == "character":
            return Type(result)

    def parse_ident(self):
        result = self.expect(TokenType.identifier)
        return result

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
        self.accept(TokenType.newLine)
        self.expect(TokenType.leftBracket)
        self.expect(TokenType.newLine)
        while self.accept(TokenType.rightBracket) is None:
            node.appendStmt(self.parse_stmt())
            self.expect(TokenType.newLine)
        return node

    def parse_stmt_body(self):
        node = StmtBlock()
        self.expectKeyword("then")
        self.expect(TokenType.newLine)
        while True:
            if self.currentToken().value == "end":
                break
            node.appendStmt(self.parse_stmt())
            self.expect(TokenType.newLine)
        self.expectKeyword("end")
        return node

    def parse_stmt(self):
        if self.currentToken().type == TokenType.leftBracket:
            return self.parse_body()
        elif self.currentToken().type == TokenType.keyword:
            if self.currentToken().value == "if":
                return self.parse_if_stmt()
            elif self.currentToken().value == "return":
                return self.parse_return_stmt()
            elif self.currentToken().value == "break":
                return StmtBreak(self.expect(TokenType.keyword))
            elif self.currentToken().value == "continue":
                return StmtContinue(self.expect(TokenType.keyword))
            elif self.currentToken().value == "while":
                return self.parse_while_stmt()
            elif self.currentToken().value == "integer":
                return self.parse_assignment_stmt()
        else:
            return self.parse_stmt_expr()

    def parse_return_stmt(self):
        self.expectKeyword("return")
        value = None
        if self.currentToken().type is not TokenType.newLine:
            value = self.parse_stmt_expr()
        return StmtReturn(value)

    def parse_if_stmt(self):
        branches = []
        elsebody = None
        eifcond = None
        eifbody = None
        self.expectKeyword("if")
        cond = self.parse_stmt_expr()
        self.expect(TokenType.newLine)
        body = self.parse_stmt_body()
        branches.append(Branch(cond,body))
        if self.peekAtTokens().value == "elseif":
            self.expect(TokenType.newLine)
        while self.currentToken().value == "elseif":
            self.expectKeyword("elseif")
            eifcond = self.parse_stmt_expr()
            self.expect(TokenType.newLine)
            eifbody = self.parse_stmt_body()
            branches.append(Branch(eifcond, eifbody))
            if self.peekAtTokens().value == "elseif" or  self.peekAtTokens().value == "else":
                self.expect(TokenType.newLine)
        if self.currentToken().value == "else":
            self.expectKeyword("else")
            self.expect(TokenType.newLine)
            elsebody = self.parse_stmt_body()
        return StmtIf(branches,elsebody)

    def parse_while_stmt(self):
        self.expect(TokenType.keyword)
        cond = self.parse_stmt_expr()
        self.expect(TokenType.newLine)
        body = None
        if self.currentToken().value == "then":
            body = self.parse_stmt_body()
        return StmtWhile(cond, body)

    def parse_assignment_stmt(self):
        type = None
        if self.currentToken().type == TokenType.keyword:
           type = self.parse_type()
        name = self.parse_ident()
        operator = self.expect(TokenType.assign)
        right = self.parse_stmt_expr()
        return StmtAssign(type,name,operator,right)

    def parse_priority_expr(self):
        self.expect(TokenType.leftParenthesis)
        expr = self.parse_stmt_expr()
        self.expect(TokenType.rightParenthesis)
        return ExprPriority(expr)

    def parse_term_expr(self):
        if self.currentToken().type == TokenType.identifier:
            name = self.expect(TokenType.identifier)
            op = self.accept(TokenType.assign)
            call = self.accept(TokenType.leftParenthesis)
            args = []
            if op is not None:
                right = self.parse_stmt_expr()
                return StmtAssign(None,name,op,right)
            elif call is not None:
                while self.accept(TokenType.rightParenthesis) is None:
                    args.append(self.parse_stmt_expr())
                    self.accept(TokenType.comma)
                return ExprCall(name,args)
            return ExprVar(name)
        elif self.currentToken().type == TokenType.integerLiteral:
            literal = self.expect(TokenType.integerLiteral)
            return ExprConstant(literal)
        elif self.currentToken().type == TokenType.booleanLiteral:
            literal = self.expect(TokenType.booleanLiteral)
            return ExprConstant(literal)
        elif self.currentToken().type == TokenType.stringLiteral:
            literal = self.expect(TokenType.stringLiteral)
            return ExprConstant(literal)
        elif self.currentToken().type == TokenType.floatLiteral:
            literal = self.expect(TokenType.floatLiteral)
            return ExprConstant(literal)
        elif self.currentToken().type == TokenType.leftParenthesis:
            return self.parse_priority_expr()

    def parse_stmt_expr(self):
        expr = self.parse_logical_or_expr()
        return StmtExpr(expr)
        
    def parse_logical_or_expr(self):
        left = self.parse_logical_and_expr()
        while True:
            result = self.accept(TokenType.logicalOr)
            if result is None:
                break
            right = self.parse_logical_and_expr()
            left = ExprBinary(left, result, right)
        return left
    
    def parse_logical_and_expr(self):
        left = self.parse_comparsion_expr()
        while True:
            result = self.accept(TokenType.logicalAnd)
            if result is None:
                break
            right = self.parse_comparsion_expr()
            left = ExprBinary(left, result, right)
        return left
        
    def parse_comparsion_expr(self):
        left = self.parse_add_expr()
        while True:
            result = self.accept(TokenType.greaterThan)
            if result is None:
                break
            right = self.parse_add_expr()
            left = ExprBinary(left, result, right)
        return left

    def parse_add_expr(self):
        left = self.parse_mult_expr()
        while True:
            if self.currentToken().type in self.addOperators:
                result = self.accept(self.currentToken().type)
                if result is None:
                    break
                right = self.parse_mult_expr()
                left = ExprBinary(left, result, right)
            else:
                break
        return left

    def parse_mult_expr(self):
        left = self.parse_unary_expr()
        while True:
            if self.currentToken().type in self.multOperators:
                result = self.accept(self.currentToken().type)
                if result is None:
                    break
                right = self.parse_unary_expr()
                left = ExprBinary(left, result, right)
            else:
                break
        return left

    def parse_unary_expr(self):
        if self.currentToken().type in self.unaryOperators:
            operator =  self.accept(self.currentToken().type)
            right = self.parse_term_expr()
            return ExprUnary(operator, right)
        else:
            return self.parse_term_expr()


class Scope:
    def __init__(self,parent_scope=None):
        self.members = {}
        self.parent_scope = parent_scope

    def add(self,name,node):
        if type(name) is not Token:
            raise TypeError("expected token got {}".format(type(name)))
        if not issubclass(type(node),Node):
            raise TypeError("expected node got {}".format(type(node)))
        if type(name) is Token:
            if name.value in self.members:
                print("{}.meme:{}:error:duplicate variable {}".format(sys.argv[1], name.line + 1, name.value),
                      file=sys.stderr)
            else:
                self.members[name.value] = node
        elif name is Node:
            if name.name.value in self.members:
                print("{}.meme:{}:error:duplicate variable {}".format(sys.argv[1], name.name.line + 1, name.name.value),
                      file=sys.stderr)
            else:
                self.members[name.name.value] = node

    def resolve(self,name):
        if type(name) is not Token:
            raise TypeError("expected token got {}".format(type(name)))
        elif name.value in self.members:
            return self.members[name.value]
        elif self.parent_scope is not None:
            return self.parent_scope.resolve(name)
        else:
            print("{}.meme:{}:error:undeclared variable {}".format(sys.argv[1], name.line + 1, name.value),
                  file=sys.stderr)
