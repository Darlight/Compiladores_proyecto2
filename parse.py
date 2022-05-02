"""
Universidad del Valle de Guatemala
parse.py
Proposito: Orden y consumo de los inputs
Mario Perdomo 18029
"""
from lexer import Lexer
from token import Token
from Nodes import *
from Attribute import Attribute, Vartype

class Parser:
    def __init__(self, Lexer):
        self.lexer = Lexer
        self.tokens = None
        self.tree_list = list()
        
    def nextToken(self):
        try:
            self.curr_token = next(self.tokens)
        except StopIteration:
            self.curr_token = None
    
    def consume(self, name):
        if self.next_token.name == name:
            self.next_token = self.lexer.get_token()
        elif self.next_token.name != name:
            pass

    def newSymbol(self):
        token = self.curr_token

        if token.type == Vartype.LPAR:
            self.nextToken()
            res = self.Expression()

            if self.curr_token.type != Vartype.RPAR:
                raise Exception('No right parenthesis for expression!')

            self.nextToken()
            return res

        elif token.type == Vartype.CHAR or token.type == Vartype.IDENT or token.type == VarType.STRING:
            self.nextToken()
            if token.type == Vartype.IDENT:
                return Symbol(token.value, token.type, token.name)
            return Symbol(token.value, token.type)

    def newGroup(self):
        res = self.NewSymbol()

        while self.curr_token != None and \
                (
                    self.curr_token.type == Vartype.L_KLEENE or
                    self.curr_token.type == Vartype.L_BRACK
                ):
            if self.curr_token.type == Vartype.L_KLEENE:
                self.nextToken()
                res = Kleene(self.Expression())

                if self.curr_token.type != Vartype.R_KLEENE:
                    raise Exception('No right curly bracket for a token!')
                self.nextToken()

            elif self.curr_token.type == Vartype.L_BRACK:
                self.nextToken()
                res = Bracket(self.Expression())

                if self.curr_token.type != Vartype.R_BRACK:
                    raise Exception('No right bracket for a token!')
                self.nextToken()

        return res

    def term(self):
        res = self.NewGroup()

        while self.curr_token != None and self.curr_token.type == Vartype.APPEND:
            self.nextToken()
            res = Append(res, self.NewGroup())

        return res

    def expression(self):
        res = self.Term()

        while self.curr_token != None and self.curr_token.type == Vartype.OR:
            self.nextToken()
            res = Or(res, self.Expression())

        return res
    
    def parse(self, tokens):
        self.tokens = iter(tokens)
        self.nextToken()
        if self.curr_token == None:
            return None

        res = self.Expression()
        return res

    def toSingleExpression(self):
        new_list = list()
        for token in self.lexer.tokens:
            tokens = token.value
            tokens.insert(0, Attribute(Vartype.L_PAREN, '('))
            tokens.append(Attribute(Vartype.R_PAREN, ')'))
            tokens.append(Attribute(Vartype.OR, '|'))
            new_list += tokens

        new_list.pop()
        return new_list
    
"""
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


"""
    