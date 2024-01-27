# Шаблонный узел
class Node:
    # Инициализация и обработка
    def __init__(self, parser):
        self.value = True
        self.data = []

    # Вывод данных
    def __repr__(self):
        if self.value:
            return f"{self.data}"
        else:
            return ""

    def is_if(token):
        return False

    def is_if_else(self, parser, fl_add, fl_frag, node, str):
        if self.value:
            if node.is_if(parser.lexer.curren_token()):
                node = node(parser)

                if (fl_frag == 0):
                    if fl_add:
                        self.data += [node]
                    return node
                if (fl_frag == 1):
                    if fl_add:
                        self.data += node.data
                    return node.data
                if (fl_frag == 2):
                    if fl_add:
                        self.data += node.data[0].data
                    return node.data[0].data

            else:
                self.LogError(parser, str)

    def syntax_tree(self, shift=""):
        return f"{shift}{self.data}"

    def LogInfo(self, node, info):
        pass

    # print(node, ":", info)

    def LogWarn(string, token):
        print(f"Warn: Expected '{string}', Received '{token.code} : {token.token}'")

    def LogError(self, parser, str):
        self.value = False
        self.data = []

        token = parser.lexer.curren_token()
        print(f"Error:Expected '{str}', Received '{token.code} : {token.token}'")


def Skip(parser):
    while True:
        token = parser.lexer.curren_token()
        if Semicolon.is_if(token):
            Semicolon(parser)
        elif Comment.is_if(token):
            Comment(parser)
        else:
            break


# Comment
class Comment(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "comment":
            self.value = True
            self.data = "comment"
            parser.lexer.next()
        else:
            Node.LogWarn("comment", token)

    def is_if(token):
        if token.code == "comment":
            return True
        else:
            return False


# Package
class Package(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "package":
            self.value = True
            self.data = "package"
            parser.lexer.next()
        else:
            Node.LogWarn("package", token)

    def is_if(token):
        if token.code == "package":
            return True
        else:
            return False


# Func
class Func(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "func":
            self.value = True
            self.data = "func"
            parser.lexer.next()
        else:
            Node.LogWarn("func", token)

    def is_if(token):
        if token.code == "func":
            return True
        else:
            return False


# Const
class Const(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "const":
            self.value = True
            self.data = "const"
            parser.lexer.next()
        else:
            Node.LogWarn("const", token)

    def is_if(token):
        if token.code == "const":
            return True
        else:
            return False


# Var
class Var(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "var":
            self.value = True
            self.data = "var"
            parser.lexer.next()
        else:
            Node.LogWarn("var", token)

    def is_if(token):
        if token.code == "var":
            return True
        else:
            return False


# If
class If(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "if":
            self.value = True
            self.data = "if"
            parser.lexer.next()
        else:
            Node.LogWarn("if", token)

    def is_if(token):
        if token.code == "if":
            return True
        else:
            return False


# Else
class Else(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "else":
            self.value = True
            self.data = "else"
            parser.lexer.next()
        else:
            Node.LogWarn("else", token)

    def is_if(token):
        if token.code == "else":
            return True
        else:
            return False


# For
class For(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "for":
            self.value = True
            self.data = "for"
            parser.lexer.next()
        else:
            Node.LogWarn("for", token)

    def is_if(token):
        if token.code == "for":
            return True
        else:
            return False


# Switch
class Switch(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "switch":
            self.value = True
            self.data = "switch"
            parser.lexer.next()
        else:
            Node.LogWarn("switch", token)

    def is_if(token):
        if token.code == "switch":
            return True
        else:
            return False


# Case
class Case(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "case":
            self.value = True
            self.data = "case"
            parser.lexer.next()
        else:
            Node.LogWarn("case", token)

    def is_if(token):
        if token.code == "case":
            return True
        else:
            return False


# Default
class Default(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "default":
            self.value = True
            self.data = "default"
            parser.lexer.next()
        else:
            Node.LogWarn("default", token)

    def is_if(token):
        if token.code == "default":
            return True
        else:
            return False


# Continue
class Continue(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "continue":
            self.value = True
            self.data = "continue"
            parser.lexer.next()
        else:
            Node.LogWarn("continue", token)

    def is_if(token):
        if token.code == "continue":
            return True
        else:
            return False


# Break
class Break(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "break":
            self.value = True
            self.data = "break"
            parser.lexer.next()
        else:
            Node.LogWarn("break", token)

    def is_if(token):
        if token.code == "break":
            return True
        else:
            return False


# Return
class Return(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "return":
            self.value = True
            self.data = "return"
            parser.lexer.next()
        else:
            Node.LogWarn("return", token)

    def is_if(token):
        if token.code == "return":
            return True
        else:
            return False


# BinaryOp
class BinaryOp(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "binaryop":
            self.value = True
            self.data = [token]
            parser.lexer.next()
        else:
            Node.LogWarn("binaryop", token)

    def is_if(token):
        if token.code == "binaryop":
            return True
        else:
            return False


# RelOp
class RelOp(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "relop":
            self.value = True
            self.data = [token]
            parser.lexer.next()
        else:
            Node.LogWarn("relop", token)

    def is_if(token):
        if token.code == "relop":
            return True
        else:
            return False


# Increment
class Increment(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "increment":
            self.value = True
            self.data = [token]
            parser.lexer.next()
        else:
            Node.LogWarn("increment", token)

    def is_if(token):
        if token.code == "increment":
            return True
        else:
            return False


# AddOp
class AddOp(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "addop":
            self.value = True
            self.data = [token]
            parser.lexer.next()
        else:
            Node.LogWarn("addop", token)

    def is_if(token):
        if token.code == "addop":
            return True
        else:
            return False


# MulOp
class MulOp(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "mulop":
            self.value = True
            self.data = [token]
            parser.lexer.next()
        else:
            Node.LogWarn("mulop", token)

    def is_if(token):
        if token.code == "mulop":
            return True
        else:
            return False


# UnaryOp
class UnaryOp(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "unaryop":
            self.value = True
            self.data = ["unaryop"]
            parser.lexer.next()
        else:
            Node.LogWarn("unaryop", token)

    def is_if(token):
        if token.code == "unaryop":
            return True
        else:
            return False


# Equals
class Equals(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "equals":
            self.value = True
            self.data = "equals"
            parser.lexer.next()
        else:
            Node.LogWarn("equals", token)

    def is_if(token):
        if token.code == "equals":
            return True
        else:
            return False


# To_App
class To_App(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "to_app":
            self.value = True
            self.data = "to_app"
            parser.lexer.next()
        else:
            Node.LogWarn("to_app", token)

    def is_if(token):
        if token.code == "to_app":
            return True
        else:
            return False


# LBR
class LBR(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "lbr":
            self.value = True
            self.data = ["lbr"]
            parser.lexer.next()
        else:
            Node.LogWarn("lbr", token)

    def is_if(token):
        if token.code == "lbr":
            return True
        else:
            return False


# RBR
class RBR(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "rbr":
            self.value = True
            self.data = ["rbr"]
            parser.lexer.next()
        else:
            Node.LogWarn("rbr", token)

    def is_if(token):
        if token.code == "rbr":
            return True
        else:
            return False


# LCBR
class LCBR(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "lcbr":
            self.value = True
            self.data = "lcbr"
            parser.lexer.next()
        else:
            Node.LogWarn("lcbr", token)

    def is_if(token):
        if token.code == "lcbr":
            return True
        else:
            return False


# RCBR
class RCBR(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "rcbr":
            self.value = True
            self.data = "rcbr"
            parser.lexer.next()
        else:
            Node.LogWarn("rcbr", token)

    def is_if(token):
        if token.code == "rcbr":
            return True
        else:
            return False


# LSBR
class LSBR(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "lsbr":
            self.value = True
            self.data = ["lsbr"]
            parser.lexer.next()
        else:
            Node.LogWarn("lsbr", token)

    def is_if(token):
        if token.code == "lsbr":
            return True
        else:
            return False


# RSBR
class RSBR(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "rsbr":
            self.value = True
            self.data = ["rsbr"]
            parser.lexer.next()
        else:
            Node.LogWarn("rsbr", token)

    def is_if(token):
        if token.code == "rsbr":
            return True
        else:
            return False


# Dot
class Dot(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "dot":
            self.value = True
            self.data = ["dot"]
            parser.lexer.next()
        else:
            Node.LogWarn("dot", token)

    def is_if(token):
        if token.code == "dot":
            return True
        else:
            return False


# Comma
class Comma(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "comma":
            self.value = True
            self.data = "comma"
            parser.lexer.next()
        else:
            Node.LogWarn("comma", token)

    def is_if(token):
        if token.code == "comma":
            return True
        else:
            return False


# Colon
class Colon(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "colon":
            self.value = True
            self.data = "colon"
            parser.lexer.next()
        else:
            Node.LogWarn("colon", token)

    def is_if(token):
        if token.code == "colon":
            return True
        else:
            return False


# Semicolon
class Semicolon(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "semicolon":
            self.value = True
            self.data = "semicolon"
            parser.lexer.next()
        else:
            Node.LogWarn("semicolon", token)

    def is_if(token):
        if token.code == "semicolon":
            return True
        else:
            return False


# Identifier
class Identifier(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "identifier":
            self.value = True
            self.data = [token]
            parser.lexer.next()
        else:
            Node.LogWarn("identifier", token)

    def is_if(token):
        if token.code == "identifier":
            return True
        else:
            return False


# Float_Lit
class Float_Lit(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "float_lit":
            self.value = True
            self.data = [token]
            parser.lexer.next()
        else:
            Node.LogWarn("float_lit", token)

    def is_if(token):
        if token.code == "float_lit":
            return True
        else:
            return False


# Int_Lit
class Int_Lit(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "int_lit":
            self.value = True
            self.data = [token]
            parser.lexer.next()
        else:
            Node.LogWarn("int_lit", token)

    def is_if(token):
        if token.code == "int_lit":
            return True
        else:
            return False


# String_Lit
class String_Lit(Node):
    def __init__(self, parser):
        self.value = False
        token = parser.lexer.curren_token()
        if token.code == "string_lit":
            self.value = True
            self.data = [token]
            parser.lexer.next()
        else:
            Node.LogWarn("string_lit", token)

    def is_if(token):
        if token.code == "string_lit":
            return True
        else:
            return False
