# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

from sly import Lexer, Parser
import math

class CalcLexer(Lexer):
    tokens = { THING, PERIOD }
    ignore = ' \t'

    # Tokens
    THING = r'[a-zA-Z_][a-zA-Z0-9_]*'
    PERIOD = r'\.'

    # NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    # NUMBER = r'\d+'

    # Special symbols
    # PLUS = r'\+'
    # MINUS = r'-'
    # TIMES = r'\*'
    # DIVIDE = r'/'
    # ASSIGN = r'='
    # LPAREN = r'\('
    # RPAREN = r'\)'
    # FACTORIAL = r'!'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    # precedence = (
    #     ('left', PLUS, MINUS),
    #     ('left', TIMES, DIVIDE, FACTORIAL),
    #     ('right', UMINUS),
    #     )

    def __init__(self):
        self.names = { }

    @_('repeatingthing PERIOD')
    def thing(self, p):
        print(p.PERIOD)

    @_('repeatingthing THING')
    def repeatingthing(self, p):
        print(p.THING)

    @_('empty')
    def repeatingthing(self, p):
        pass

    @_('')
    def empty(self, p):
        pass

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))