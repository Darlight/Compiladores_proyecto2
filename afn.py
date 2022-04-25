"""
Universidad del Valle de Guatemala
CC----
thompson.py
Proposito: AFN ya establecido
"""

class AFN:
    def __init__(self, start, end):
        self.start = start
        self.end = end # start and end states
        end.is_end = True
        self.text = "State Inicial: {}|  State Final: {}".format(self.start,self.end)
    
    #Recursion                          \      afn n veces /
    #state-set es como un stack -->      \       afn1     /
    #                                     \______afn0____/ 
    def addstate(self, state, state_set): # add state + recursively add epsilon transitions
        if state in state_set:
            return 
        state_set.add(state)
        for eps in state.epsilon:
            self.addstate(eps, state_set)
        
    
    def __str__(self) -> str:
        return self.text
    
    def match(self,s):
        current_states = set() # set es para ordernarlos  set([3, 4, 1, 4, 5]) --> {1, 3, 4, 5}
        self.addstate(self.start, current_states)
        #print("Set inicial:  " )
        #for i in current_states:
        #    print(i)
        #print(current_states.keys())
        #print(current_states)
        for c in s:
            #print(s)
            next_states = set()
            #test = "State: {} | Transitions: {}.".format(state,state.transitions[c])
            for state in current_states:
                #print(state.transitions.keys())
                if c in state.transitions.keys():
                    #print("State original: {} ".format(state))
                    trans_state = state.transitions[c]
                    self.addstate(trans_state, next_states)
                    #print("State next: {} |  state Final".format(trans_state))
                    #print("Char: " + c)
                    
           
            current_states = next_states

        #for s in current_states:
        #    print(s)

        for s in current_states:
            #si el caracter llega a un estado final, termine y se hace match el input del automata creado 
            if s.is_end:
                return True
        return False