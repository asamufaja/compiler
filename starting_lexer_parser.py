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
            EXCLAMATIONMARK, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN
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

    # symbols  : ; { } ( ) [ ] = == != >= <= > < && || ! + - * / += -= *= /= << >> . ,
    # COLON, SEMICOLON, LBRACE, RBRACE, LBRACKET, RBRACKET, EQUALS, NOTEQUALS, GREATEROREQUAL, LESSOREQUAL, GREATERTHAN, LESSTHAN, AND, OR, PLUSEQUALS, MINUSEQUALS, TIMESEQUALS, DIVIDEEQUALS, LEFTSHIFT(for cout), RIGHTSHIFT(for cin), PERIOD, COMMA
    COLON = r":"
    SEMICOLON = r";"
    PERIOD = r"\."
    COMMA = r","
    LBRACE = r"{"
    RBRACE = r"}"
    LBRACKET = r"\["
    RBRACKET = r"\]"
    LPAREN = r"\("
    RPAREN = r"\)"
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

    # precedence = (
    #     ('left', PLUS, MINUS),
    #     ('left', TIMES, DIVIDE),
    #     ('right', UMINUS, NOT),
    #     )

    def __init__(self):
        self.idents = { }

    @_('')
    def empty(self, p):
        pass
    '''
    CompilationUnit = RepeatClassDefinition void kxi2022 main ( ) MethodBody
    '''
    @_(RepeatClassDefinition void kxi2022 main LPAREN RPAREN MethodBody)
    def CompilationUnit(self, p):
        pass
    '''
    RepeatClassDefinition = RepeatClassDefinition CompilationUnit
        | empty
    '''
    @_(RepeatClassDefinition CompilationUnit)
    def RepeatClassDefinition(self, p):
        pass
    
    @_(empty)
    def RepeatClassDefinition(self, p):
        pass
    '''
    ClassDefinition = CLASS IDENTIFIER { RepeatClassMemberDefinition }
    '''
    @_(CLASS IDENTIFIER LBRACE RepeatClassMemberDefinition RBRACE)
    def ClassDefinition(self, p):
        pass
    '''
    RepeatClassMemberDefinition = RepeatClassMemberDefinition ClassDefinition
        | empty
    '''
    @_(RepeatClassMemberDefinition ClassDefinition)
    def RepeatClassMemberDefinition(self, p):
        pass

    @_(empty)
    def RepeatClassMemberDefinition(self, p):
        pass
    '''
    Type ::= void | int | char | bool | string | identifier
    '''
    @_(VOID)
    def Type(self, p):
        pass
    @_(INT)
    def Type(self, p):
        pass
    @_(CHAR)
    def Type(self, p):
        pass
    @_(BOOL)
    def Type(self, p):
        pass
    @_(STRING)
    def Type(self, p):
        pass
    @_(IDENTIFIER)
    def Type(self, p):
        pass
    '''
    Modifier ::= public | private
    ClassMemberDefinition ::= MethodDeclaration
    | DataMemberDeclaration
    | ConstructorDeclaration
    DataMemberDeclaration ::= Modifier VariableDeclaration

    MethodDeclaration = Modifier Type OptionalBrackets identifier MethodSuffix
    OptionalBrackets = [ ]
        | empty

    ConstructorDeclaration ::= identifier MethodSuffix
    Initializer ::= = Expression
    MethodSuffix ::= ( OptionalParameterList ) MethodBody
    OptionalParameterList = ParameterList
        | empty

    MethodBody = { RepeatStatement }
    RepeatStatement = RepeatStatement Statement
        | empty
    ParameterList = Parameter RepeatCommaParameter
    RepeatCommaParameter = RepeatCommaParameter , Parameter
        | empty
    Parameter = Type OptionalBrackets identifier
    VariableDeclaration = Type OptionalBrackets identifier Initializer  ;

    Statement = { RepeatStatement }
        | Expression;
        | if ( Expression ) Statement OptionalElseStatement
        | while ( Expression ) Statement
        | return OptionalExpression  ;
        | cout << Expression ;
        | cin >> Expression ;
        | switch ( Expression ) CaseBlock
        | break ;
        | VariableDeclaration

    OptionalElseStatement = else Statement
        | empty
    OptionalExpression = Expression
        | empty
    CaseBlock = { RepeatCase default : RepeatStatement }
    RepeatCase = RepeatCase Case
        | empty
    Case = case num-literal | char-literal : RepeatStatement

    Expression ::= ( Expression )
        | Expression = Expression
        | Expression += Expression
        | Expression -= Expression
        | Expression *= Expression
        | Expression /= Expression
        | Expression + Expression
        | Expression - Expression
        | Expression * Expression
        | Expression / Expression
        | Expression == Expression
        | Expression != Expression
        | Expression < Expression
        | Expression > Expression
        | Expression <= Expression
        | Expression >= Expression
        | Expression && Expression
        | Expression || Expression
        | ! Expression
        | + Expression
        | - Expression
        | num-literal
        | char-literal
        | string-literal
        | true
        | false
        | null
        | identifier
        | new Type  Arguments | Index
        | this
        | Expression . identifier
        | Expression Index
        | Expression Arguments

    Arguments = ( OptionalArgumentList )
    OptionalArgumentList = ArgumentList
        | empty
    ArgumentList = Expression RepeatCommaExpression
    RepeatCommaExpression = RepeatCommaExpression , Expression
        | empty
    Index ::= [ Expression ]
    '''


if __name__ == '__main__':
    lexer = BigLexer()
    parser = BigParser()
    # while True:
        # try:
        #     text = input('calc > ')
        # except EOFError:
        #     break
        # if text:
        #     parser.parse(lexer.tokenize(text))