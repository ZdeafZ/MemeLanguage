import sys


class TokenType:

    identifier = "identifier"
    number = "number"
    keyword = "keyword"
    operator = "operator"
    integerType = "type_integer"
    doubleType = "type_double"
    stringType = "type_string"
    nothingType = "nothing"
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

def printMistmatchError(type1,type2,line=None):
    if type1 is not None and type2 is not None:
        if type(type1) is TypeBoolean:
            temp1 = "boolean"
        if type(type1) is TypeFloat:
            temp1 = "float"
        if type(type1) is TypeInt:
            temp1 = "integer"
        if type(type1) is TypeNothing:
            temp1 = "nothing"
        if type(type1) is TypeString:
            temp1 = "string"
        if type(type2) is TypeBoolean:
            temp2 = "boolean"
        if type(type2) is TypeFloat:
            temp2 = "float"
        if type(type2) is TypeInt:
            temp2 = "integer"
        if type(type2) is TypeNothing:
            temp2 = "nothing"
        if type(type2) is TypeString:
            temp2 = "string"
        if line is None:
            line = type1.type.line + 1
        print("{}.meme:{}:error:type mismatch: {} vs {}".format(sys.argv[1], line,
                                                                temp1, temp2),
              file=sys.stderr)


def printArgsMismatchError(params_count, args_count, target):
    print("{}.meme:{}:error:invalid argument count: {} vs {}".format(sys.argv[1], target.name.line + 1
                                                                     , params_count, args_count),
          file=sys.stderr)

def printNotCallable(name):
    print("{}.meme:{}:error:not a callable object".format(sys.argv[1], name.line + 1),
          file=sys.stderr)

def printNotVariable(value):
    print("{}.meme:{}:error:not a variable".format(sys.argv[1], value.line + 1),
          file=sys.stderr)
          

def unify_types(type1,type2,line=None):
    if type(type1) != type(type2):
        printMistmatchError(type1,type2,line)

class Node:
    def __init__(self):
        self.parent = None

    def print(self,p):
        p.print("CLASS NOT IMPLEMENTED")

    def resolve_names(self, scope):
        print("not implemented for {}".format(self.__class__.__name__))

    def check_types(self):
        print("not implemented for {}".format(self.__class__.__name__))

    def add_children(self,value):
        if value is None:
            pass
        elif type(value) is list:
            for x in value:
                self.add_children(x)
        elif issubclass(type(value), Node) or issubclass(type(value), Stmt) or issubclass(type(value), Expr):
            value.parent = self

    def ancestor_fn(self):
        current = self.parent
        while current is not None:
            if type(current) is FuncDefinition:
                break
            current = current.parent
        return current

    def ancestor_loop(self):
        current = self.parent
        while current is not None:
            if type(current) is StmtWhile:
                break
            current = current.parent
        return current


class FuncDefinition(Node):
    def __init__ (self, rtype, name, params, body, parent=None):
        self.type = rtype
        self.add_children(self.type)
        self.name = name
        self.params = params
        self.add_children(self.params)
        self.funcbody = body
        self.add_children(self.funcbody)
        self.parent = parent

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

    def __init__ (self, parent=None):
        self.functions = []
        self.parent = parent

    def appendFunction(self, func):
        self.functions.append(func)
        self.add_children(func)

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
    def __init__(self, exprs, parent=None):
        self.exprs = exprs
        self.add_children(self.exprs)
        self.parent = parent

    def print(self ,p):
        p.print("Expression",self.exprs)

    def resolve_names(self,scope):
        self.exprs.resolve_names(scope)


class ExprConstant(Expr):
    def __init__ (self, lit, parent=None):
        self.lit = lit
        self.parent = parent

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
            return TypeString(self.lit)
        elif self.lit.type == TokenType.booleanLiteral:
            return TypeBoolean(self.lit)


class ExprVar(Expr):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def print(self,p):
        p.print("Name",self.name)

    def resolve_names(self,scope):
        self.target = scope.resolve(self.name)

    def check_types(self):
        if type(self.target) is StmtDeclaration:
            return self.target.type
        elif type(self.target) is FuncDefinition:
            printNotVariable(self.name)
        else:
            pass
            

class Arg(Node):
    def __init__(self, arg_type, name, parent=None):
        self.arg_type = arg_type
        self.add_children(arg_type)
        self.name = name
        self.parent = parent

    def print(self,p):
        p.print("Arg Type",self.arg_type)
        p.print("Name",self.name)


class Stmt(Node):
    pass


class Branch(Stmt):
    def __init__(self, cond, body, parent=None):
        self.cond = cond
        self.add_children(self.cond)
        self.body = body
        self.add_children(self.body)
        self.parent = parent

    def print(self,p):
        p.print("Cond",self.cond)
        p.print("Body",self.body)

    def resolve_names(self, scope):
        self.cond.resolve_names(scope)
        self.body.resolve_names(scope)

    def check_types(self):
        cond_type = self.cond.check_types()
        unify_types(cond_type,TypeBoolean(None))
        self.body.check_types()

class StmtBlock(Stmt):
    def __init__(self, parent=None):
        self.stmts = []
        self.parent = parent

    def appendStmt(self,stmt):
        self.stmts.append(stmt)
        self.add_children(stmt)

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
    def __init__(self,expr,parent=None):
        self.expr = expr
        self.parent = parent

    def print(self,p):
        p.print("Expression",self.expr)

    def resolve_names(self,scope):
        if self.expr is not None:
            self.expr.resolve_names(scope)

    def check_types(self):
        return self.expr.check_types()


class StmtReturn(Stmt):
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent

    def print(self,p):
        p.print("Return Value",self.value)

    def resolve_names(self,scope):
        if self.value is not None:
            self.value.resolve_names(scope)

    def check_types(self):
        if self.value is not None:
            value_type = self.value.check_types()
        else:
            value_type = TypeNothing(self.value)
        ret_type = self.ancestor_fn().type
        unify_types(value_type, ret_type)


class StmtContinue(Stmt):
    def __init__(self, token, parent=None):
        self.token = token
        self.parent = parent

    def print(self,p):
        p.print("Continue", self.token)

    def resolve_names(self,scope):
        pass

    def check_types(self):
        if self.ancestor_loop() is None:
            print("continue is not in loop faggot")

class StmtIf(Stmt):
    def __init__(self, branches, body, parent=None):
        self.branches = branches
        self.add_children(self.branches)
        self.body = body
        self.add_children(self.body)
        self.parent = parent

    def print(self,p):
        p.print("Condition branches", self.branches)
        p.print("Else block",self.body)

    def resolve_names(self,scope):
        for branch in self.branches:
            branch.resolve_names(scope)
        if self.body is not None:
            self.body.resolve_names(scope)

    def check_types(self):
        for branch in self.branches:
            branch.check_types()
        if self.body is not None:
            self.body.check_types()

class StmtBreak(Stmt):
    def __init__(self,token, parent=None):
        self.token = token
        self.parent = parent

    def print(self,p):
        p.print("Break", self.token)

    def resolve_names(self,scope):
        pass

    def check_types(self):
        if self.ancestor_loop() is None:
            print("break not in loop faggot")

class StmtWhile(Stmt):
    def __init__(self, cond, body, parent=None):
        self.cond = cond
        self.add_children(self.cond)
        self.body = body
        self.add_children(self.body)
        self.parent = parent

    def print(self,p):
        p.print("Cond",self.cond)
        p.print("Body",self.body)

    def resolve_names(self,scope):
        self.cond.resolve_names(scope)
        self.body.resolve_names(scope)

    def check_types(self):
        cond_type = self.cond.check_types()
        unify_types(cond_type, TypeBoolean(None))
        self.body.check_types()

class StmtAssign(Stmt):
    def __init__(self,name,operator,right,parent=None):
        self.name = name
        self.operator = operator
        self.right = right
        self.parent = parent

    def print(self, p):
        p.print("Name", self.name)
        p.print("Operator",self.operator)
        p.print("Right",self.right)

    def resolve_names(self,scope):
        self.target = scope.resolve(self.name)
        self.right.resolve_names(scope)

    def check_types(self):
        if self.target is not None:
            target_type = self.target.type
            value_type = self.right.check_types()
            unify_types(target_type,value_type)


class StmtDeclaration(Stmt):
    def __init__(self,type,name,operator,right,parent=None):
        self.type = type
        self.add_children(self.type)
        self.name = name
        self.operator = operator
        self.right = right
        self.parent = parent

    def print(self, p):
        p.print("Type", self.type)
        p.print("Name", self.name)
        p.print("Operator",self.operator)
        p.print("Right",self.right)

    def resolve_names(self,scope):
        scope.add(self.name,self)
        self.target = scope.resolve(self.name)
        self.right.resolve_names(scope)

    def check_types(self):
        target_type = self.target.type
        value_type = self.right.check_types()
        unify_types(target_type,value_type)

class ExprBinary(Expr):
    def __init__(self,left,operator,right,parent=None):
        self.operator = operator
        self.left = left
        self.add_children(self.left)
        self.right = right
        self.add_children(self.right)
        self.parent = parent

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
        unify_types(left_type, right_type)
        return left_type

class ExprUnary(Expr):
    def __init__(self,operator,right,parent=None):
        self.operator = operator
        self.right = right
        self.add_children(self.right)
        self.parent = parent

    def print(self,p):
        p.print("Operator",self.operator)
        p.print("Right",self.right)

    def resolve_names(self,scope):
        self.right.resolve_names(scope)


class ExprCall(Expr):
    def __init__(self,name,args,parent=None):
        self.name = name
        self.args = args
        self.add_children(self.args)
        self.parent = parent

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
                printArgsMismatchError(params_count, args_count, self.target)

            mininum = min(params_count, args_count)
            for i in range (0,mininum):
                param_type = self.target.params[i].arg_type
                arg_type = self.args[i].check_types()
                unify_types(param_type, arg_type)
            return self.target.type
        else:
            printNotCallable(self.name)
