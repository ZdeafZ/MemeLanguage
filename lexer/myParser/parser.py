
class Node:
    def print(self):
        print("CLASS NOT IMPLEMENTED")

class FuncDefinition(Node):
    def __init__ (self, rtype, name, params, body):
        self.type = rtype
        self.name = name
        self.params = params
        self.funcbody = body

    def print(self):
        print(self.type)
        print(self.name)
        print(self.params)
        print(self.funcbody)

class Functions(Node):

    def __init__ (self):
        self.functions = []

    def appendFunction(self, func):
        self.functions.append(func)

    def print(self):
        print(self.functions)


class Type(Node):
    def __init__(self, rtype):
        self.type = rtype

    def print(self):
        print(self.type)

class Expr(Node):
    def __init__(self, op,left,right):
        self.op = op
        self.left = left
        self.right = right

    def print(self):
        print(self.op)
        print(self.left)
        print(self.right)

class ExprPriority(Node):
    def __init__(self, exprs):
        self.exprs = exprs

    def print(self):
        print(self.exprs)

class ExprConstant(Node):
    def __init__ (self, lit):
        self.lit = lit

    def print(self):
        print(self.lit)

class  ExprIdent(Node):
    def __init__(self, name):
        self.name = name

    def print(self):
        print(self.name)

class Arg(Node):
    def __init__(self, rtype, name):
        self.rtype = rtype
        self.name = name

class Stmt(Node):
    pass

class StmtBlock(Stmt):
    def __init__(self):
        self.stmts = []

    def appendStmt(self,stmt):
        self.stmts.append(stmt)

    def print(self):
        print(self.stmts)

class StmtExpr(Stmt):
    def __init__(self,expr):
        self.expr = expr

    def print(self):
        print(self.expr)

class StmtReturn(Stmt):
    def __init__(self, rident):
        self.rident = rident

    def print(self):
        print(self.rident)

class StmtIf(Stmt):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def print(self):
        print(self.cond)
        print(self.body)

class StmtBreak(Stmt):
    def print(self):
        print("break")

class StmtWhile(Stmt):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def print(self):
        print(self.cond)
        print(self.body)

class ExprBinary(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def print(self):
        print(self.left)
        print(self.right)
