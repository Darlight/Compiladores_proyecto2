"""
Universidad del Valle de Guatemala
CC----
thompson.py
Proposito: clase de un estado usando la construccion de thompson
"""
#Thompson's Construction 
from afn import AFN
from lexer import Lexer
from parse import Parser
from token import Token
from state import State


class Thompson:
    def __init__(self):
        self.state_count = 0
        self.constructor = {
            'CHAR':self.handle_char, # [a-z]
            'CONCAT':self.handle_concat, #[backspace]
            'ALT':self.handle_alt, # [|]
            'STAR':self.handle_rep,# [*]
            'PLUS':self.handle_rep,# [+]
            'QMARK':self.handle_qmark }# [?]

    def create_state(self):
        self.state_count += 1
        return State('s' + str(self.state_count))
    
    def handle_char(self, t, AFN_stack):
        print("chars")
        s0 = self.create_state()
        s1 = self.create_state()
        #print("State 0: {} |  State 1: {}".format(s0,s1))
        #print(s0)
        #print(s1)
        #print(s1.transitions[t.value])
        s0.transitions[t.value] = s1
        afn = AFN(s0, s1)
        AFN_stack.append(afn)
    
    def handle_concat(self, t, AFN_stack):
        n2 = AFN_stack.pop()
        n1 = AFN_stack.pop()
        n1.end.is_end = False
        n1.end.epsilon.append(n2.start)
        afn = AFN(n1.start, n2.end)
        AFN_stack.append(afn)
    
    def handle_alt(self, t, AFN_stack):
        n2 = AFN_stack.pop()
        n1 = AFN_stack.pop()
        s0 = self.create_state()
        s0.epsilon = [n1.start, n2.start]
        s3 = self.create_state()
        n1.end.epsilon.append(s3)
        n2.end.epsilon.append(s3)
        n1.end.is_end = False
        n2.end.is_end = False
        #print("alts | : ")
        #print(s0)
        #print(s3)
        afn = AFN(s0, s3)
        AFN_stack.append(afn)
    
    def handle_rep(self, t, AFN_stack):
        n1 = AFN_stack.pop()
        s0 = self.create_state()
        s1 = self.create_state()
        s0.epsilon = [n1.start]
        if t.name == 'STAR':
            s0.epsilon.append(s1)
        n1.end.epsilon.extend([s1, n1.start])
        n1.end.is_end = False
        #print("+ y * ")
        #print(s0)
        #print(s1)
        afn = AFN(s0, s1)
        AFN_stack.append(afn)

    def handle_qmark(self, t, AFN_stack):
        n1 = AFN_stack.pop()
        n1.start.epsilon.append(n1.end)
        AFN_stack.append(n1)
"""
n = 20
p = 'a?' * n + 'a' * n
print(p)
"""
def compile(p):
    
    def print_tokens(tokens):
        for t in tokens:
            print(t)

    #lexer = Lexer(p)
    parser = Parser(p)
    tokens = parser.parse()

    handler = Thompson()

    print("Tokens: ")
    print_tokens(tokens)
    print("\n\n")
    nfa_stack = []

    for t in tokens:
        #print(t.name)
        print("Actual Token:  {} \n".format(t))
        handler.constructor[t.name](t, nfa_stack)
        #print(nfa_stack[0])
        #print(nfa_stack)
        #print(handler.state_count)

    #for i in nfa_stack:
    #    print (i)
    #print(nfa_stack[0])

    print("Total de estados creados: {}".format(handler.state_count))
    assert len(nfa_stack) == 1, "Hubo un fallo o typo en la expresion regular \n "
    return nfa_stack.pop() 

n = 20
p = 'a?' * n + 'a' * n
p2 = '*+a)'
input_string = 'a' * n


nfa = compile(p2)
#print(nfa)
matched = nfa.match('a')
print(matched)
