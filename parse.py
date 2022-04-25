"""
Universidad del Valle de Guatemala
CC----
thompson.py
Proposito: Orden y consumo de los inputs
"""
from lexer import Lexer
from token import Token

class Parser:
    def __init__(self, pattern):
        self.lexer = Lexer(pattern)
        self.tokens = []
        self.next_token = self.lexer.get_token()
        
    def parse(self):
        self.exp()
        return self.tokens
    
    def consume(self, name):
        if self.next_token.name == name:
            self.next_token = self.lexer.get_token()
        elif self.next_token.name != name:
            pass
    #orden de jerarquia, los parentesis son priorirdad #1
    def primary(self):
        if self.next_token.name == 'LEFT':
            self.consume('LEFT')
            self.exp()
            self.consume('RIGHT')
        elif self.next_token.name == 'CHAR':
            self.tokens.append(self.next_token)
            self.consume('CHAR')
    #Esto permite que vaya leyendo la expresion desde el primer parentesis
    # ademas, 
    def term(self):
        self.factor()
        if self.next_token.value not in ')|':
            self.term()
            self.tokens.append(Token('CONCAT', '\x08'))
        
    def exp(self):
        self.term()
        if self.next_token.name == 'ALT':
            t = self.next_token # t = token
            self.consume('ALT')
            self.exp()
            self.tokens.append(t)

    
    def factor(self):
        self.primary()
        # Las divisiones para cada AFN se clasifican desde aqui
        if self.next_token.name in ['STAR', 'PLUS', 'QMARK']:
            self.tokens.append(self.next_token)
            self.consume(self.next_token.name)

    