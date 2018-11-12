from enum import Enum
import sys
class States(Enum):
    eof = -1
    initial = 0
    identifier = 1
    keyword = 2
    literal = 3
    operator = 4
    parenthesis = 5
    comment = 6
    float = 7;
class Lexer:
    def __init__(self, inputstring, keywords, operators):
        self.inputstring = inputstring
        self.keywords = keywords
        self.operators = operators
        self.line = 0
        self.position = 0
        self.currentState = States.initial
        self.tempString = ""
    tokenList = []
    escapeSeq = {"~n" : "\n", "~t" : "\t", "~\"" : "\""}
    def printTokens(self):
        print("|       {:22}       |        {:15}       |  {:5}  |".format("TYPE", "VALUE","LINE"))
        print("-------------------------------------------------------------------------------".format("TYPE", "VALUE", "LINE"))
        for Token in self.tokenList:
            if not(Token is None):
                Token.print()

    def isEof(self):
        if self.position == self.getLenght():
            return True
        else:
            return False

    def getChar(self):
        return self.inputstring[self.position]

    def getLenght(self):
        return len(self.inputstring)
        
    def checkLenght(self):
        return self.position < len(self.inputstring)

    def appendToString(self):
        self.tempString += self.getChar()
        self.position += 1

    def indentPosition(self):
        self.position += 1

    def indentLine(self):
        self.line += 1

    def run(self):
        while not self.isEof():
            self.parse()

    def parse(self):
        if self.position == len(self.inputstring):
            self.tokenList.append(self.reof())
        elif self.isIdent():
            self.tokenList.append(self.rindentifier())
            self.tempString = ""
        elif self.isWhiteSpace():
            pass
        elif self.isLiteral():
            self.tokenList.append(self.rliteral())
            self.tempString = ""
        elif self.isOperator():
            self.tokenList.append(self.roperator())
            self.tempString = ""
        elif self.isParenthesis():
            if self.currentState == States.parenthesis:
                self.tokenList.append(self.rparenthesis())
        elif self.position == len(self.inputstring):
            self.tokenList.append(self.reof())
        
    def isIdent(self):
        if self.getChar().isalpha():
            return True
        else:
            return False
    
    def isParenthesis(self):
        if self.getChar() == "(" or self.getChar() == ")":
            return True
            
    def isWhiteSpace(self):
        if self.checkLenght() and self.inputstring[self.position] == "\n":
            self.rnewline()
            return True
        if self.checkLenght() and self.inputstring[self.position] == " ":
            self.rspace()
            return True

    def isOperator(self):
        if self.inputstring[self.position] in self.operators:
            return True

    def isLiteral(self):
        if self.getChar() == "\"":
            return True
        elif self.getChar().isdigit():
            return True
        else:
            return False

    def reof(self):
        return Token(TokenType.endOfFile,"",self.line)

    def rparenthesis(self):
        if self.getChar() == "(":
            self.indentPosition()
            return Token(TokenType.leftParenthesis,"",self.line)
        if self.getChar() == ")":
            self.indentPosition()
            return Token(TokenType.rightParenthesis,"",self.line)
            
    def rcomment(self):
        commentString = ""
        try:
            while True:
                commentString += self.getChar()
                if self.getChar() == "\n":
                    self.indentLine()
                self.indentPosition()
                if "comment_end" in commentString:
                    break
        except IndexError:
            print("{}.meme:{}:error:NO TERMINATING SYMBOL".format(sys.argv[1], self.line + 1))

    def roperator(self):
        if self.getChar() == "<":
            self.appendToString()
            if self.checkLenght() and self.getChar() == "=":
                self.appendToString()
                return Token(TokenType.lessThanOrEqual,"",self.line)
            return Token(TokenType.lessThan,"", self.line)
        if self.getChar() == ">":
            self.appendToString()
            if self.position < self.getLenght() and self.getChar() == "=":
                self.appendToString()
                return Token(TokenType.greaterThanOrEqual,"",self.line)
            return Token(TokenType.greaterThan, "", self.line)
        if self.getChar() == "!":
            self.appendToString()
            if self.checkLenght() and self.getChar() == "=":
                self.appendToString()
                return Token(TokenType.notEqual,"",self.line)
            return Token(TokenType.notSomething, "", self.line)
        if  self.getChar() == "=":
            self.appendToString()
            if self.checkLenght() and self.getChar() == "=":
                self.appendToString()
                return Token(TokenType.equal,"",self.line)
            return Token(TokenType.assign, "", self.line)
        if self.getChar() == "+":
            self.indentPosition()
            return Token(TokenType.plus, "", self.line)
        if self.getChar() == "-":
            self.indentPosition()
            if self.getChar() == ">":
                self.indentPosition()
                return Token(TokenType.assign,"",self.line)
            return Token(TokenType.minus, "", self.line)
        if self.getChar() == "*":
            self.indentPosition()
            return Token(TokenType.mult, "", self.line)
        if self.getChar() == "/":
            self.indentPosition()
            return Token(TokenType.div, "", self.line)

    def rliteral(self):
        while self.checkLenght():
            if self.getChar() == "\"":
                return self.rstring()
            if self.getChar().isdigit():
                return self.rint()

    def rstring(self):
                self.indentPosition()
                try:
                    while self.getChar() != "\"":
                        if self.getChar() == "~":
                            self.appendToString()
                            self.appendToString()
                        else:
                            self.appendToString()
                except IndexError:
                    print("{}.meme:{}:error:NO TERMINATING SYMBOL".format(sys.argv[1], self.line + 1))
                else:
                    self.indentPosition()
                    counter = 0
                    for x in self.tempString:
                        if x == "~n" or x == "\n":
                            self.indentLine()
                            counter += 1
                    memeString = self.tempString
                    for x in self.escapeSeq:
                        memeString = memeString.replace(x,self.escapeSeq[x])
                    return Token(TokenType.stringLiteral, memeString , self.line-counter)

    def rfloat(self):
        if self.getChar() == "-":
            self.appendToString()
        if not self.getChar().isdigit():
            print("{}.meme:{}:error:UNIDENTIFIED LITERAL".format(sys.argv[1], self.line + 1))
            sys.exit()
        while self.checkLenght() and self.getChar().isdigit():
            self.appendToString()
            if self.position == self.getLenght():
                break
            if self.getChar().isalpha() or self.getChar() == "_":
                print("{}.meme:{}:error:UNIDENTIFIED LITERAL".format(sys.argv[1], self.line + 1))
                sys.exit()
        return Token(TokenType.floatLiteral, self.tempString,self.line)

    def rint(self):
        while self.checkLenght() and self.getChar().isdigit():
            self.appendToString()
            if self.position == self.getLenght():
                break

            if self.getChar() == "." or self.getChar() == "e":
                self.appendToString()
                return self.rfloat()
            if self.getChar().isalpha() or self.getChar() == "_":
                print("{}.meme:{}:error:UNIDENTIFIED LITERAL".format(sys.argv[1], self.line + 1))
                sys.exit()
        return Token(TokenType.integerLiteral, self.tempString, self.line)

    def rnewline(self):
        self.indentLine()
        self.indentPosition()
        return Token(TokenType.newLine, "", self.line-1)

    def rindentifier(self):
        while self.checkLenght():
            if not(self.getChar().isalpha() or self.getChar().isdigit() or self.getChar() == "_"):
                break
            else:
                self.appendToString()
        if self.tempString in keywordList:
            return Token(TokenType.keyword,self.tempString, self.line)
        elif self.tempString == "truth" or self.tempString == "lie":
            return Token(TokenType.booleanLiteral, self.tempString, self.line)
        elif self.tempString == "and":
            return Token(TokenType.logicalAnd,"", self.line)
        elif self.tempString == "comment_start":
            self.rcomment()
        elif self.tempString == "or":
            return Token(TokenType.logicalOr,"", self.line)
        else:
            return Token(TokenType.identifier, self.tempString, self.line)

    def rspace(self):
        self.indentPosition()


class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def print(self):
        print("|       {:22}       |        {:15}       |{:5}    |".format(self.type.upper(),self.value,self.line+1))


class TokenType:

    identifier = "IDENTIFIER"
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
    newLine = "new_line"
    endOfFile = "end_of_file"
    commentStart = "comment_start"
    commentEnd = "comment_end"

try:
    with open("{}.meme".format(str(sys.argv[1])), "r") as file:
        string = file.read()
except:
    print("File you are trying to lex was not found. Exiting")
    sys.exit()
with open ("keywords.txt", "r") as file:
    keywordList = file.read().split(",")
with open ("operators.txt", "r") as file:
    operatorList = file.read().split(",")

lexer = Lexer(string, keywordList, operatorList)
lexer.run()
lexer.printTokens()