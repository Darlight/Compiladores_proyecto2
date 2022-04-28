"""
Universidad del Valle de Guatemala
token.py
Proposito: Token
Mario Perdomo 18029
"""
from Attribute import Attribute, Vartype
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


