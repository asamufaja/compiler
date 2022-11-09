# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

from sly import Lexer, Parser
import math

class CalcLexer(Lexer):
    tokens = { NAME, NUMBER, PLUS, TIMES, MINUS, DIVIDE, ASSIGN, LPAREN, RPAREN, FACTORIAL }

    ignore = ' \t'

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    FACTORIAL = r'!'


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

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE, FACTORIAL),
        ('right', UMINUS),
        )

    def __init__(self):
        self.names = { }

    @_('NAME ASSIGN expr')
    def statement(self, p):
        # self.names[p.NAME] = p.expr
        pass

    @_('expr')
    def statement(self, p):
        # print(p.expr)
        pass

    @_('expr PLUS expr')
    def expr(self, p):
        # return p.expr0 + p.expr1
        pass

    @_('expr MINUS expr')
    def expr(self, p):
        # return p.expr0 - p.expr1
        pass

    @_('expr TIMES expr')
    def expr(self, p):
        # return p.expr0 * p.expr1
        pass

    @_('expr DIVIDE expr')
    def expr(self, p):
        # return p.expr0 / p.expr1
        pass

    @_('expr FACTORIAL')
    def expr(self, p):
        # return math.factorial(p.expr)
        pass

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        # return -p.expr
        pass

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        # return p.expr
        pass

    @_('NUMBER')
    def expr(self, p):
        # return int(p.NUMBER)
        pass

    @_('NAME')
    def expr(self, p):
        # try:
        #     return self.names[p.NAME]
        # except LookupError:
        #     print(f'Undefined name {p.NAME!r}')
        #     return 0
        pass

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    # parser.parse(lexer.tokenize("9 + 10 * 11"))
    for token in lexer.tokenize("9 + 10 * 11"):
        print(f"{token.Type}, {token.value}")
    # while True:
    #     try:
    #         text = input('calc > ')
    #     except EOFError:
    #         break
    #     if text:
    #         parser.parse(lexer.tokenize(text))