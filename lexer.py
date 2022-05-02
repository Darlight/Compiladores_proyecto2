"""
Universidad del Valle de Guatemala
lexer.py
Proposito: Lexema/leyenda de los inputs ingresados
Mario Perdomo 18029
"""
from token import Token

class Lexer:
    def __init__(self,pattern):
        self.source = pattern
        self.symbols = {'(':'LEFT', ')':'RIGHT', '*':'STAR', '|':'ALT', '\x08':'CONCAT', '+':'PLUS', '?':'QMARK'}
        self.current = 0
        self.length = len(self.source)
       
    def get_token(self): 
        #Se va incrementando el estado de manera que sea mayor al patron
        if self.current < self.length:
            c = self.source[self.current]
            self.current += 1
            if c not in self.symbols.keys(): # CHAR [a-z]
                token = Token('CHAR', c)
            else:
                token = Token(self.symbols[c], c)
            return token
        else:
            return Token('NONE', '')