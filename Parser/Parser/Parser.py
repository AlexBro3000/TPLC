from Parser.Term import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def parsing(self):
        return SourceFile(self)
