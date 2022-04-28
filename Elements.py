"""
Universidad del Valle de Guatemala
Elements.py
Proposito: Clasificacion de gramatica lexica
Mario Perdomo 18029
"""
from Attribute import Attribute, Vartype 
from dataclasses import dataclass
# ==== Character ====
# Manages the chars from arg archives
class Character(Attribute):
    def __init__(self, identifier, value):
        super().__init__(identifier, value)


class Keyword(Attribute):
    def __init__(self, identifier, value):
        super().__init__(identifier, value)


# ==== Variable ====
# Assigns the chars from the character class to their respective 
# type and value
@dataclass
class Variable:
    type: Vartype
    value: any = None
    name: str = None

    def __repr__(self):
        if self.name:
            return f'{self.type.name}: {self.name}'
        return self.type.name + (f':{self.value}' if self.value != None else '')