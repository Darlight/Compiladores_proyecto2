"""
Universidad del Valle de Guatemala
CC----
thompson.py
Proposito: Representacion de estados en general 
"""
#  {a, b, ε}
class State:
    def __init__(self, name):
        self.epsilon = [] #estados vacios
        #Transiciones del input y hacia el siguiuente estado
        self.transitions = {} 
        self.name = name
        self.is_end = False # True --> estado final
        self.text = "State: {} | Transitions: {}. | Epsilons: {}".format(self.name,self.transitions, self.epsilon)
        self.text3 = "State: {} | Transitions: {}. ".format(self.name,self.transitions)
        self.text2 = "State: {} | Transitions: {}. | final state?: {}".format(self.name,self.transitions, self.is_end)
        #self.text3 = "algo"
    
    def __str__(self) -> str:
        return self.name