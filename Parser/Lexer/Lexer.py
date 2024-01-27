import re

lexer_token_type = [
    ('comment', r'(?://.*?\n)|(?://.*(?!\n))|(?:/\*(?:.*?|\n)*?\*/)'),

    ('package', r'package(?![\_a-zA-Z\d])'),
    ('func', r'func(?![\_a-zA-Z\d])'),
    ('const', r'const(?![\_a-zA-Z\d])'),
    ('var', r'var(?![\_a-zA-Z\d])'),
    ('if', r'if(?![\_a-zA-Z\d])'),
    ('else', r'else(?![\_a-zA-Z\d])'),
    ('for', r'for(?![\_a-zA-Z\d])'),
    ('switch', r'switch(?![\_a-zA-Z\d])'),
    ('case', r'case(?![\_a-zA-Z\d])'),
    ('default', r'default(?![\_a-zA-Z\d])'),
    ('continue', r'continue(?![\_a-zA-Z\d])'),
    ('break', r'break(?![\_a-zA-Z\d])'),
    ('return', r'return(?![\_a-zA-Z\d])'),

    ('binaryop', r'(\|\|)|(&&)'),
    ('relop', r'(==)|(!=)|(<=)|(>=)|>|<'),
    ('increment', r'(\+\+)|(--)'),
    ('addop', r'\+|-'),
    ('mulop', r'\*|/|%'),
    ('unaryop', r'!'),
    ('equals', r'='),
    ('to_app', r':='),

    ('lbr', r'\('),
    ('rbr', r'\)'),
    ('lcbr', r'\{'),
    ('rcbr', r'\}'),
    ('lsbr', r'\['),
    ('rsbr', r'\]'),

    ('dot', r'\.'),
    ('comma', r','),
    ('colon', r':'),
    ('semicolon', r'(?:[;\n])+'),

    ('identifier', r'(?:[\_a-zA-Z](?:[\_a-zA-Z\d])*)'),
    ('float_lit', r'\d+(?:\.\d*)'),
    ('int_lit', r'0(?!\.)|[1-9]\d*(?!\.)'),
    ('string_lit', r'(?:\".*?\")|(?:\`(?:.*?|\n)*?\`)')
]

lexer_token_type_error = [
    ('identifier', ('int_lit', 'float_lit', 'string_lit'), "Incorrect identifier")
]


class Token:
    def __init__(self, code, token):
        self.code = code
        self.token = token

    def __repr__(self):
        return f"Token: {'{'} {self.code}: {self.token} {'}'}"

    def syntax_tree(self, shift=""):
        return f"{shift}{self.code}: {self.token}"


class Lexer:
    def __init__(self):
        self.token = None
        self.token_type = lexer_token_type
        self.token_type_error = lexer_token_type_error
        self.pos = None
        self.tokens = None

    def tokenization(self, source):
        tokens = []
        token_reg_ex = '|'.join('(?P<%s>%s)' % it for it in self.token_type)

        for it in re.finditer(token_reg_ex, source):
            code = it.lastgroup
            token = it.group(code)

            for i in self.token_type_error:
                if code == i[0] and len(tokens) != 0:
                    for j in i[1]:
                        if j == tokens[-1].code:
                            raise SyntaxError(f'{i[2]}: {tokens[-1].token + token}')

            token = Token(code, token.replace("\n", "\\n"))
            tokens.append(token)

        self.token = Token(None, None)
        self.pos = 0
        self.tokens = tokens
        return self.tokens

    def __next_token(self):
        self.pos += 1
        if self.pos >= len(self.tokens):
            return Token('EOF', None)
        return self.tokens[self.pos]

    def __last_token(self):
        self.pos -= 1
        if self.pos < 0:
            return Token('EOF', None)
        return self.tokens[self.pos]

    def curren_token(self):
        if self.pos < 0:
            return Token('EOF', None)
        if self.pos >= len(self.tokens):
            return Token('EOF', None)
        self.token = self.tokens[self.pos]
        return self.token

    def next_token(self):
        self.token = self.__next_token()
        return self.token

    def last_token(self):
        self.token = self.__last_token()
        return self.token

    def next(self):
        self.token = self.__next_token()

    def last(self):
        self.token = self.__last_token()
