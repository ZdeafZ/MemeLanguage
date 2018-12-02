import sys


class TokenType:

    identifier = "identifier"
    number = "number"
    keyword = "keyword"
    operator = "operator"
    integerType = "type_integer"
    doubleType = "type_double"
    stringType = "type_string"
    characterType = "type_character"
    integerLiteral = "integer"
    booleanLiteral = "boolean"
    stringLiteral = "string"
    floatLiteral = "float"
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


def unify_types(type1,type2):
    if type1 is None:
        print("type1 is gay")
    elif type2 is None:
        print("type2 is gay")
    else:
        if type(type1) != type(type2):
            if type2.type.type != "keyword":
                print("{}.meme:{}:error:type mismatch: {} vs {}".format(sys.argv[1], type2.type.line +1, type1.type.value, type2.type.type),
                      file=sys.stderr)
            else:
                print("{}.meme:{}:error:type mismatch: {} vs {}".format(sys.argv[1], type2.type.line + 1,
                                                                        type1.type.value, type2.type.value),
                      file=sys.stderr)

class Node:
    def print(self,p):
        p.print("CLASS NOT IMPLEMENTED")

    def resolve_names(self, scope):
        print("not implemented for {}".format(self.__class__.__name__))

    def check_types(self):
        print("not implemented for {}".format(self.__class__.__name__))


class FuncDefinition(Node):
    def __init__ (self, rtype, name, params, body):
        self.type = rtype
        self.name = name
        self.params = params
        self.funcbody = body

    def print(self,p):
        p.print("Type",self.type)
        p.print("Name",self.name)
        p.print("Args",self.params)
        p.print("Body",self.funcbody)

    def resolve_names(self,scope):
        import myparser.myparser as parser
        inner_scope = parser.Scope(scope)
        for args in self.params:
            inner_scope.add(args.name,args)
        self.funcbody.resolve_names(inner_scope)

    def check_types(self):
        self.funcbody.check_types()


class Functions(Node):

    def __init__ (self):
        self.functions = []

    def appendFunction(self, func):
        self.functions.append(func)

    def print(self, p):
        p.print("Functions", self.functions)

    def resolve_names(self,scope):
        for func in self.functions:
            scope.add(func.name, func)
        for func in self.functions:
            func.resolve_names(scope)

    def check_types(self):
        for func in self.functions:
            func.check_types()


class Type(Node):
    pass


class TypeInt(Type):
    def __init__(self, rtype):
        self.type = rtype

    def print(self,p):
        p.print("Type",self.type)


class TypeString(Type):
    def __init__(self, rtype):
        self.type = rtype

    def print(self,p):
        p.print("Type",self.type)


class TypeFloat(Type):
    def __init__(self, rtype):
        self.type = rtype

    def print(self,p):
        p.print("Type",self.type)


class TypeNothing(Type):
    def __init__(self, rtype):
        self.type = rtype

    def print(self,p):
        p.print("Type",self.type)


class TypeBoolean(Type):
    def __init__(self, rtype):
        self.type = rtype

    def print(self,p):
        p.print("Type",self.type)


class TypeCharacter(Type):
    def __init__(self, rtype):
        self.type = rtype

    def print(self,p):
        p.print("Type",self.type)


class Expr(Node):
    def print(self,p):
        p.print("CLASS NOT IMPLEMENTED")


class ExprPriority(Expr):
    def __init__(self, exprs):
        self.exprs = exprs

    def print(self ,p):
        p.print("Expression",self.exprs)

    def resolve_names(self,scope):
        self.exprs.resolve_names(scope)


class ExprConstant(Expr):
    def __init__ (self, lit):
        self.lit = lit

    def print(self,p):
        p.print("Literal",self.lit)

    def resolve_names(self,scope):
        pass

    def check_types(self):
        if self.lit.type == TokenType.integerLiteral:
            return TypeInt(self.lit)
        elif self.lit.type == TokenType.floatLiteral:
            return TypeFloat(self.lit)
        elif self.lit.type == TokenType.stringLiteral:
            return TypeFloat(self.lit)
        elif self.lit.type == TokenType.booleanLiteral:
            return TypeFloat(self.lit)


class ExprVar(Expr):
    def __init__(self, name):
        self.name = name

    def print(self,p):
        p.print("Name",self.name)

    def resolve_names(self,scope):
        self.target = scope.resolve(self.name)


    def check_types(self):
        return self.target.type

class Arg(Node):
    def __init__(self, arg_type, name):
        self.arg_type = arg_type
        self.name = name

    def print(self,p):
        p.print("Arg Type",self.arg_type)
        p.print("Name",self.name)


class Stmt(Node):
    pass


class Branch(Stmt):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def print(self,p):
        p.print("Cond",self.cond)
        p.print("Body",self.body)

    def resolve_names(self, scope):
        self.cond.resolve_names(scope)
        self.body.resolve_names(scope)


class StmtBlock(Stmt):
    def __init__(self):
        self.stmts = []

    def appendStmt(self,stmt):
        self.stmts.append(stmt)

    def print(self,p):
        p.print("Stmts",self.stmts)

    def resolve_names(self, scope):
        import myparser.myparser as parser
        inner_scope = parser.Scope(scope)
        for stmt in self.stmts:
            stmt.resolve_names(inner_scope)

    def check_types(self):
        for stmt in self.stmts:
            stmt.check_types()

class StmtExpr(Stmt):
    def __init__(self,expr):
        self.expr = expr

    def print(self,p):
        p.print("Expression",self.expr)

    def resolve_names(self,scope):
        if self.expr is not None:
            self.expr.resolve_names(scope)
    def check_types(self):
        return self.expr.check_types()

class StmtReturn(Stmt):
    def __init__(self, value):
        self.value = value

    def print(self,p):
        p.print("Return Value",self.value)

    def resolve_names(self,scope):
        if self.value is not None:
            self.value.resolve_namess(scope)


class StmtContinue(Stmt):
    def __init__(self, token):
        self.token = token

    def print(self,p):
        p.print("Continue", self.token)

    def resolve_names(self,scope):
        pass

class StmtIf(Stmt):
    def __init__(self, branches, body):
        self.branches = branches
        self.body = body

    def print(self,p):
        p.print("Condition branches", self.branches)
        p.print("Else block",self.body)

    def resolve_names(self,scope):
        for branch in self.branches:
            branch.resolve_names(scope)
        if self.body is not None:
            self.body.resolve_names(scope)

class StmtBreak(Stmt):
    def __init__(self,token):
        self.token = token

    def print(self,p):
        p.print("Break", self.token)

    def resolve_names(self,scope):
        pass

class StmtWhile(Stmt):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def print(self,p):
        p.print("Cond",self.cond)
        p.print("Body",self.body)

    def resolve_names(self,scope):
        self.cond.resolve_names(scope)
        self.body.resolve_names(scope)

class StmtAssign(Stmt):
    def __init__(self,type,name,operator,right):
        self.type = type
        self.name = name
        self.operator = operator
        self.right = right

    def print(self, p):
        p.print("Type", self.type)
        p.print("Name", self.name)
        p.print("Operator",self.operator)
        p.print("Right",self.right)

    def resolve_names(self,scope):
        if self.type is None:
            self.target = scope.resolve(self.name)
            self.right.resolve_names(scope)
        else:
            scope.add(self.name,self)
            self.target = scope.resolve(self.name)
            self.right.resolve_names(scope)

    def check_types(self):
        target_type = self.target.type
        value_type = self.right.check_types()
        unify_types(target_type,value_type)


class ExprBinary(Expr):
    def __init__(self,left,operator,right):
        self.operator = operator
        self.left = left
        self.right = right

    def print(self,p):
        p.print("Left",self.left)
        p.print("Operator",self.operator)
        p.print("Right",self.right)

    def resolve_names(self,scope):
        self.left.resolve_names(scope)
        self.right.resolve_names(scope)

    def check_types(self):
        left_type = self.left.check_types()
        right_type = self.right.check_types()
        unify_types(left_type,right_type)
        return left_type

class ExprUnary(Expr):
    def __init__(self,operator,right):
        self.operator = operator
        self.right = right

    def print(self,p):
        p.print("Operator",self.operator)
        p.print("Right",self.right)

    def resolve_names(self,scope):
        self.right.resolve_names(scope)


class ExprCall(Expr):
    def __init__(self,name,args):
        self.name = name
        self.args = args

    def print(self,p):
        p.print("Name",self.name)
        p.print("Args",self.args)

    def resolve_names(self,scope):
        self.target = scope.resolve(self.name)
        for arg in self.args:
            arg.resolve_names(scope)

    def check_types(self):
        if type(self.target) is FuncDefinition:
            params_count = len(self.target.params)
            args_count = len(self.args)
            if params_count != args_count:
                print("{}.meme:{}:error:invalid argument count: {} vs {}".format(sys.argv[1], self.target.name.line + 1
                      , params_count, args_count),
                      file=sys.stderr)
            mininum = min(params_count, args_count)
            for i in range (0,mininum):
                param_type = self.target.params[i].arg_type
                arg_type = self.args[i].check_types()
                unify_types(param_type, arg_type)
            return self.target.type
