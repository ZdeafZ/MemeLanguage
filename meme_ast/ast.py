import sys
import meme_codegen.generate_code as code_gen
import meme_utils.current_stack_slot as stack
stringMap = {}
currentStringConstant = 0
mainIndex = 0
noErrors = True


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


aritOperators = [
    TokenType.plus,
    TokenType.minus,
    TokenType.mult,
    TokenType.div
]

logicalOperators = [
    TokenType.logicalAnd,
    TokenType.logicalOr
]
relationOperators = [
    TokenType.greaterThan,
    TokenType.greaterThanOrEqual,
    TokenType.lessThanOrEqual,
    TokenType.lessThan,
]
equalityOperators = [
    TokenType.equal,
    TokenType.notEqual
]


def get_error_found_status():
    return noErrors


def print_not_in_loop_error(instruction, line):
    global noErrors
    noErrors = False
    print("{}.meme:{}:error:{} not in loop".format(sys.argv[1], line+1, instruction),
          file=sys.stderr)


def print_main_not_found_error(line):
    global noErrors
    noErrors = False
    print("{}.meme:{}:error:main function not found".format(sys.argv[1], line+1),
          file=sys.stderr)


def print_mismatch_error(type1, type2, line=None):
    temp1 = None
    temp2 = None
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
    line = type1.type.line + 1
    global noErrors
    noErrors = False
    print("{}.meme:{}:error:type mismatch: {} vs {}".format(sys.argv[1], line,
                                                            temp1, temp2),
          file=sys.stderr)


def print_invalid_operation_error(line):
    global noErrors
    noErrors = False
    print("{}.meme:{}:error:invalid binary operation".format(sys.argv[1], line +1),
          file=sys.stderr)


def print_void_error(type):
    global noErrors
    noErrors = False
    print("{}.meme:{}:error:type cannot be Nothing".format(sys.argv[1], type.type.line +1),
          file=sys.stderr)


def print_boolean_error(type):
    global noErrors
    noErrors = False
    print("{}.meme:{}:error:type cannot be Boolean".format(sys.argv[1], type.type.line +1),
          file=sys.stderr)


def print_args_mismatch_error(params_count, args_count, target):
    global noErrors
    noErrors = False
    print("{}.meme:{}:error:invalid argument count: {} vs {}".format(sys.argv[1], target.name.line + 1
                                                                     , params_count, args_count),
          file=sys.stderr)


def print_main_args_mismatch_error(params_count, args_count, line):
    global noErrors
    noErrors = False
    print("{}.meme:{}:error:invalid argument count: {} vs {}".format(sys.argv[1], line
                                                                     , params_count, args_count),
          file=sys.stderr)


def print_not_a_call_error(line):
    global noErrors
    noErrors = False
    print("{}.meme:{}:error:not a call".format(sys.argv[1], line + 1),
          file=sys.stderr)


def print_not_a_variable_error(line):
    global noErrors
    noErrors = False
    print("{}.meme:{}:error:not a variable".format(sys.argv[1], line + 1),
          file=sys.stderr)


def unify_types(type1, type2, line=None):
    if type(type1) != type(type2):
        print_mismatch_error(type1, type2, line)
        return False
    else:
        return True


class Node:
    def __init__(self):
        self.parent = None

    def print(self,p):
        p.print("CLASS NOT IMPLEMENTED")

    def resolve_names(self, scope):
        print("not implemented for {}".format(self.__class__.__name__))

    def check_types(self):
        print("not implemented for {}".format(self.__class__.__name__))

    def add_children(self, value):
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

    def generate_code(self, w):
        print("not implemented for class {}", self.__class__.__name__)


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
        self.entry_label = code_gen.Label()

    def print(self,p):
        p.print("Type",self.type)
        p.print("Name",self.name)
        p.print("Args",self.params)
        p.print("Body",self.funcbody)

    def resolve_names(self,scope):
        import meme_parser.parser as parser
        inner_scope = parser.Scope(scope)
        stack.current_stack_slot = 0
        for args in self.params:
            inner_scope.add(args.name, args)
        self.funcbody.resolve_names(inner_scope)
        self.local_variables = stack.current_stack_slot

    def check_types(self):
        self.funcbody.check_types()

    def generate_code(self, w):
        w.place_label(self.entry_label)
        w.write("ALLOC", self.local_variables)
        self.funcbody.generate_code(w)
        w.write("RET")


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

    def generate_code(self, w):
        global mainIndex
        if mainIndex == -1:
            sys.exit()
        counter = 0
        for function in self.functions:
            if counter == mainIndex:
                w.write("PUSH_DUM",function.entry_label)
                w.write("CALL",len(function.params))
                w.write("PRNT") 
                w.write("EXIT")
            function.generate_code(w)
            if counter == mainIndex:
                counter += 1
            
    def check_main(self):
        global mainIndex
        mainIndex = -1
        counter = 0
        for function in self.functions:
            if function.name.value == "main":
                if unify_types(function.type,TypeInt(None)):
                    if len(function.params) == 0: 
                        mainIndex = counter
                        break
                    else:
                        print_main_args_mismatch_error(len(function.params), 0, function.name.line + 1)
            counter += 1
        if mainIndex == -1:
            print_main_not_found_error(0)
        return mainIndex
            

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

    def generate_code(self, w):
        if self.expr is not None:
            self.expr.generate_code(w)


class ExprPriority(Expr):
    def __init__(self, exprs, parent=None):
        self.exprs = exprs
        self.add_children(self.exprs)
        self.parent = parent

    def print(self ,p):
        p.print("Expression",self.exprs)

    def resolve_names(self,scope):
        self.exprs.resolve_names(scope)

    def check_types(self):
        self.exprs.check_types()

    def generate_code(self, w):
        self.exprs.generate_code(w)


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
            if self.lit.value not in stringMap:
                global currentStringConstant
                stringMap[self.lit.value] = currentStringConstant
                currentStringConstant += 1
            return TypeString(self.lit)
        elif self.lit.type == TokenType.booleanLiteral:
            return TypeBoolean(self.lit)

    def generate_code(self, w):
        if self.lit.type == TokenType.integerLiteral:
            w.write("PUSH",int(self.lit.value))
        elif self.lit.type == TokenType.booleanLiteral:
            if self.lit.value == "truth":
                w.write("PUSH", 1)
            elif self.lit.value == "lie":
                w.write("PUSH", 0)
        elif self.lit.type == TokenType.stringLiteral:
            w.write("PUSH", stringMap[self.lit.value])


class ExprVar(Expr):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def print(self,p):
        p.print("Name",self.name)

    def resolve_names(self,scope):
        self.target = scope.resolve(self.name)

    def check_types(self):
        if (type(self.target) is StmtDeclaration or type(self.target) is Arg) and self.target is not None:
            return self.target.type
        else:
            print_not_a_variable_error(self.name.line)

    def generate_code(self, w):
        if hasattr(self.target,"stack_slot"):
            w.write("PEEK", self.target.stack_slot)
        else:
            w.write("PEEK", "ERROR")

class Arg(Node):
    def __init__(self, type, name, parent=None):
        self.type = type
        self.add_children(type)
        self.name = name
        self.parent = parent
        self.stack_slot = 0


    def print(self,p):
        p.print("Arg Type", self.type)
        p.print("Name", self.name)


class Stmt(Node):
    pass


class Branch(Stmt):
    def __init__(self, cond, body, parent=None):
        self.cond = cond
        self.add_children(self.cond)
        self.body = body
        self.add_children(self.body)
        self.parent = parent
        self.last = False

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

    def generate_code(self, w):
        self.start_label = w.new_label_placed()
        self.end_label = w.new_label()
        self.cond.generate_code(w)
        w.write("BZ", self.end_label)
        self.body.generate_code(w)
        if self.last == True and self.parent.body is None:
            pass
        else:
            w.write("BR", self.parent.final_label)
        w.place_label(self.end_label)

class StmtBlock(Stmt):
    def __init__(self, parent=None):
        self.stmts = []
        self.parent = parent

    def appendStmt(self,stmt):
        self.stmts.append(stmt)
        self.add_children(stmt)

    def print(self,p):
        p.print("Stmts", self.stmts)

    def resolve_names(self, scope):
        import meme_parser.parser as parser
        inner_scope = parser.Scope(scope)
        for stmt in self.stmts:
            stmt.resolve_names(inner_scope)

    def check_types(self):
        for stmt in self.stmts:
            stmt.check_types()

    def generate_code(self, w):
        for stmt in self.stmts:
            stmt.generate_code(w)


class StmtExpr(Stmt):
    def __init__(self, expr, parent=None):
        self.expr = expr
        self.parent = parent

    def print(self,p):
        p.print("Expression", self.expr)

    def resolve_names(self, scope):
        if self.expr is not None:
            self.expr.resolve_names(scope)

    def check_types(self):
        if self.expr is not None:
            return self.expr.check_types()

    def generate_code(self, w):
        if self.expr is not None:
            self.expr.generate_code(w)


class StmtReturn(Stmt):
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent

    def print(self,p):
        p.print("Return Value",self.value)

    def resolve_names(self, scope):
        if self.value is not None:
            self.value.resolve_names(scope)

    def check_types(self):
        if self.value is not None:
            value_type = self.value.check_types()
        else:
            value_type = TypeNothing(self.value)
        ret_type = self.ancestor_fn().type
        if value_type is not None:
            unify_types(value_type, ret_type)

    def generate_code(self, w):
        if self.value is not None:
            self.value.generate_code(w)
            w.write("RET_V")
        else:
            w.write("RET")


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
            print_not_in_loop_error("continue", self.token.line)

    def generate_code(self, w):
        w.write("BR", self.ancestor_loop().start_label)


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

    def generate_code(self, w):
        self.final_label = w.new_label()
        for branch in self.branches:
            if branch == self.branches[len(self.branches)-1]:
                branch.last = True
            branch.generate_code(w)
        if self.body is not None:
            self.body.generate_code(w)
            w.place_label(self.final_label)
        else:
            w.place_label(self.final_label)

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
            print_not_in_loop_error("break", self.token.line)

    def generate_code(self, w):
        w.write("BR",self.ancestor_loop().end_label)


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

    def generate_code(self, w):
        self.start_label = w.new_label_placed()
        self.cond.generate_code(w)
        self.end_label = w.new_label()
        w.write("BZ", self.end_label)
        self.body.generate_code(w)
        w.write("BR", self.start_label)
        w.place_label(self.end_label)


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

    def generate_code(self, w):
        self.right.generate_code(w)
        w.write("POKE",self.target.stack_slot)

class StmtDeclaration(Stmt):
    def __init__(self,type,name,operator,right,parent=None):
        self.type = type
        self.add_children(self.type)
        self.name = name
        self.operator = operator
        self.right = right
        self.parent = parent
        self.stack_slot = 0

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

    def generate_code(self, w):
        self.right.generate_code(w)
        w.write("POKE",self.target.stack_slot)


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
        unify_types(left_type,right_type)
        return left_type

    def generate_code(self, w):
        self.left.generate_code(w)
        self.right.generate_code(w)
        if self.operator.type == TokenType.greaterThan:
            w.write("GR")
        elif self.operator.type == TokenType.greaterThanOrEqual:
            w.write("GREQ")
        elif self.operator.type == TokenType.lessThan:
            w.write("LS")
        elif self.operator.type == TokenType.lessThanOrEqual:
            w.wirte("LSEQ")
        elif self.operator.type == TokenType.plus:
            w.write("ADD")
        elif self.operator.type == TokenType.minus:
            w.write("SUB")
        elif self.operator.type == TokenType.div:
            w.write("DIV")
        elif self.operator.type == TokenType.mult:
            w.write("MULT")
        elif self.operator.type == TokenType.logicalAnd:
            w.write("AND")
        elif self.operator.type == TokenType.logicalOr:
            w.write("OR")
        elif self.operator.type == TokenType.equal:
            w.write("EQ")
        elif self.operator.type == TokenType.notEqual:
            w.write("NEQ")
        else:
            print_invalid_operation_error(self.operator.line)


class ExprBinaryArithmetic(ExprBinary):
    def __init__(self, left, operator, right, parent=None):
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
        if type(left_type) == TypeNothing:
            print_void_error(left_type)
        if type(right_type) == TypeNothing:
            print_void_error(right_type)
        if type(left_type) == TypeBoolean:
            print_boolean_error(left_type)
        if type(right_type) == TypeBoolean:
            print_boolean_error(right_type)
        unify_types(left_type, right_type)
        return left_type


class ExprBinaryLogical(ExprBinary):
    def __init__(self, left, operator, right, parent=None):
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
        unify_types(left_type, TypeBoolean(None))
        unify_types(right_type, TypeBoolean(None))
        return TypeBoolean(None)


class ExprBinaryEquality(ExprBinary):
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
        if type(left_type) != TypeNothing and type(right_type) != TypeNothing:
            unify_types(left_type, right_type)
        if type(left_type) == TypeNothing:
            print_void_error(left_type)
        if type(right_type) == TypeNothing:
            print_void_error(right_type)
        return TypeBoolean(None)


class ExprBinaryRelational(ExprBinary):
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
        if left_type != TypeNothing(None) and right_type != TypeNothing(None):
            unify_types(left_type, right_type)
        if left_type == TypeNothing(None):
            print_void_error(left_type)
        if right_type == TypeNothing(None):
            print_void_error(right_type)
        return TypeBoolean(None)


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
                print_args_mismatch_error(params_count, args_count, self.target)

            mininum = min(params_count, args_count)
            for i in range (0,mininum):
                param_type = self.target.params[i].type
                arg_type = self.args[i].check_types()
                unify_types(param_type, arg_type)
            return self.target.type
        else:
            print_not_a_call_error(self.name.line)

    def generate_code(self, w):
        if hasattr(self.target,"entry_label"):
            w.write("PUSH_DUM", self.target.entry_label)
        else:
            w.write("PUSH_DUM", -1)

        for arg in self.args:
            arg.generate_code(w)
        w.write("CALL",len(self.args))
