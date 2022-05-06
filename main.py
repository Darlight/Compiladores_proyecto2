"""
Universidad del Valle de Guatemala
main.py
Proposito: Generador del lenguaje a traves de un cocor
Mario Perdomo 18029
"""

import sys
from lexer import Lexer
from afd_directo import DDFA
from parse import Parser
from pickle_utils import DumpAutomata
from python_generator import CodeGen
from pprint import pprint


if __name__ == "__main__":

    grammar_file = './gramatica/ArchivoPrueba1.atg'

    if len(sys.argv) > 1:
        grammar_file = sys.argv[1]

    #lexer = lexer(grammar_file)

    try:
        lexer = Lexer(grammar_file)
    except FileNotFoundError as e:
        print(f'\tERR: "{grammar_file} file not found."')
    except Exception as e:
        print(f'\tERR: {e}')
        exit(-1)

    allchars = lexer.GetAllChars()
    parser = Parser(lexer)
    tokens = parser.toSingleExpression()
    tree = parser.parse(tokens)

    # print('\n\n', '='*20, 'ARBOL SINTÁCTICO', '='*20, '\n')
    # pprint(tree)
    # print(tokens)


    ddfa = DDFA(tree, allchars, lexer.keywords, lexer.ignore)
    DumpAutomata(ddfa)

    CodeGen('./scanner.py', lexer.tokens, ddfa).GenerateScannerFile()

    print(
    """
    Evaluador de expresiones CoCoR

    Identifica token basados en una gramatica creada por cualquier usuario. 

    Comando para cargar la gramatica: | python main.py [archivo.cfg] |
    
    """)
    print(
    """
    Del programa python_generator.py, se crea un archivo llamado scanner.py. 
    Este archivo permite leer los tokens basados de la gramatica.

    Comando para cargar un archivo txt que detecte tokens: | python scanner.py [archivo.txt]
    
    """)
