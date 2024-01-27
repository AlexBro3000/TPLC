import Lexer.Lexer as Lexer
import Parser.Term as Term


class Generator:
    def __init__(self, result_parsing):
        self.data = result_parsing.data

    def generate(self):
        data = self.data
        res = self.generator(data, "", "")
        return res

    def generator(self, data, res, before):
        res = ""
        for element in data:
            res = res + before
            if isinstance(element, Term.TopLevelDecl):
                res = res + self.g(element.data, res, before)
                continue
            if isinstance(element, Term.Statement):
                res = res + self.g(element.data, res, before) + "\n"
                continue
        res = res.replace("||", " or ")
        res = res.replace("&&", " and ")
        return res

    def g(self, data, res, before):
        res = ""
        for element in data:
            if isinstance(element, Term.Expression):
                res = res + Expression(element) + "\n"
                continue

            if isinstance(element, Term.ConstDecl) or isinstance(element, Term.VarDecl):
                if len(element.data) == 2 and isinstance(element.data[1], Term.Type):
                    tmp = "None"
                else:
                    tmp = Expression(element.data[-1])

                if isinstance(element.data[1].data[0], Term.ArrayType):
                    res = res + Token(element.data[0]) + " = "
                    step = 2
                    while len(element.data[1].data[0].data) >= step:
                        t = tmp
                        for i in range(1, int(element.data[1].data[0].data[len(element.data[1].data[0].data) - step].data[0].token)):
                            tmp += ", " + t
                        tmp = "[" + tmp + "]"
                        step += 1
                    res = res + tmp + "\n"
                else:
                    res = res + Token(element.data[0]) + " = " + tmp + "\n"
                continue

            if isinstance(element, Term.FunctionDecl):
                res = res + "def " + Token(element.data[0]) + "("
                if len(element.data[1].data) == 0:
                    res = res + "):\n"
                    res = res + self.generator(element.data[2].data, res, before + "\t")
                else:
                    res = res + ParameterList(element.data[1].data[1]) + "):\n"
                    res = res + self.generator(element.data[2].data, res, before + "\t")

            if isinstance(element, Term.SimpleStmt):
                if len(element.data) == 1:
                    if type(element.data[0]) == str:
                        res = res + element.data[0]
                    res = res + Expression(element.data[0])
                elif len(element.data) == 2:
                    if isinstance(element.data[0], Term.Expression) and isinstance(element.data[1], Lexer.Token):
                        res = res + Expression(element.data[0]) + element.data[1].token
                        continue
                    res = res + Expression(element.data[0]) + " = " + Expression(element.data[1])
                elif len(element.data) == 3:
                    res = res + Expression(element.data[0]) + " " + element.data[1] + " " + Expression(element.data[2])
                continue

            if isinstance(element, Term.IfStmt):
                res = res + "if "
                for el in element.data:
                    if isinstance(el, Term.Statement):
                        dat = [el]
                        res = res + self.generator(dat, res, before + "\t")
                    elif isinstance(el, Term.Expression):
                        res = res + Expression(el) + ":\n"
                    elif type(el) == str:
                        if el == "else":
                            res = res + before + "else:\n"
                        elif el == "elif":
                            res = res + before + "elif "

            if isinstance(element, Term.SwitchStmt):
                res = res + "match " + Expression(element.data[0]) + ":\n"
                for i in range(1, len(element.data)):
                    if element.data[i].data[0] == "case":
                        res = res + before + "\tcase " + ExpressionList(element.data[i].data[1]) + ":\n"
                        for st in element.data[i].data[2].data:
                            res = res + self.generator([st], res, before + "\t\t")
                    if element.data[i].data[0] == "default":
                        res = res + before + "\tcase _:\n"
                        for st in element.data[i].data[1].data:
                            res = res + self.generator([st], res, before + "\t\t")
                continue

            if isinstance(element, Term.ForStmt):
                simple_stmts = []
                for i in range(len(element.data)):
                    if isinstance(element.data[i], Term.SimpleStmt):
                        simple_stmts.append(element.data[i])
                if len(simple_stmts) == 1:
                    res = res + "while " + Expression(simple_stmts[0]) + ":\n"
                elif len(simple_stmts) == 3:
                    third = ""
                    if (isinstance(simple_stmts[2].data[1], Lexer.Token)):
                        if (simple_stmts[2].data[1].token == "++"):
                            third = "1"
                        else:
                            third = "-1"
                    else:
                        if (simple_stmts[2].data[1] == "+="):
                            third = "+"+Expression(simple_stmts[2].data[2])
                        else:
                            third = "-"+Expression(simple_stmts[2].data[2])
                    res = res + "for " + Expression(simple_stmts[0].data[0]) + " in range(" + Expression(simple_stmts[0].data[1]) + ", " + simple_stmts[1].data[0].data[2].token +", "+third + "):\n"
                for el in element.data:
                    if isinstance(el, Term.Statement):
                        dat = [el]
                        res = res + self.generator(dat, res, before + "\t")

            if type(element) == str:
                res = res + Str(element)
                continue

        return res


def ExpressionList(expression_list):
    res = ""
    for i in range(len(expression_list.data)):
        res = res + Expression(expression_list.data[i])
        if i != len(expression_list.data) - 1:
            res = res + ", "
    return res


def ParameterList(parameter_list):
    res = ""
    if len(parameter_list.data) == 1:
        if isinstance(parameter_list.data[0], Lexer.Token):
            return ""
        for i in range(len(parameter_list.data[0].data[0].data)):
            res = res + parameter_list.data[0].data[0].data[i].token
            if i != len(parameter_list.data[0].data[0].data) - 1:
                res = res + ", "
    else:
        for i in range(len(parameter_list.data)):
            vars = ""
            for k in range(len(parameter_list.data[i].data[0].data)):
                vars = vars + parameter_list.data[i].data[0].data[k].token
                if (k != len(parameter_list.data[i].data[0].data)-1):
                    vars = vars + ", "
            res = res + vars
            if i != len(parameter_list.data) - 1:
                res = res + ", "
    return res


def Token(token):
    return token.token


def Str(elem):
    res = ""
    if elem == "lbr":
        res = res + "("
    elif elem == "rbr":
        res = res + ")"
    elif elem == "lsbr":
        res = res + "["
    elif elem == "rsbr":
        res = res + "]"
    elif elem == "dot":
        res = res + "."
    elif elem == "unaryop":
        res = res + "not "
    elif elem == "Continue":
        res = res + "continue"
    elif elem == "Break":
        res = res + "break"
    elif elem == "Return":
        res = res + "return "
    else:
        res = res + elem
    return res


def Expression(expression):
    res = ""
    for elem in expression.data:
        if isinstance(elem, Lexer.Token):
            if Token(elem) == "Print" or Token(elem) == "Println":
                res = res + "print"
            else:
                res = res + Token(elem)
        elif type(elem) == str:
            res = res + Str(elem)
        elif isinstance(elem, Term.ExpressionList):
            res = res + ExpressionList(elem)
        else:
            res = res + Expression(elem)
    return res