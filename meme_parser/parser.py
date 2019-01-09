import meme_utils.current_stack_slot as stack
import meme_ast.ast as ast
import sys


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
            ast.TokenType.greaterThan,
            ast.TokenType.greaterThanOrEqual,
            ast.TokenType.lessThan,
            ast.TokenType.lessThanOrEqual,
            ast.TokenType.equal,
            ast.TokenType.notEqual
        ]
        self.addOperators = [
            ast.TokenType.plus,
            ast.TokenType.minus
        ]
        self.multOperators = [
            ast.TokenType.mult,
            ast.TokenType.div
        ]
        self.unaryOperators = [
            ast.TokenType.notSomething
        ]
        self.typeList = [
            "integer", "string", "boolean", "float"
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
            print("error", file=sys.stderr)
            print("{}.meme:{}:error:found {} expected {}".format(sys.argv[1], curr_token.line + 1, curr_token.type,
                                                                 token),
                  file=sys.stderr)
            sys.exit()

    def expectKeyword(self,value):
        if self.currentToken().value == value:
            return self.expect(ast.TokenType.keyword)
        else:
            curr_token = self.tokens[self.position]
            print("error", file=sys.stderr)
            print("{}.meme:{}:error:found {} with value {} expected value {}".format(sys.argv[1],curr_token.line + 1,
                                                                                     curr_token.type, self.currentToken().value, value,),file=sys.stderr)
            sys.exit()

    def parse_function(self):
        rtype = self.parse_type()
        identifier = self.parse_ident()
        args = self.parse_args()
        body = self.parse_body()
        return ast.FuncDefinition(rtype, identifier, args, body)

    def parse_functions(self):
        node = ast.Functions()
        while self.currentToken().type is not ast.TokenType.endOfFile:
            self.expect(ast.TokenType.keyword)
            temp = self.parse_function()
            node.appendFunction(temp)
            self.expect(ast.TokenType.newLine)
        return node

    def parse_type(self):
        result = self.expect(ast.TokenType.keyword)
        if result.value == "integer":
            return ast.TypeInt(result)
        elif result.value == "string":
            return ast.TypeString(result)
        elif result.value == "boolean":
            return ast.TypeBoolean(result)
        elif result.value == "float":
            return ast.TypeFloat(result)
        elif result.value == "character":
            return ast.TypeCharacter(result)
        elif result.value == "nothing":
            return ast.TypeNothing(result)

    def parse_ident(self):
        result = self.expect(ast.TokenType.identifier)
        return result

    def parse_args(self):
        args = []
        self.expect(ast.TokenType.leftParenthesis)
        if self.currentToken().type is not ast.TokenType.rightParenthesis:
            args.append(self.parse_arg())
        while self.accept(ast.TokenType.rightParenthesis) is None:
            self.expect(ast.TokenType.comma)
            args.append(self.parse_arg())
        return args

    def parse_arg(self):
        return ast.Arg(self.parse_type(),self.expect(ast.TokenType.identifier))

    def parse_body(self):
        node = ast.StmtBlock()
        self.accept(ast.TokenType.newLine)
        self.expect(ast.TokenType.leftBracket)
        self.expect(ast.TokenType.newLine)
        while self.accept(ast.TokenType.rightBracket) is None:
            node.appendStmt(self.parse_stmt())
            self.expect(ast.TokenType.newLine)
        return node

    def parse_stmt_body(self):
        node = ast.StmtBlock()
        self.expectKeyword("then")
        self.expect(ast.TokenType.newLine)
        while True:
            if self.currentToken().value == "end":
                break
            node.appendStmt(self.parse_stmt())
            self.expect(ast.TokenType.newLine)
        self.expectKeyword("end")
        return node

    def parse_stmt(self):
        if self.currentToken().type == ast.TokenType.leftBracket:
            return self.parse_body()
        elif self.currentToken().type == ast.TokenType.keyword:
            if self.currentToken().value == "if":
                return self.parse_if_stmt()
            elif self.currentToken().value == "return":
                return self.parse_return_stmt()
            elif self.currentToken().value == "break":
                return ast.StmtBreak(self.expect(ast.TokenType.keyword))
            elif self.currentToken().value == "continue":
                return ast.StmtContinue(self.expect(ast.TokenType.keyword))
            elif self.currentToken().value == "while":
                return self.parse_while_stmt()
            elif self.currentToken().value in self.typeList:
                return self.parse_assignment_stmt()
        else:
            return self.parse_stmt_expr()

    def parse_return_stmt(self):
        self.expectKeyword("return")
        value = None
        if self.currentToken().type is not ast.TokenType.newLine:
            value = self.parse_stmt_expr()
        return ast.StmtReturn(value)

    def parse_if_stmt(self):
        branches = []
        elsebody = None
        eifcond = None
        eifbody = None
        self.expectKeyword("if")
        self.expect(ast.TokenType.leftParenthesis)
        cond = self.parse_stmt_expr()
        self.expect(ast.TokenType.rightParenthesis)
        self.expect(ast.TokenType.newLine)
        body = self.parse_stmt_body()
        branches.append(ast.Branch(cond, body))
        if self.peekAtTokens().value == "elseif":
            self.expect(ast.TokenType.newLine)
        while self.currentToken().value == "elseif":
            self.expectKeyword("elseif")
            self.expect(ast.TokenType.leftParenthesis)
            eifcond = self.parse_stmt_expr()
            self.expect(ast.TokenType.rightParenthesis)
            self.expect(ast.TokenType.newLine)
            eifbody = self.parse_stmt_body()
            branches.append(ast.Branch(eifcond, eifbody))
            if self.peekAtTokens().value == "elseif" or  self.peekAtTokens().value == "else":
                self.expect(ast.TokenType.newLine)
        if self.currentToken().value == "else":
            self.expectKeyword("else")
            self.expect(ast.TokenType.newLine)
            elsebody = self.parse_stmt_body()
        return ast.StmtIf(branches,elsebody)

    def parse_while_stmt(self):
        self.expect(ast.TokenType.keyword)
        self.expect(ast.TokenType.leftParenthesis)
        cond = self.parse_stmt_expr()
        self.expect(ast.TokenType.rightParenthesis)
        self.expect(ast.TokenType.newLine)
        body = None
        if self.currentToken().value == "then":
            body = self.parse_stmt_body()
        return ast.StmtWhile(cond, body)

    def parse_assignment_stmt(self):
        type = self.parse_type()
        name = self.parse_ident()
        operator = self.expect(ast.TokenType.assign)
        right = self.parse_expr()
        return ast.StmtDeclaration(type, name, operator, right)

    def parse_priority_expr(self):
        self.expect(ast.TokenType.leftParenthesis)
        expr = self.parse_stmt_expr()
        self.expect(ast.TokenType.rightParenthesis)
        return ast.ExprPriority(expr)

    def parse_term_expr(self):
        if self.currentToken().type == ast.TokenType.identifier:
            name = self.expect(ast.TokenType.identifier)
            op = self.accept(ast.TokenType.assign)
            call = self.accept(ast.TokenType.leftParenthesis)
            args = []
            if op is not None:
                right = self.parse_expr()
                return ast.StmtAssign(name, op, right)
            elif call is not None:
                while self.accept(ast.TokenType.rightParenthesis) is None:
                    args.append(self.parse_expr())
                    self.accept(ast.TokenType.comma)
                return ast.ExprCall(name,args)
            return ast.ExprVar(name)
        elif self.currentToken().type == ast.TokenType.integerLiteral:
            literal = self.expect(ast.TokenType.integerLiteral)
            return ast.ExprConstant(literal)
        elif self.currentToken().type == ast.TokenType.booleanLiteral:
            literal = self.expect(ast.TokenType.booleanLiteral)
            return ast.ExprConstant(literal)
        elif self.currentToken().type == ast.TokenType.stringLiteral:
            literal = self.expect(ast.TokenType.stringLiteral)
            return ast.ExprConstant(literal)
        elif self.currentToken().type == ast.TokenType.floatLiteral:
            literal = self.expect(ast.TokenType.floatLiteral)
            return ast.ExprConstant(literal)
        elif self.currentToken().type == ast.TokenType.leftParenthesis:
            return self.parse_priority_expr()

    def parse_stmt_expr(self):
        expr = self.parse_logical_or_expr()
        return ast.StmtExpr(expr)
        
    def parse_expr(self):
        expr = self.parse_logical_or_expr()
        return ast.Expr(expr)
        
    def parse_logical_or_expr(self):
        left = self.parse_logical_and_expr()
        while True:
            result = self.accept(ast.TokenType.logicalOr)
            if result is None:
                break
            right = self.parse_logical_and_expr()
            left = ast.ExprBinaryLogical(left, result, right)
        return left
    
    def parse_logical_and_expr(self):
        left = self.parse_comparsion_expr()
        while True:
            result = self.accept(ast.TokenType.logicalAnd)
            if result is None:
                break
            right = self.parse_comparsion_expr()
            left = ast.ExprBinaryLogical(left, result, right)
        return left
        
    def parse_comparsion_expr(self):
        left = self.parse_add_expr()
        while True:
            if self.currentToken().type in self.compOperators:
                result = self.accept(self.currentToken().type)
                if result is None:
                    break
                right = self.parse_add_expr()
                if result.type == ast.TokenType.equal or result.type == ast.TokenType.notEqual:
                    left = ast.ExprBinaryEquality(left, result, right)
                else:
                    left = ast.ExprBinaryRelational(left, result, right)
            else:
                break
        return left

    def parse_add_expr(self):
        left = self.parse_mult_expr()
        while True:
            if self.currentToken().type in self.addOperators:
                result = self.accept(self.currentToken().type)
                if result is None:
                    break
                right = self.parse_mult_expr()
                left = ast.ExprBinaryArithmetic(left, result, right)
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
                left = ast.ExprBinaryArithmetic(left, result, right)
            else:
                break
        return left

    def parse_unary_expr(self):
        if self.currentToken().type in self.unaryOperators:
            operator =  self.accept(self.currentToken().type)
            right = self.parse_term_expr()
            return ast.ExprUnary(operator, right)
        else:
            return self.parse_term_expr()


class Scope:
    def __init__(self,parent_scope=None):
        self.members = {}
        self.parent_scope = parent_scope

    def add(self,name,node):
        if type(name) is not Token:
            raise TypeError("expected token got {}".format(type(name)))
        if not issubclass(type(node), ast.Node):
            raise TypeError("expected node got {}".format(type(node)))
        if hasattr(node,"stack_slot"):
            node.stack_slot = stack.current_stack_slot
            stack.current_stack_slot += 1

        if type(name) is Token:
            if name.value in self.members:
                print("{}.meme:{}:error:duplicate variable {}".format(sys.argv[1], name.line + 1, name.value),
                      file=sys.stderr)
            else:
                self.members[name.value] = node
        elif type(name) is ast.Node:
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