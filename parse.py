"""
Universidad del Valle de Guatemala
parse.py
Proposito: Orden y consumo de los inputs
Mario Perdomo 18029
"""
from token_project import *
from Nodes import *
from Attribute import Vartype
from Elements import Variable



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

        if token.type == Vartype.L_PAREN:
            self.nextToken()
            res = self.expression()

            if self.curr_token.type != Vartype.R_PAREN:
                raise Exception('No right parenthesis for expression!')

            self.nextToken()
            return res

        elif token.type == Vartype.CHAR or token.type == Vartype.IDENTIFIER or token.type == Vartype.STRING:
            self.nextToken()
            if token.type == Vartype.IDENTIFIER:
                return Symbol(token.value, token.type, token.name)
            return Symbol(token.value, token.type)

    def newGroup(self):
        res = self.newSymbol()

        while self.curr_token != None and \
                (
                    self.curr_token.type == Vartype.L_KLEENE or
                    self.curr_token.type == Vartype.L_BRACK
                ):
            if self.curr_token.type == Vartype.L_KLEENE:
                self.nextToken()
                res = Kleene(self.expression())

                if self.curr_token.type != Vartype.R_KLEENE:
                    raise Exception('No right curly bracket for a token!')
                self.nextToken()

            elif self.curr_token.type == Vartype.L_BRACK:
                self.nextToken()
                res = Bracket(self.expression())

                if self.curr_token.type != Vartype.R_BRACK:
                    raise Exception('No right bracket for a token!')
                self.nextToken()

        return res

    def term(self):
        res = self.newGroup()

        while self.curr_token != None and self.curr_token.type == Vartype.APPEND:
            self.nextToken()
            res = Append(res, self.newGroup())

        return res

    def expression(self):
        res = self.term()

        while self.curr_token != None and self.curr_token.type == Vartype.OR:
            self.nextToken()
            res = Or(res, self.expression())

        return res
    
    def parse(self, tokens):
        self.tokens = iter(tokens)
        self.nextToken()
        if self.curr_token == None:
            return None

        res = self.expression()
        return res

    def toSingleExpression(self):
        new_list = list()
        for token in self.lexer.tokens:
            tokens = token.value
            tokens.insert(0, Variable(Vartype.L_PAREN, '('))
            tokens.append(Variable(Vartype.R_PAREN, ')'))
            tokens.append(Variable(Vartype.OR, '|'))
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
    