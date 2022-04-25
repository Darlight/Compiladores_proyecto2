"""
Universidad del Valle de Guatemala
CC----
thompson.py
Proposito: clasificacion de input
"""

class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + ":" + self.value