from myparser.myparser import Token

class ASTPrinter:
    def __init__(self):
        self.indent = 0
        
    def print(self,name,value):
        if type(value) is list:
            self.printArray(name,value)
        elif type(value) is Token:
            print("    "*self.indent + "{}  {}  {}  {}".format(name,value.__class__.__name__, value.type, value.value))
        elif value is None:
            pass
        elif type(value) is str:
            print("    " * self.indent + "{}".format(value))
        else:
            print("    "*self.indent + "{}  {}".format(name,value.__class__.__name__))
            self.indent += 1
            value.print(self)
            self.indent -= 1

    def printArray(self,name,value):
        counter = 0
        for x in value:
            self.print(name+" [{}]".format(counter), x)
            counter += 1