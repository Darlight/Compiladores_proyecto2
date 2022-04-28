"""
Universidad del Valle de Guatemala
Node.py
Proposito: Representacion de Diferentes tipos de nodes
Mario Perdomo 18029
"""
# == Kleene ==
class Kleene:
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return '{ ' + f'{self.a}' + ' }'

# == Brackets [] ==
class Bracket:
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return f'[ {self.a} ]'

# == OR ==
class Or:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'({self.a}) | ({self.b})'
        # return f'{self.a} | {self.b}'

# == Append  ==
class Append:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        # return f'({self.a} . {self.b})'
        return f'{self.a} . {self.b}'

# == Symbol AKA variable ==
class Symbol:
    def __init__(self, value, type_=None, ident_name=None):
        self.value = value
        self.type = type_
        self.ident_name = ident_name

    def __repr__(self):
        if self.ident_name:
            return f'{self.ident_name}'
        return f'{self.value}'

