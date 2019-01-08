from enum import Enum
import sys
sys.path.append('../')
from meme_parser.parser import *

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
            Token.print()

    def isEof(self):
        if self.position == self.getLenght():
            return True
        else:
            return False

    def printError(self,message):
        print("{}.meme:{}:error:{}".format(sys.argv[1], self.line + 1,message),file=sys.stderr)    
    
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
        self.tokenList.append(self.reof())

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
            self.tokenList.append(self.rparenthesis())
        elif self.isBraces():
            self.tokenList.append(self.rbraces())
        elif self.isBrackets():
            self.tokenList.append(self.rbrackets())
        elif self.isComma():
            self.tokenList.append(self.rcomma())
        
    def isIdent(self):
        if self.getChar().isalpha():
            return True
        else:
            return False

    def isComma(self):
        if self.getChar() == ",":
            return True

    def isParenthesis(self):
        if self.getChar() == "(" or self.getChar() == ")":
            return True
    def isBrackets(self):
        if self.getChar() == "[" or self.getChar() == "]":
            return True
    def isBraces(self):
        if self.getChar() == "{" or self.getChar() == "}":
            return True
            
    def isWhiteSpace(self):
        if self.checkLenght() and self.inputstring[self.position] == "\n":
            self.tokenList.append(self.rnewline())
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

    def rcomma(self):
        if self.getChar() == ",":
            self.indentPosition()
            return Token(TokenType.comma,"",self.line)

    def rparenthesis(self):
        if self.getChar() == "(":
            self.indentPosition()
            return Token(TokenType.leftParenthesis,"",self.line)
        if self.getChar() == ")":
            self.indentPosition()
            return Token(TokenType.rightParenthesis,"",self.line)
    def rbrackets(self):
        if self.getChar() == "[":
            self.indentPosition()
            return Token(TokenType.leftBracket,"",self.line)
        if self.getChar() == "]":
            self.indentPosition()
            return Token(TokenType.rightBracket,"",self.line)

    def rbraces(self):
        if self.getChar() == "{":
            self.indentPosition()
            return Token(TokenType.leftBrace, "", self.line)
        if self.getChar() == "}":
            self.indentPosition()
            return Token(TokenType.rightBrace, "", self.line)

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
            self.printError("NO COMMENT TERMINATION FOUND")

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
        if self.getChar() == "=":
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
        esq =""
        self.indentPosition()
        try:
            while self.getChar() != "\"":
                if self.getChar() == "~":
                    esq += self.getChar()
                    self.appendToString()
                    esq += self.getChar()
                    if esq not in self.escapeSeq:
                        self.printError("UNKNOWN ESCAPE SEQUENCE")
                        sys.exit()
                    self.appendToString()
                else:
                    self.appendToString()
        except IndexError:
            self.printError("NO STRING TERMINATION FOUND")
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
            self.printError("INVALID SUFFIX AFTER FLOAT")
            sys.exit()
        while self.checkLenght() and self.getChar().isdigit():
            self.appendToString()
            if self.position == self.getLenght():
                break
            if self.getChar().isalpha() or self.getChar() == "_":
                self.printError("INVALID SUFFIX AFTER FLOAT")
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
                self.printError("INVALID SUFFIX AFTER INTEGER")
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
        if self.tempString in self. keywords:
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
