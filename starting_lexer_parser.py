# from lib2to3.pgen2.token import MINUS, PLUS
from sly import Lexer, Parser
import math

class BigLexer(Lexer):
    tokens = { BOOL, BREAK, CASE, CLASS, KEYWORDCHAR, CIN, COUT, DEFAULT, ELSE, FALSE, IF, INT, KXI2022, NEW, 
            NULL, PUBLIC, PRIVATE, RETURN, STRING, SWITCH, TRUE, VOID, WHILE,
            COLON, SEMICOLON, LBRACE, RBRACE, LBRACKET, RBRACKET, DOUBLEEQUALS, EQUALS, NOTEQUALS, 
            GREATEROREQUAL, LESSOREQUAL, GREATERTHAN, LESSTHAN, AND, OR, PLUSEQUALS, 
            MINUSEQUALS, TIMESEQUALS, DIVIDEEQUALS, LEFTSHIFT, RIGHTSHIFT, PERIOD, COMMA,
            ALPHA, DIGIT, IDENTIFIER, LINE_ENDING, COMMENT, UNESCAPED_CHAR, ESCAPED_CHAR,
            CHAR, CHAR_LITERAL, STRING_LITERAL, NUM_LITERAL,
            EXCLAMATIONMARK, PLUS, MINUS, TIMES, DIVIDE
            }
    ignore = ' \t'

    # keywords
    BOOL = r'bool'
    BREAK = r'break'
    CASE = r'case'
    CLASS = r'class'
    KEYWORDCHAR = r'char'
    CIN = r'cin'
    COUT = r'cout'
    DEFAULT = r'default'
    ELSE = r'else'
    FALSE = r'false'
    IF = r'if'
    INT = r'int'
    KXI2022 = r'kxi2022'
    NEW = r'new'
    NULL = r'null'
    PUBLIC = r'public'
    PRIVATE = r'private'
    RETURN = r'return'
    STRING = r'string'
    SWITCH = r'switch'
    TRUE = r'true'
    VOID = r'void'
    WHILE = r'while'

    # symbols  : ; { } [ ] = == != >= <= > < && || ! + - * / += -= *= /= << >> . ,
    # COLON, SEMICOLON, LBRACE, RBRACE, LBRACKET, RBRACKET, EQUALS, NOTEQUALS, GREATEROREQUAL, LESSOREQUAL, GREATERTHAN, LESSTHAN, AND, OR, PLUSEQUALS, MINUSEQUALS, TIMESEQUALS, DIVIDEEQUALS, LEFTSHIFT(for cout), RIGHTSHIFT(for cin), PERIOD, COMMA
    COLON = r":"
    SEMICOLON = r";"
    PERIOD = r"\."
    COMMA = r","
    LBRACE = r"{"
    RBRACE = r"}"
    LBRACKET = r"\["
    RBRACKET = r"\]"
    DOUBLEEQUALS = r"=="
    EQUALS = r"="
    NOTEQUALS = r"!="
    EXCLAMATIONMARK = r"!"
    GREATEROREQUAL = r">="
    LESSOREQUAL = r"<="
    LEFTSHIFT = r"<<"  # (for cout)
    RIGHTSHIFT = r">>"  # (for cin)
    GREATERTHAN = r">"
    LESSTHAN = r"<"
    AND = r"&&"
    OR = r"\|\|"
    PLUSEQUALS = r"\+="
    MINUSEQUALS = r"-="
    TIMESEQUALS = r"\*="
    DIVIDEEQUALS = r"/="
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"

    # Tokens
    ALPHA = r"[A-Za-z]"
    DIGIT = r"[0-9]"
    IDENTIFIER = r"(?:[A-Za-z]|_)(?:[A-Za-z]|_|[0-9])*"
    LINE_ENDING = r"(?:\r|\n|\r\n)"
    COMMENT = r"//[^\n]*"
    UNESCAPED_CHAR = r"[^\"'\\\n\t\r]"  # should not automatically match whitespace
    # Any ASCII character from SPACE (32) to ~ (126)
    # except " (34), ' (39), or \ (92)
    ESCAPED_CHAR = r"(\r|\n|\t|\\)"
    CHAR = r"(?:[^\"'\\\n\t\r]|(\r|\n|\t|\\))"
    CHAR_LITERAL = r"'(?:(?:[^\"'\\\n\t\r]|(\r|\n|\t|\\))|\"|\\')'"
    STRING_LITERAL = r'"(?:(?:[^\"\'\\\n\t\r]|(\r|\n|\t|\\))|\'|\\")*"'
    NUM_LITERAL = r"[0-9]+"

    def DIGIT(self, t):
        t.value = int(t.value)
        return t

    def NUM_LITERAL(self, t):
        t.value = int(t.value)
        return t

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class BigParser(Parser):
    tokens = BigLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS, NOT),
        )

    def __init__(self):
        self.idents = { }

    @_('IDENT ASSIGN expr')
    def statement(self, p):
        self.idents[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('expr NOT')
    def expr(self, p):
        return math.factorial(p.expr)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

    @_('IDENT')
    def expr(self, p):
        try:
            return self.idents[p.IDENT]
        except LookupError:
            print(f'Undefined name {p.IDENT!r}')
            return 0

if __name__ == '__main__':
    lexer = BigLexer()
    # parser = BigParser()
    # while True:
        # try:
        #     text = input('calc > ')
        # except EOFError:
        #     break
        # if text:
        #     parser.parse(lexer.tokenize(text))