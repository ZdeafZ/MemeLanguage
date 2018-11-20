from myParser.parser import *

class ASTPrinter:
    def __init__(self):
        indent = 0

    def print(self,node):
        node.print()