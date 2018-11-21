from myParser.parserv2 import Token
class ASTPrinter:
    def __init__(self):
        indent = 0
        
    def print(self,name,value):
        if type(value) is list:
            self.printArray(name,value)
        elif type(value) is Token:
            print("{}  {}  {}  {}".format(name, value.__class__.__name__, value.type, value.value))
        elif value is None:
            print("empty")
        else:
            print("{}  {}".format(name,value.__class__.__name__))
            value.print(self)

    def printArray(self,name,value):
        for x in value:
            print("{}  {}".format(name, x.__class__.__name__))
            x.print(self)
    