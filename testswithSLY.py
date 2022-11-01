# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

from sly import Lexer, Parser
import math

class CalcLexer(Lexer):
    tokens = { THING, PERIOD, SUS }
    ignore = ' \t'

    # Tokens
    THING = r'[a-zA-Z_][a-zA-Z0-9_]*'
    PERIOD = r'\.'
    SUS = r'SUS'

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

    @_('repeatingthing optionalthing PERIOD')
    def thing(self, p):
        print(p.PERIOD)

    @_('repeatingthing THING')
    def repeatingthing(self, p):
        print(p.THING)

    @_('empty')
    def repeatingthing(self, p):
        pass

    # adding the optionalthing is silly since the repeating thing covers anything, but I could adjust that
    
    @_('SUS')
    def optionalthing(self, p):
        print(p.SUS)

    @_('empty')
    def optionalthing(self, p):
        pass

    @_('')
    def empty(self, p):
        pass

    class Expr:
        pass

    class BinOp(Expr):
        def __init__(self, op, left, right)
            self.op = op
            self.left = left
            self.right = right

    class Number(Expr):
        def __init__(self, value):
            self.value = value

    @_('expr PLUS expr',
    'expr MINUS expr',
    'expr TIMES expr',
    'expr DIVIDE expr')
    def expr(self, p):
        return BinOp(p[1], p.expr0, p.expr1)

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return Number(p.NUMBER)

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