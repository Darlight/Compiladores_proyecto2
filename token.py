"""
Universidad del Valle de Guatemala
token.py
Proposito: Token
Mario Perdomo 18029
"""
from Attribute import Attribute, Vartype
from pickle_utils import GetElementType
import codecs
# ===== Token =====
# Depending on the attribute, it creates a token
# with its own name and value

class Token(Attribute):
    def __init__(self, name, value, type = None):
        super().__init__(self, name, value)
        self.type = type

    def __repr__(self):
        if self.type != None:
            return f'{self.name}  :  {self.value} -> {self.context}'
        return f'{self.name}  :  {self.value}'


class TokenExpression:
    def __init__(self, set_, idents):
        self.set = iter(set_)
        self.idents = idents
        self.curr_char = None
        self.prev_char = None
        self.last_char = None
        self.symbol_ignore = ['(', '[', '{', '|']
        self.closing_symbols = ['{', '(', '[']
        self.curr_set = set_
        self.Next()

    def Next(self):
        try:
            if self.curr_char == ' ' and self.prev_char == '|':
                self.last_char = self.prev_char
                self.prev_char = '.'
            else:
                self.last_char = self.prev_char
                self.prev_char = self.curr_char

            self.curr_char = next(self.set)
        except StopIteration:
            self.curr_char = None

    def Parse(self, token_id=None):
        while self.curr_char != None:

            # curr_char is a letter
            if self.curr_char.isalpha():
                if self.prev_char and \
                        self.prev_char not in self.symbol_ignore and \
                        self.last_char not in self.symbol_ignore:

                    yield Attribute(Vartype.APPEND)
                yield self.GenerateWord()

            # curr_char is a char or string
            elif self.curr_char == '\'' or self.curr_char == '"':
                if self.prev_char and \
                        self.prev_char not in self.symbol_ignore and \
                        self.last_char not in self.symbol_ignore:

                    yield Attribute(Vartype.APPEND)
                res = self.GenerateVar(self.curr_char)
                for var in res:
                    yield var

            # curr_char is a closing symbol
            elif self.curr_char in self.closing_symbols:
                if self.prev_char and \
                        self.prev_char not in self.symbol_ignore and \
                        self.last_char not in self.symbol_ignore:

                    yield Attribute(Vartype.APPEND)

                if self.curr_char == '{':
                    yield Attribute(Vartype.L_KLEENE)
                elif self.curr_char == '[':
                    yield Attribute(Vartype.L_BRACK)
                elif self.curr_char == '(':
                    yield Attribute(Vartype.L_PAREN)

                self.Next()

            # curr_char is kleene expr.
            elif self.curr_char == '}':
                self.Next()
                yield Attribute(Vartype.R_KLEENE)

            elif self.curr_char == ']':
                self.Next()
                yield Attribute(Vartype.R_BRACK)

            elif self.curr_char == ')':
                self.Next()
                yield Attribute(Vartype.R_PAREN)

            elif self.curr_char == '|':
                self.Next()
                yield Attribute(Vartype.OR)

            elif self.curr_char == ' ':
                self.Next()
                continue

            else:
                raise Exception(f'Invalid character: {self.curr_char}')

        if token_id != None:
            yield Attribute(Vartype.APPEND, '.')
            yield Attribute(Vartype.STRING, f'#-{token_id}')

    def GenerateWord(self):
        word = self.curr_char
        self.Next()

        while self.curr_char != None \
                and self.curr_char.isalnum() and self.curr_char != ' ':
            word += self.curr_char
            self.Next()

        res = GetElementType(word, self.idents)
        if not res:
            raise Exception(
                f'Invalid ident: {word} in expression "{self.curr_set}"')

        return res

    def GenerateVar(self, symbol_type):
        var = self.curr_char
        self.Next()

        while self.curr_char != None:
            var += self.curr_char
            self.Next()

            if self.curr_char == symbol_type:
                var += self.curr_char
                self.Next()
                break

        if var.count(symbol_type) != 2:
            raise Exception(f'Expected {symbol_type} for set')

        var = var.replace(symbol_type, '')
        if symbol_type == '\'':
            try:
                char = codecs.decode(var, 'unicode_escape')
                ord_ = ord(char)
            except:
                raise Exception(f'Unvalid char in Generate var: {var}')

            return [Attribute(Vartype.CHAR, set(chr(ord_)))]

        elif symbol_type == '\"':
            res = list()
            for char in var:
                res.append(Attribute(Vartype.STRING, set(char)))
                res.append(Attribute(Vartype.APPEND, '.'))

            if self.last_char not in self.closing_symbols:
                res.pop()
            return res

