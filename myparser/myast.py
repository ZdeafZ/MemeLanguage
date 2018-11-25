
class Node:
    def print(self,p):
        p.print("CLASS NOT IMPLEMENTED")

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

class Functions(Node):

    def __init__ (self):
        self.functions = []

    def appendFunction(self, func):
        self.functions.append(func)

    def print(self, p):
        p.print("Functions", self.functions)


class Type(Node):
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

class ExprConstant(Expr):
    def __init__ (self, lit):
        self.lit = lit

    def print(self,p):
        p.print("Literal",self.lit)

class  ExprVar(Expr):
    def __init__(self, name):
        self.name = name

    def print(self,p):
        p.print("Name",self.name)

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

class StmtBlock(Stmt):
    def __init__(self):
        self.stmts = []

    def appendStmt(self,stmt):
        self.stmts.append(stmt)

    def print(self,p):
        p.print("Stmts",self.stmts)

class StmtExpr(Stmt):
    def __init__(self,expr):
        self.expr = expr

    def print(self,p):
        p.print("Expression",self.expr)

class StmtReturn(Stmt):
    def __init__(self, value):
        self.value = value

    def print(self,p):
        p.print("Return Value",self.value)

class StmtIf(Stmt):
    def __init__(self, branches, body):
        self.branches = branches
        self.body = body

    def print(self,p):
        p.print("Condition branches", self.branches)
        p.print("Else block",self.body)

class StmtBreak(Stmt):
    def print(self,p):
        p.print("Break")

class StmtWhile(Stmt):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def print(self,p):
        p.print("Cond",self.cond)
        p.print("Body",self.body)

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

class ExprBinary(Expr):
    def __init__(self,left,operator,right):
        self.operator = operator
        self.left = left
        self.right = right
    def print(self,p):
        p.print("Left",self.left)
        p.print("Operator",self.operator)
        p.print("Right",self.right)
        
class ExprUnary(Expr):
    def __init__(self,operator,right):
        self.operator = operator
        self.right = right
    def print(self,p):
        p.print("Operator",self.operator)
        p.print("Right",self.right)