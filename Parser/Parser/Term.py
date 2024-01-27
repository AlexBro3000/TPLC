from Lexer.Lexer import Token
from Parser.SimpleTerm import *


class SourceFile(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, True, 0, PackageClause, "PackageClause")
        self.is_if_else(parser, False, 0, Semicolon, "Semicolon")
        Skip(parser)
        while True:
            if TopLevelDecl.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, True, 0, TopLevelDecl, "TopLevelDecl")
                if parser.lexer.curren_token().code != "EOF":
                    self.is_if_else(parser, False, 0, Semicolon, "Semicolon")
                    Skip(parser)
                if not self.value:
                    parser.lexer.next()
            else:
                self.LogInfo("SourceFile:       ", self.data)
                if parser.lexer.curren_token().code == "EOF":
                    print("- * PARSING - OK")
                else:
                    print("- * PARSING - FALSE")
                break

    def syntax_tree(self, shift=""):
        if self.value:
            res = f"{self.data[0].syntax_tree(shift)}\n"
            step = 1
            while (step < len(self.data)):
                res += f"{self.data[step].syntax_tree(shift)}\n"
                step += 1
            return res


class PackageClause(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, False, 0, Package, "Package")
        self.is_if_else(parser, True, 1, Identifier, "Identifier")
        self.LogInfo("PackageClause:    ", self.data)

    def syntax_tree(self, shift=""):
        if self.value:
            res = f"{shift}Пакетирование: {self.data[0].token}"
            return res

    def is_if(token):
        return Package.is_if(token)


class TopLevelDecl(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        if Declaration.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, Declaration, "Declaration")
        elif FunctionDecl.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, FunctionDecl, "FunctionDecl")
        else:
            self.LogError(parser, "Declaration | FunctionDecl")
        self.LogInfo("TopLevelDecl:     ", self.data)

    def syntax_tree(self, shift=""):
        if self.value:
            res = f"{self.data[0].syntax_tree(shift)}"
            return res

    def is_if(token):
        return Declaration.is_if(token) | FunctionDecl.is_if(token)


class Declaration(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        if ConstDecl.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, ConstDecl, "ConstDecl")
        elif VarDecl.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, VarDecl, "VarDecl")
        else:
            self.LogError(parser, "ConstDecl | VarDecl")
        self.LogInfo("Declaration:      ", self.data)

    def is_if(token):
        return ConstDecl.is_if(token) | VarDecl.is_if(token)


class Type(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        if Identifier.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, Identifier, "Identifier")
        elif ArrayType.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, ArrayType, "ArrayType")
        # elif FunctionType.is_if(parser.lexer.curren_token()):
        # 	self.is_if_else(parser, True, 0, FunctionType, "FunctionType")
        elif LBR.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, False, 0, LBR, "LBR")
            self.is_if_else(parser, True, 1, Type, "Type")
            self.is_if_else(parser, False, 0, RBR, "RBR")
        self.LogInfo("Type:             ", self.data)

    def syntax_tree(self, shift=""):
        if self.value:
            if isinstance(self.data[0], Token):
                res = f"{shift}Type: {self.data[0].token}"
            else:
                res = f"{self.data[0].syntax_tree(shift)}"
            return res

    def is_if(token):
        return Identifier.is_if(token) | ArrayType.is_if(token) | LBR.is_if(token)


class ArrayType(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, False, 0, LSBR, "LSBR")
        self.is_if_else(parser, True, 0, Expression, "Expression")
        self.is_if_else(parser, False, 0, RSBR, "RSBR")
        if Identifier.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, Type, "Type")
        else:
            self.is_if_else(parser, True, 2, Type, "Type")
        self.LogInfo("ArrayType:        ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "| "
        if self.value:
            res = f"{shift}Type:  {self.data[-1].token}\n"
            res += f"{shift}Array: "
            step = 1
            while (step < len(self.data)):
                res += f"{self.data[step - 1].syntax_tree()}"
                if (step + 1 < len(self.data)):
                    res += f" ; "
                step += 1
            return res

    def is_if(token):
        return LSBR.is_if(token)


# FunctionType
# "func" Signature
# class FunctionType(Node):
# 	def __init__(self, parser):
# 		self.value = True
# 		self.data  = []

# 		self.is_if_else(parser, False, 0, Func, "Func")
# 		self.is_if_else(parser, True,  0, Signature, "Signature")

# 	def is_if(token):
# 		return Func.is_if(token)


class Signature(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, False, 0, LBR, "LBR")
        if ParameterList.is_if(parser.lexer.curren_token()):
            self.data += [1]
            self.is_if_else(parser, True, 0, ParameterList, "ParameterList")
        self.is_if_else(parser, False, 0, RBR, "RBR")
        if Type.is_if(parser.lexer.curren_token()):
            self.data += [2]
            self.is_if_else(parser, True, 0, Type, "Type")
        self.LogInfo("Signature:        ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "| "
        if self.value:
            if (len(self.data) > 0 and self.data[0] == 1):
                res = f"{shift}Входные:  (\n"
                res += f"{self.data[1].syntax_tree(shift + str_shift)}\n"
                res += f"{shift})\n"
            else:
                res = f"{shift}Входные:  ( )\n"
            if (len(self.data) > 2 and self.data[2] == 2):
                res += f"{shift}Выходные: (\n"
                res += f"{self.data[3].syntax_tree(shift + str_shift)}\n"
                res += f"{shift})"
            elif (len(self.data) > 0 and self.data[0] == 2):
                res += f"{shift}Выходные: (\n"
                res += f"{self.data[1].syntax_tree(shift + str_shift)}\n"
                res += f"{shift})"
            else:
                res += f"{shift}Выходные: ( )"
            return res

    def is_if(token):
        return LBR.is_if(token)


class ParameterList(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, True, 0, ParameterDecl, "ParameterDecl")
        while True:
            if Comma.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, False, 0, Comma, "Comma")
                self.is_if_else(parser, True, 0, ParameterDecl, "ParameterDecl")
            else:
                break
        self.LogInfo("ParameterList:    ", self.data)

    def syntax_tree(self, shift=""):
        if self.value:
            res = f"{self.data[0].syntax_tree(shift)}"
            step = 1
            while (step < len(self.data)):
                res += f"\n"
                res += f"{self.data[step].syntax_tree(shift)}"
                step += 1
            return res

    def is_if(token):
        return ParameterDecl.is_if(token)


class ParameterDecl(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, True, 0, IdentifierList, "IdentifierList")
        self.is_if_else(parser, True, 0, Type, "Type")
        self.LogInfo("ParameterDecl:    ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "| "
        if self.value:
            res = f"{self.data[1].syntax_tree(shift)}\n"
            res += f"{self.data[0].syntax_tree(shift + str_shift)}"
            return res

    def is_if(token):
        return IdentifierList.is_if(token) | Type.is_if(token)


class ConstDecl(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, False, 0, Const, "Const")
        self.is_if_else(parser, True, 1, Identifier, "Identifier")
        if Type.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, Type, "Type")
        self.is_if_else(parser, False, 0, Equals, "Equals")
        self.is_if_else(parser, True, 0, Expression, "Expression")
        self.LogInfo("ConstDecl:        ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "| "
        if self.value:
            res = f"{shift}Const: {self.data[0].token}\n"
            res += f"{self.data[1].syntax_tree(shift + str_shift)}"
            if (len(self.data) == 3):
                res += f"\n"
                res += f"{self.data[2].syntax_tree(shift + str_shift)}"
            return res

    def is_if(token):
        return Const.is_if(token)


class VarDecl(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, False, 0, Var, "Var")
        self.is_if_else(parser, True, 1, Identifier, "Identifier")
        if Type.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, Type, "Type")
        self.is_if_else(parser, False, 0, Equals, "Equals")
        self.is_if_else(parser, True, 0, Expression, "Expression")
        self.LogInfo("VarDecl:          ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "| "
        if self.value:
            res = f"{shift}Var:   {self.data[0].token}\n"
            res += f"{self.data[1].syntax_tree(shift + str_shift)}"
            if (len(self.data) == 3):
                res += f"\n"
                res += f"{self.data[2].syntax_tree(shift + str_shift)}"
            return res

    def is_if(token):
        return Var.is_if(token)


class FunctionDecl(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, False, 0, Func, "Func")
        self.is_if_else(parser, True, 1, Identifier, "Identifier")
        self.is_if_else(parser, True, 0, Signature, "Signature")
        self.is_if_else(parser, True, 0, Block, "Block")
        self.LogInfo("FunctionDecl:     ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "|\t"
        if self.value:
            res = f"{shift}Функция: {self.data[0].token}\n"
            res += f"{shift}| Параметры: (\n"
            res += f"{self.data[1].syntax_tree(shift + str_shift)}\n"
            res += f"{shift}| )\n"
            res += f"{shift}| Блок: {'{'}\n"
            res += f"{self.data[2].syntax_tree(shift + str_shift)}\n"
            res += f"{shift}| {'}'}"
            return res

    def is_if(token):
        return Func.is_if(token)


class IdentifierList(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, True, 1, Identifier, "Identifier")
        while True:
            if Comma.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, False, 0, Comma, "Comma")
                self.is_if_else(parser, True, 1, Identifier, "Identifier")
            else:
                break
        self.LogInfo("IdentifierList:   ", self.data)

    def syntax_tree(self, shift=""):
        if self.value:
            res = f"{self.data[0].syntax_tree(shift)}"
            step = 1
            while (step < len(self.data)):
                res += f", {self.data[step].syntax_tree()}"
                step += 1
            return res

    def is_if(token):
        return Identifier.is_if(token)


class ExpressionList(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, True, 0, Expression, "Expression")
        while True:
            if Comma.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, False, 0, Comma, "Comma")
                self.is_if_else(parser, True, 0, Expression, "Expression")
            else:
                break
        self.LogInfo("ExpressionList:   ", self.data)

    def syntax_tree(self, shift=""):
        if self.value:
            res = f"{self.data[0].syntax_tree(shift)}"
            step = 1
            while (step < len(self.data)):
                res += f", {self.data[step].syntax_tree()}"
                step += 1
            return res

    def is_if(token):
        return Expression.is_if(token)


class Block(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, False, 0, LCBR, "LCBR")
        self.is_if_else(parser, True, 1, StatementList, "StatementList")
        self.is_if_else(parser, False, 0, RCBR, "RCBR")
        self.LogInfo("Block:            ", self.data)

    def syntax_tree(self, shift=""):
        if self.value:
            res = f""
            step = 0
            while (step < len(self.data)):
                res += f"{self.data[step].syntax_tree(shift)}"
                if (step + 1 < len(self.data)):
                    res += f"\n"
                step += 1
            return res

    def is_if(token):
        return LCBR.is_if(token)


class StatementList(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        Skip(parser)
        while True:
            if Statement.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, True, 0, Statement, "Statement")
                self.is_if_else(parser, False, 0, Semicolon, "Semicolon")
                Skip(parser)
            else:
                break
        self.LogInfo("StatementList:    ", self.data)

    def syntax_tree(self, shift=""):
        if self.value:
            res = f""
            step = 0
            while (step < len(self.data)):
                res += f"{self.data[step].syntax_tree(shift)}"
                if (step + 1 < len(self.data)):
                    res += f"\n"
                step += 1
            return res

    def is_if(token):
        return Semicolon.is_if(token) | Comment.is_if(token) | Statement.is_if(token)


class Operand(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        if Identifier.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, Identifier, "Identifier")
        elif Int_Lit.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, Int_Lit, "Int_Lit")
        elif Float_Lit.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, Float_Lit, "Float_Lit")
        elif String_Lit.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, String_Lit, "String_Lit")
        elif LBR.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, LBR, "LBR")
            self.is_if_else(parser, True, 0, Expression, "Expression")
            if self.value and (len(self.data[1].data) <= 1):
                self.data[1] = self.data[1].data[0]
            self.is_if_else(parser, True, 1, RBR, "RBR")
        self.LogInfo("Operand:          ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "  "
        if self.value:
            if len(self.data) == 1:
                res = super().syntax_tree(shift)
            else:
                res = f"{shift}(\n"
                res += f"{self.data[1].syntax_tree(shift + str_shift)}\n"
                res += f"{shift})"
            return res

    def is_if(token):
        return Identifier.is_if(token) | Int_Lit.is_if(token) | Float_Lit.is_if(token) | String_Lit.is_if(
            token) | LBR.is_if(token)


class PrimaryExpr(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, True, 0, Operand, "Operand")
        if self.value and (len(self.data[0].data) <= 1):
            self.data[0] = self.data[0].data[0]
        while True:
            if Dot.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, True, 1, Dot, "Dot")
                self.is_if_else(parser, True, 1, Identifier, "Identifier")
            elif LSBR.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, True, 1, LSBR, "LSBR")
                self.is_if_else(parser, True, 0, Expression, "Expression")
                if self.value and (len(self.data[-1].data) <= 1):
                    self.data[-1] = self.data[-1].data[0]
                self.is_if_else(parser, True, 1, RSBR, "RSBR")
            elif LBR.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, True, 1, LBR, "LBR")
                if ExpressionList.is_if(parser.lexer.curren_token()):
                    self.is_if_else(parser, True, 0, ExpressionList, "ExpressionList")
                self.is_if_else(parser, True, 1, RBR, "RBR")
            else:
                break
        self.LogInfo("PrimaryExpr:      ", self.data)

    def syntax_tree(self, shift=""):
        if self.value:
            res = f"{self.data[0].syntax_tree(shift)}"

            step = 1
            while (step < len(self.data)):
                if (self.data[step] == "dot"):
                    str_shift = ". "
                    res += f"\n"
                    res += f"{self.data[step + 1].syntax_tree(shift + str_shift)}"
                    step += 2
                elif (self.data[step] == "lsbr"):
                    str_shift = "  "
                    res += f" [\n"
                    res += f"{self.data[step + 1].syntax_tree(shift + str_shift)}\n"
                    res += f"{shift + str_shift}]"
                    step += 3
                elif (self.data[step] == "lbr"):
                    str_shift = "  "
                    if (self.data[step + 1] == "rbr"):
                        res += f" ( )"
                        step += 2
                    else:
                        res += f" (\n"
                        res += f"{self.data[step + 1].syntax_tree(shift + str_shift)}\n"
                        res += f"{shift + str_shift})"
                        step += 3
            return res

    def is_if(token):
        return Operand.is_if(token)


class Expression(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, True, 0, UnaryExpr, "UnaryExpr")
        if self.value and (len(self.data[0].data) <= 1):
            self.data[0] = self.data[0].data[0]
        if Expression.is_if(parser.lexer.next_token()):
            parser.lexer.last()
            if BinaryOp.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, True, 1, BinaryOp, "BinaryOp")
                self.is_if_else(parser, True, 1, Expression, "Expression")
            elif RelOp.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, True, 1, RelOp, "RelOp")
                self.is_if_else(parser, True, 1, Expression, "Expression")
            elif AddOp.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, True, 1, AddOp, "AddOp")
                elem = self.is_if_else(parser, True, 1, Expression, "Expression")
            elif MulOp.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, True, 1, MulOp, "MulOp")
                self.is_if_else(parser, True, 1, Expression, "Expression")
        else:
            parser.lexer.last()
        self.LogInfo("Expression:       ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "  "
        if self.value:
            if (len(self.data) == 1):
                res = f"{self.data[0].syntax_tree(shift)}"
            elif (len(self.data) == 3):
                res = f"{shift}{self.data[1]}\n"
                res += f"{self.data[0].syntax_tree(shift + str_shift)}\n"
                res += f"{self.data[2].syntax_tree(shift + str_shift)}"
            else:
                res = f"{self.data[0].syntax_tree(shift)}"
                step = 1
                while (step < len(self.data)):
                    res += f"\n"
                    res += f"{shift + str_shift}{self.data[step]}\n"
                    res += f"{self.data[step + 1].syntax_tree(shift)}"
                    step += 2
            return res

    def is_if(token):
        return UnaryExpr.is_if(token)


class UnaryExpr(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        if PrimaryExpr.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, PrimaryExpr, "PrimaryExpr")
            if self.value and (len(self.data[0].data) <= 1):
                self.data[0] = self.data[0].data[0]
        elif AddOp.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, AddOp, "AddOp")
            self.is_if_else(parser, True, 1, UnaryExpr, "UnaryExpr")
        elif UnaryOp.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, UnaryOp, "UnaryOp")
            self.is_if_else(parser, True, 1, UnaryExpr, "UnaryExpr")
        else:
            self.LogError(parser, "PrimaryExpr | AddOp | UnaryOp")
        self.LogInfo("UnaryExpr:        ", self.data)

    def syntax_tree(self, shift=""):
        if self.value:
            res = f"{shift}"
            step = 0
            while (step + 1 < len(self.data)):
                if isinstance(self.data[step], str):
                    res += f"{self.data[step]} "
                else:
                    res += f"{self.data[step].token} "
                step += 1
            res += f"({self.data[-1].syntax_tree()})"
            return res

    def is_if(token):
        return PrimaryExpr.is_if(token) | AddOp.is_if(token) | UnaryOp.is_if(token)


class Statement(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        if Declaration.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, Declaration, "Declaration")
        elif SimpleStmt.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, SimpleStmt, "SimpleStmt")
        elif Continue.is_if(parser.lexer.curren_token()):
            self.data += ["Continue"]
            self.is_if_else(parser, False, 0, Continue, "Continue")
        elif Break.is_if(parser.lexer.curren_token()):
            self.data += ["Break"]
            self.is_if_else(parser, False, 0, Break, "Break")
        elif Return.is_if(parser.lexer.curren_token()):
            self.data += ["Return"]
            self.is_if_else(parser, False, 0, Return, "Return")
            if Expression.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, True, 0, Expression, "Expression")
        elif IfStmt.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, IfStmt, "IfStmt")
        elif SwitchStmt.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, SwitchStmt, "SwitchStmt")
        elif ForStmt.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, ForStmt, "ForStmt")
        elif Block.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 0, Block, "Block")
        else:
            self.LogError(parser,
                          "Declaration | SimpleStmt | Continue | Break | Return | IfStmt | SwitchStmt | ForStmt | Block")
        self.LogInfo("Statement:        ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "| "
        if self.value:
            if isinstance(self.data[0], Node):
                res = f"{self.data[0].syntax_tree(shift)}"
            else:
                res = f"{shift}{self.data[0]}"
                if (len(self.data) == 2):
                    res += f"\n"
                    res += f"{self.data[1].syntax_tree(shift + str_shift)}"
            return res

    def is_if(token):
        return Declaration.is_if(token) | SimpleStmt.is_if(token) | Continue.is_if(token) | Break.is_if(
            token) | Return.is_if(token) | IfStmt.is_if(token) | SwitchStmt.is_if(token) | ForStmt.is_if(
            token) | Block.is_if(token)


class SimpleStmt(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, True, 0, Expression, "Expression")
        self.option = 1
        if Increment.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, Increment, "Increment")
            self.option = 2
        elif Assign_Op.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, True, 1, Assign_Op, "Assign_Op")
            Skip(parser)
            self.is_if_else(parser, True, 0, Expression, "Expression")
            self.option = 3
        elif To_App.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, False, 0, To_App, "To_App")
            Skip(parser)
            self.is_if_else(parser, True, 0, Expression, "Expression")
            self.option = 4
        self.LogInfo("SimpleStmt:       ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = ".\t"
        if self.value:
            if self.option == 1:
                res = f"{self.data[0].syntax_tree(shift)}"
            elif self.option == 2:
                res = f"{self.data[0].syntax_tree(shift)}{self.data[1].token}"
            elif self.option == 3:
                res = f"{self.data[0].syntax_tree(shift)} {self.data[1]}\n"
                res += f"{self.data[2].syntax_tree(shift + str_shift)}"
            elif self.option == 4:
                res = f"{self.data[0].syntax_tree(shift)} :=\n"
                res += f"{self.data[1].syntax_tree(shift + str_shift)}"
            return res
        else:
            return None

    def is_if(token):
        return Expression.is_if(token)


class Assign_Op(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        if AddOp.is_if(parser.lexer.curren_token()) or MulOp.is_if(parser.lexer.curren_token()):
            if AddOp.is_if(parser.lexer.curren_token()):
                elem = self.is_if_else(parser, False, 1, AddOp, "AddOp")
                self.is_if_else(parser, False, 0, Equals, "Equals")
            else:
                elem = self.is_if_else(parser, False, 1, MulOp, "MulOp")
                self.is_if_else(parser, False, 0, Equals, "Equals")
            if self.value:
                self.data = [f"{elem[0].token}="]
        else:
            self.is_if_else(parser, False, 0, Equals, "Equals")
            if self.value:
                self.data = [f"="]
        self.LogInfo("Assign_Op:        ", self.data)

    def is_if(token):
        return AddOp.is_if(token) | MulOp.is_if(token) | Equals.is_if(token)


class IfStmt(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []
        self.count = 0

        self.is_if_else(parser, False, 0, If, "If")
        self.is_if_else(parser, True, 0, Expression, "Expression")
        self.is_if_else(parser, True, 1, Block, "Block")
        if Else.is_if(parser.lexer.curren_token()):
            self.is_if_else(parser, False, 0, Else, "Else")

            if IfStmt.is_if(parser.lexer.curren_token()):
                self.data += ['elif']
                elem = self.is_if_else(parser, False, 0, IfStmt, "IfStmt")
                self.data += elem.data
                self.count += elem.count + 1
            elif Block.is_if(parser.lexer.curren_token()):
                self.data += ['else']
                elem = self.is_if_else(parser, True, 1, Block, "Block")
                self.count += 1
            else:
                self.LogError(parser, "IfStmt | Block")
        self.LogInfo("IfStmt:           ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "|\t"
        if self.value:
            res = f"{shift}Ветвление: if: \n"
            res += f"{shift}| Параметры: (\n"
            res += f"{self.data[0].syntax_tree(shift + str_shift)}\n"
            res += f"{shift}| )\n"
            res += f"{shift}| Блок {'{'}\n"
            if len(self.data) > 1 and not isinstance(self.data[1], str):
                res += f"{self.data[1].syntax_tree(shift + str_shift)}\n"
                step = 2
            else:
                step = 1
            res += f"{shift}| {'}'}"

            for i in range(self.count):
                res += f"\n"
                if self.data[step] == 'elif':
                    res += f"{shift}Ветвление: elif\n"
                    res += f"{shift}| Параметры: (\n"
                    res += f"{self.data[step + 1].syntax_tree(shift + str_shift)}\n"
                    res += f"{shift}| )\n"
                    res += f"{shift}| Блок {'{'}\n"
                    if len(self.data) > step + 2 and not isinstance(self.data[step + 2], str):
                        res += f"{self.data[step + 2].syntax_tree(shift + str_shift)}\n"
                        step += 3
                    else:
                        step += 2
                    res += f"{shift}| {'}'}"
                else:
                    res += f"{shift}Ветвление: else\n"
                    res += f"{shift}| Блок {'{'}\n"
                    if len(self.data) > step + 1 and not isinstance(self.data[step + 1], str):
                        res += f"{self.data[step + 1].syntax_tree(shift + str_shift)}\n"
                    res += f"{shift}| {'}'}"
                    break
            return res

    def is_if(token):
        return If.is_if(token)


class SwitchStmt(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []
        self.count = 0

        self.is_if_else(parser, False, 0, Switch, "Switch")
        self.is_if_else(parser, True, 0, Expression, "Expression")
        self.is_if_else(parser, False, 0, LCBR, "LCBR")
        Skip(parser)
        while True:
            if ExprCaseClause.is_if(parser.lexer.curren_token()):
                self.is_if_else(parser, True, 0, ExprCaseClause, "ExprCaseClause")
                Skip(parser)
                self.count += 1
            else:
                break
        self.is_if_else(parser, False, 0, RCBR, "RCBR")
        self.LogInfo("SwitchStmt:       ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "|\t"
        if self.value:
            res = f"{shift}Ветвление: switch: (\n"
            res += f"{self.data[0].syntax_tree(shift + str_shift)}\n"
            res += f"{shift}| )\n"
            res += f"{shift}| Блок {'{'}\n"
            for i in range(self.count):
                res += f"{self.data[i + 1].syntax_tree(shift + str_shift)}\n"
            res += f"{shift}| {'}'}"
            return res

    def is_if(token):
        return Switch.is_if(token)


class ExprCaseClause(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        if Case.is_if(parser.lexer.curren_token()):
            if self.value:
                self.data = ['case']
            self.is_if_else(parser, False, 0, Case, "Case")
            self.is_if_else(parser, True, 0, ExpressionList, "ExpressionList")
        elif Default.is_if(parser.lexer.curren_token()):
            if self.value:
                self.data = ['default']
            self.is_if_else(parser, False, 0, Default, "Default")
        else:
            self.LogError(parser, "Case | Default")
        self.is_if_else(parser, False, 0, Colon, "Colon")
        self.is_if_else(parser, True, 0, StatementList, "StatementList")
        self.LogInfo("ExprCaseClause:   ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "|\t"
        if self.value:
            if self.data[0] == 'case':
                res = f"{shift}Case: (\n"
                res += f"{self.data[1].syntax_tree(shift + str_shift)}\n"
                res += f"{shift}| )\n"
            else:
                res = f"{shift}Default:\n"
            res += f"{shift}| Блок: {'{'}\n"
            res += f"{self.data[-1].syntax_tree(shift + str_shift)}\n"
            res += f"{shift}| {'}'}"
            return res

    def is_if(token):
        return Case.is_if(token) | Default.is_if(token)


class ForStmt(Node):
    def __init__(self, parser):
        self.value = True
        self.data = []

        self.is_if_else(parser, True, 0, For, "For")
        self.is_if_else(parser, True, 0, SimpleStmt, "SimpleStmt")
        if Semicolon.is_if(parser.lexer.curren_token()):
            if self.value:
                self.data[0] = 'for'
            self.is_if_else(parser, False, 0, Semicolon, "Semicolon")
            self.is_if_else(parser, True, 0, SimpleStmt, "SimpleStmt")
            self.is_if_else(parser, False, 0, Semicolon, "Semicolon")
            self.is_if_else(parser, True, 0, SimpleStmt, "SimpleStmt")
        else:
            if self.value:
                self.data[0] = 'while'
        self.is_if_else(parser, True, 1, Block, "Block")
        self.LogInfo("ForStmt:          ", self.data)

    def syntax_tree(self, shift=""):
        str_shift = "|\t"
        if self.value:
            res = f"{shift}Цикл: {self.data[0]}\n"
            res += f"{shift}| Параметры: (\n"
            if self.data[0] == 'for':
                res += f"{self.data[1].syntax_tree(shift + str_shift)}\n"
                res += f"{self.data[2].syntax_tree(shift + str_shift)}\n"
                res += f"{self.data[3].syntax_tree(shift + str_shift)}\n"
                res += f"{shift}| )\n"
            else:
                res += f"{self.data[1].syntax_tree(shift + str_shift)}\n"
                res += f"{shift}| )\n"
            res += f"{shift}| Блок: {'{'}\n"
            res += f"{self.data[-1].syntax_tree(shift + str_shift)}\n"
            res += f"{shift}| {'}'}"
            return res

    def is_if(token):
        return For.is_if(token)
