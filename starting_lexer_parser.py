from sly import Lexer, Parser
import math

class CalcLexer(Lexer):
    tokens = { IDENT, NUMBER, PLUS, TIMES, MINUS, DIVIDE, ASSIGN, LPAREN, RPAREN, NOT, 
            BOOL, BREAK, CASE, CLASS, CHAR, CIN, COUT, DEFAULT, ELSE, FALSE, IF, INT, KXI2022, NEW, 
            NULL, PUBLIC, PRIVATE, RETURN, STRING, SWITCH, TRUE, VOID, WHILE
            }
    ignore = ' \t'

    # Tokens
    alpha = r"[A-Za-z]"
    digit = r"[0 - 9]"
    identifier = r"[alpha | _] [alpha | _ | digit]*"
    line_ending = r"[\r | \n | \r\n]"
    comment = r"// . * line-ending"
    unescaped_char = r""
    # Any ASCII character from SPACE (32) to ~ (126)
    # except " (34), ' (39), or \ (92)
    escaped_char = r"[\r | \n | \t | \\]"
    char = r"[unescaped-char | escaped-char]"
    char_literal = r"'(?:char|\"|\\')'"
    string_literal = r'"(?:char|\'|\\")*"'
    num_literal = r"[0 - 9]+"

    # keywords
    BOOL = r'bool'
    BREAK = r'break'
    CASE = r'case'
    CLASS = r'class'
    CHAR = r'char'
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

    # symbols  : ; { } [ ] == != >= <= > < && || += -= *= /= << >> . ,
    # COLON, SEMICOLON, LBRACE, RBRACE, LBRACKET, RBRACKET, EQUALS, NOTEQUALS, GREATEROREQUAL, LESSOREQUAL, GREATERTHAN, LESSTHAN, AND, OR, PLUSEQUALS, MINUSEQUALS, TIMESEQUALS, DIVIDEEQUALS, LEFTSHIFT(for cout), RIGHTSHIFT(for cin), PERIOD, COMMA
    COLON = r":"
    SEMICOLON = r";"
    LBRACE = r"{"
    RBRACE = r"}"
    LBRACKET = r"\["
    RBRACKET = r"\]"
    EQUALS = r"="
    NOTEQUALS = r"!="
    GREATEROREQUAL = r">="
    LESSOREQUAL = r"<="
    GREATERTHAN = r">"
    LESSTHAN = r"<"
    AND = r"&&"
    OR = r"\|\|"
    PLUSEQUALS = r"\+="
    MINUSEQUALS = r"-="
    TIMESEQUALS = r"\*="
    DIVIDEEQUALS = r"/="
    LEFTSHIFT = r"<<"  # (for cout)
    RIGHTSHIFT = r">>"  # (for cin)
    PERIOD = r"\."
    COMMA = r","


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
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))