import codecs
import pickle
from Attribute import Vartype, Attribute
from re import findall
"""
Universidad del Valle de Guatemala
picke_utils.py
Proposito: Manejo de leer archivos y crear outputs con la gramatica ingresada
Mario Perdomo 18029
"""
CONTEXT_WORDS = ['ANY']
ANY_SET = set([chr(char) for char in range(0, 256)])

def GetTextInsideSymbols(string, init_symbol, end_symbol):
    start = string.find(init_symbol)
    end = string.find(end_symbol)

    if start == -1 or end == -1:
        return None

    if string.count(init_symbol) != 1 or string.count(end_symbol) != 1:
        return None

    return string[start+1:end]


def GetTextFromDoubleQuotes(string):
    text = findall('"([^"]*)"', string)

    if not text:
        return None
    if len(text) > 1:
        return None

    return text[0]


def GetTextFromSingleQuotes(string):
    text = findall("'([^']*)'", string)

    if not text:
        return None
    if len(text) > 1:
        return None

    return str(text[0])


def GetNoAlpha(string):
    pos = 1
    while pos < len(string) and (string[pos].isalpha() or string[pos] == '|'):
        pos += 1
    return pos if pos < len(string) else None


def IdentExists(ident, char_set):
    try:
        next(filter(lambda x: x.ident == ident, char_set))
        return True
    except StopIteration:
        return False


def GetIdentValue(ident, char_set):
    try:
        ident = next(filter(lambda x: x.ident == ident, char_set))
        return ident.value
    except StopIteration:
        return None


def GetCharValue(char):
    # Finally, we check for the text inside the parenthesis
    value = GetTextInsideSymbols(char, '(', ')')

    # Check for missing or extra parenthesis
    if value == None:
        raise Exception(
            'In CHARACTERS, char is not defined correctly: missplaced parenthesis')

    # Check if the value is a digit
    if not value.isdigit():
        raise Exception(
            'In CHARACTERS, char is not defined correctly: non-digit CHR value')

    return chr(int(value))


def GetElementType(string, char_set):

    if string.count('"') == 2:
        string = string.replace('\"', '')
        val = set([chr(ord(char)) for char in string])
        return Attribute(Vartype.STRING, val)

    if string.count('\'') == 2:
        char = GetTextFromSingleQuotes(string)
        try:
            char = codecs.decode(char, 'unicode_escape')
            ord_ = ord(char)
        except:
            raise Exception(f'Unvalid char in GetElementType: {string}')

        new_set = set(chr(ord_))
        return Attribute(Vartype.CHAR, new_set)

    if string in CONTEXT_WORDS:
        if 'ANY' == string:
            return Attribute(Vartype.STRING, ANY_SET)

    if string.isdigit():
        return Attribute(Vartype.NUMBER, string)

    if IdentExists(string, char_set):
        return Attribute(Vartype.IDENTIFIER, GetIdentValue(string, char_set), string)

    if 'CHR' in string:
        char = set(GetCharValue(string))
        return Attribute(Vartype.CHAR, char)


def WriteToFile(filename: str, content: str):
    with open(filename, 'w') as _file:
        _file.write(content)

    return f'File "{filename}" created!'


def DumpAutomata(automata):
    pickle.dump(automata, open('./output/automata.p', 'wb'))