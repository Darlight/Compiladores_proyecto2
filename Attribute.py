"""
Universidad del Valle de Guatemala
Attribute.py
Proposito: Selector de elemento de un file ATG
Mario Perdomo 18029
"""
# ===== Most important Class =====
# Assigns the attribute with its value and own identifier
from regex import R


class Attribute:
    def __init__(self, identifier, val) -> None:
        self.identifier = identifier
        self.val = val
    def __repr__(self) -> str:
        return f'{self.identifier} = {self.value}'
# ===== Classifier Class =====
# A
class Vartype(str):
    IDENTIFIER = 0
    STRING = 1 
    CHAR = 2
    NUMBER = 3
    UNION = 4 
    DIFF = 5
    RANGE = 6
    APPEND = 7
    L_KLEENE = 8
    R_KLEENE = 9 
    L_PAREN = 10 
    R_PAREN = 11
    L_BRACK = 12
    R_BRACK = 13 
    OR = 14
