
"""
Universidad del Valle de Guatemala
token.py
Proposito: Sets encontrados adentro de cada corchete o parentesis
Mario Perdomo 18029
"""

from pickle_utils import GetCharValue, GetElementType
from Attribute import Vartype
from Elements import Variable
class SetDecl:
    def __init__(self, set_, idents):
        self.set = iter(set_)
        self.idents = idents
        self.curr_char = None
        self.curr_set = set_
        self.valid_alnum = ['(', ')']
        self.Next()

    def Next(self):
        try:
            self.curr_char = next(self.set)
        except StopIteration:
            self.curr_char = None

    def Set(self):
        while self.curr_char != None:

            # curr_char is a letter
            if self.curr_char.isalpha():
                yield self.GenerateWord()

            # curr_char is a char or string
            elif self.curr_char == '\'' or self.curr_char == '"':
                yield self.GenerateVar(self.curr_char)

            elif self.curr_char == '+':
                self.Next()
                yield Variable(Vartype.UNION)

            elif self.curr_char == '-':
                self.Next()
                yield Variable(Vartype.DIFF)

            elif self.curr_char == '.':
                self.Next()
                if self.curr_char == '.':
                    self.Next()
                    yield Variable(Vartype.RANGE)
                else:
                    raise Exception(
                        f'Invalid dot found in set: {self.curr_set}')

            elif self.curr_char == ' ':
                self.Next()

    def GenerateWord(self):
        word = self.curr_char
        self.Next()

        while self.curr_char != None \
                and (self.curr_char.isalnum() or self.curr_char in self.valid_alnum) \
                and self.curr_char != ' ':
            word += self.curr_char
            self.Next()

        if 'CHR(' in word:
            res = GetCharValue(word)
            
            res = Variable(Vartype.CHAR, set(res))
        else:
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

        res = GetElementType(var, self.idents)

        if not res:
            raise Exception(f'Invalid var: {var}')

        return res


class SetGenerator:
    def __init__(self, set_, idents):
        self.set = iter(set_)
        self.idents = idents
        self.curr_var = None
        self.prev_var = None
        self.res_set = None
        self.curr_set = set_
        self.Next()

    def Next(self):
        try:
            self.prev_var = self.curr_var
            self.curr_var = next(self.set)
        except StopIteration:
            self.curr_var = None

        if not self.res_set:
            self.res_set = self.curr_var.value

    def GenerateSet(self):
        while self.curr_var != None:

            if self.curr_var.type == Vartype.UNION:
                self.NewSet('UNION')
                self.Next()

            elif self.curr_var.type == Vartype.DIFF:
                self.NewSet('DIFFERENCE')
                self.Next()

            elif self.curr_var.type == Vartype.RANGE:
                self.NewRange()
                self.Next()

            else:
                self.Next()

        return self.res_set

    def NewSet(self, op):
        self.Next()

        if self.curr_var.value == None:
            Exception(f'Unvalid set declaration')

        curr_set = self.curr_var.value

        if op == 'UNION':
            self.res_set = self.res_set.union(curr_set)
        elif op == 'DIFFERENCE':
            self.res_set = self.res_set.difference(curr_set)

    def NewRange(self):
        char1 = self.prev_var
        self.Next()
        char2 = self.curr_var

        if char1.type != Vartype.CHAR or char2.type != Vartype.CHAR:
            raise Exception(
                f'Unvalid char range found in {self.curr_set}')

        # We gotta .pop since the value is a set of 1 item
        range1 = ord(char1.value.pop())
        range2 = ord(char2.value.pop())

        if range1 > range2:
            range1, range2 = range2, range1

        # Create a new list with all the chars in the range
        char_range = set([chr(char)
                          for char in range(range1, range2 + 1)])

        self.res_set.update(char_range)
