# from lib2to3.pgen2.token import MINUS, PLUS
from sly import Lexer, Parser
import math


class BigLexer(Lexer):
    tokens = {BOOL, BREAK, CASE, CLASS, KEYWORDCHAR, CIN, COUT, DEFAULT, ELSE, FALSE, IF, INT, KXI2022, NEW,
              NULL, PUBLIC, PRIVATE, RETURN, STRING, SWITCH, TRUE, VOID, WHILE,
              COLON, SEMICOLON, LBRACE, RBRACE, LBRACKET, RBRACKET, DOUBLEEQUALS, EQUALS, NOTEQUALS,
              GREATEROREQUAL, LESSOREQUAL, GREATERTHAN, LESSTHAN, AND, OR, PLUSEQUALS,
              MINUSEQUALS, TIMESEQUALS, DIVIDEEQUALS, LEFTSHIFT, RIGHTSHIFT, PERIOD, COMMA,
              IDENTIFIER, CHAR_LITERAL, STRING_LITERAL, NUM_LITERAL, MAIN,
              EXCLAMATIONMARK, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, THIS
              # ALPHA,  UNESCAPED_CHAR, ESCAPED_CHAR, LINE_ENDING, CHAR, DIGIT, COMMENT,
              }
    ignore = ' \t'
    # Ignored pattern
    ignore_newline = r'\n+'
    ignore_comment = r'//[^\n]*'

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

    MAIN = r'main'
    THIS = r'this'

    # COMMENT = r"//[^\n]*"

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
    # ALPHA = r"[A-Za-z]"
    # DIGIT = r"[0-9]"
    IDENTIFIER = r"(?:[A-Za-z]|_)(?:[A-Za-z]|_|[0-9])*"
    # LINE_ENDING = r"(?:\r|\n|\r\n)"

    # UNESCAPED_CHAR = r"[^\"'\\\n\t\r]"  # should not automatically match whitespace
        # Any ASCII character from SPACE (32) to ~ (126)
        # except " (34), ' (39), or \ (92)
    # ESCAPED_CHAR = r"(\r|\n|\t|\\)"
    # CHAR = r"(?:[^\"'\\\n\t\r]|(\r|\n|\t|\\))"
    CHAR_LITERAL = r"'(?:(?:[^\"'\\\n\t\r]|(\r|\n|\t|\\))|\"|\\')'"
    STRING_LITERAL = r'"(?:(?:[^\"\'\\\n\t\r]|(\r|\n|\t|\\))|\'|\\")*"'
    NUM_LITERAL = r"[1-9][0-9]*"

    # def DIGIT(self, t):
    #     t.value = int(t.value)
    #     return t

    def NUM_LITERAL(self, t):
        t.value = int(t.value)
        return t

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class BigParser(Parser):
    tokens = BigLexer.tokens
    debugfile = 'parser.out'

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        )

    def __init__(self):
        self.idents = {}

    '''CompilationUnit = RepeatClassDefinition void kxi2022 main ( ) MethodBody'''

    @_('RepeatClassDefinition VOID KXI2022 MAIN LPAREN RPAREN MethodBody')
    def CompilationUnit(self, p):
        pass

    '''RepeatClassDefinition = RepeatClassDefinition ClassDefinition | empty'''

    @_('RepeatClassDefinition ClassDefinition')
    def RepeatClassDefinition(self, p):
        pass

    @_('empty')
    def RepeatClassDefinition(self, p):
        pass

    '''ClassDefinition = CLASS IDENTIFIER { RepeatClassMemberDefinition }'''

    @_('CLASS IDENTIFIER LBRACE RepeatClassMemberDefinition RBRACE')
    def ClassDefinition(self, p):
        pass

    '''RepeatClassMemberDefinition = RepeatClassMemberDefinition ClassMemberDefinition 
        | empty'''

    @_('RepeatClassMemberDefinition ClassMemberDefinition')
    def RepeatClassMemberDefinition(self, p):
        pass

    @_('empty')
    def RepeatClassMemberDefinition(self, p):
        pass

    '''Type ::= void | int | char | bool | string | identifier'''

    @_('VOID')
    def Type(self, p):
        pass

    @_('INT')
    def Type(self, p):
        pass

    @_('KEYWORDCHAR')
    def Type(self, p):
        pass

    @_('BOOL')
    def Type(self, p):
        pass

    @_('STRING')
    def Type(self, p):
        pass

    @_('IDENTIFIER')
    def Type(self, p):
        pass

    '''Modifier ::= public | private'''

    @_('PUBLIC')
    def Modifier(self, p):
        pass

    @_('PRIVATE')
    def Modifier(self, p):
        pass

    '''ClassMemberDefinition ::= MethodDeclaration| DataMemberDeclaration
        | ConstructorDeclaration'''

    @_('MethodDeclaration')
    def ClassMemberDefinition(self, p):
        pass

    @_('DataMemberDeclaration')
    def ClassMemberDefinition(self, p):
        pass

    @_('ConstructorDeclaration')
    def ClassMemberDefinition(self, p):
        pass

    '''DataMemberDeclaration ::= Modifier VariableDeclaration'''

    @_('Modifier VariableDeclaration')
    def DataMemberDeclaration(self, p):
        pass

    '''MethodDeclaration = Modifier Type OptionalBrackets identifier MethodSuffix'''

    @_('Modifier Type OptionalBrackets IDENTIFIER MethodSuffix')
    def MethodDeclaration(self, p):
        pass

    '''OptionalBrackets = [ ] | empty'''

    @_('LBRACKET RBRACKET')
    def OptionalBrackets(self, p):
        pass

    @_('empty')
    def OptionalBrackets(self, p):
        pass

    '''ConstructorDeclaration ::= identifier MethodSuffix'''

    @_('IDENTIFIER MethodSuffix')
    def ConstructorDeclaration(self, p):
        pass

    '''Initializer ::= = Expression'''

    @_('EQUALS Expression')
    def Initializer(self, p):
        pass

    '''MethodSuffix ::= ( OptionalParameterList ) MethodBody'''

    @_('LPAREN OptionalParameterList RPAREN MethodBody')
    def MethodSuffix(self, p):
        pass

    '''OptionalParameterList = ParameterList | empty'''

    @_('ParameterList')
    def OptionalParameterList(self, p):
        pass

    @_('empty')
    def OptionalParameterList(self, p):
        pass


    '''MethodBody = { RepeatStatement }'''

    @_('LBRACE RepeatStatement RBRACE')
    def MethodBody(self, p):
        pass

    '''RepeatStatement = RepeatStatement Statement | empty'''

    @_('RepeatStatement Statement')
    def RepeatStatement(self, p):
        pass

    @_('empty')
    def RepeatStatement(self, p):
        pass


    '''ParameterList = Parameter RepeatCommaParameter'''

    @_('Parameter RepeatCommaParameter')
    def ParameterList(self, p):
        pass

    '''RepeatCommaParameter = RepeatCommaParameter , Parameter | empty'''

    @_('RepeatCommaParameter COMMA Parameter')
    def RepeatCommaParameter(self, p):
        pass

    @_('empty')
    def RepeatCommaParameter(self, p):
        pass

    '''Parameter = Type OptionalBrackets identifier'''

    @_('Type OptionalBrackets IDENTIFIER')
    def Parameter(self, p):
        pass

    '''VariableDeclaration = Type OptionalBrackets identifier OptionalInitializer  ;'''

    @_('Type OptionalBrackets IDENTIFIER OptionalInitializer SEMICOLON')
    def VariableDeclaration(self, p):
        pass

    @_('Initializer')
    def OptionalInitializer(self, p):
        pass

    @_('empty')
    def OptionalInitializer(self, p):
        pass

    '''Statement = { RepeatStatement }
        | Expression;
        | if ( Expression ) Statement OptionalElseStatement
        | while ( Expression ) Statement
        | return OptionalExpression  ;
        | cout << Expression ;
        | cin >> Expression ;
        | switch ( Expression ) CaseBlock
        | break ;
        | VariableDeclaration'''

    @_('LBRACE RepeatStatement RBRACE')
    def Statement(self, p):
        pass

    @_('Expression SEMICOLON')
    def Statement(self, p):
        pass

    @_('IF LPAREN Expression RPAREN Statement OptionalElseStatement')
    def Statement(self, p):
        pass

    @_('WHILE LPAREN Expression RPAREN Statement')
    def Statement(self, p):
        pass

    @_('RETURN OptionalExpression SEMICOLON')
    def Statement(self, p):
        pass

    @_('COUT LEFTSHIFT Expression SEMICOLON')
    def Statement(self, p):
        pass

    @_('CIN RIGHTSHIFT Expression SEMICOLON')
    def Statement(self, p):
        pass

    @_('SWITCH LPAREN Expression RPAREN CaseBlock')
    def Statement(self, p):
        pass

    @_('BREAK SEMICOLON')
    def Statement(self, p):
        pass

    @_('VariableDeclaration')
    def Statement(self, p):
        pass

    '''OptionalElseStatement = else Statement | empty'''

    @_('ELSE Statement')
    def OptionalElseStatement(self, p):
        pass

    @_('empty')
    def OptionalElseStatement(self, p):
        pass

    '''OptionalExpression = Expression | empty'''

    @_('Expression')
    def OptionalExpression(self, p):
        pass

    @_('empty')
    def OptionalExpression(self, p):
        pass

    '''CaseBlock = { RepeatCase default : RepeatStatement }'''

    @_('LBRACE RepeatCase DEFAULT COLON RepeatStatement RBRACE')
    def CaseBlock(self, p):
        pass

    '''RepeatCase = RepeatCase Case | empty'''

    @_('RepeatCase Case')
    def RepeatCase(self, p):
        pass

    @_('empty')
    def RepeatCase(self, p):
        pass

    '''Case = case num-literal | char-literal : RepeatStatement'''

    @_('CASE NUM_LITERAL')
    def Case(self, p):
        pass

    @_('CHAR_LITERAL COLON RepeatStatement')
    def Case(self, p):
        pass

    '''Expression ::= ( Expression )'''

    @_('LPAREN Expression RPAREN')
    def Expression(self, p):
        pass

    '''| Expression = Expression '''

    @_('Expression EQUALS Expression')
    def Expression(self, p):
        pass

    '''| Expression += Expression '''

    @_('Expression PLUSEQUALS Expression')
    def Expression(self, p):
        pass

    '''| Expression -= Expression'''

    @_('Expression MINUSEQUALS Expression')
    def Expression(self, p):
        pass

    '''| Expression *= Expression'''

    @_('Expression TIMESEQUALS Expression')
    def Expression(self, p):
        pass

    '''| Expression /= Expression'''

    @_('Expression DIVIDEEQUALS Expression')
    def Expression(self, p):
        pass

    '''| Expression + Expression'''

    @_('Expression PLUS Expression')
    def Expression(self, p):
        pass

    '''| Expression - Expression'''

    @_('Expression MINUS Expression')
    def Expression(self, p):
        pass

    '''| Expression * Expression'''

    @_('Expression TIMES Expression')
    def Expression(self, p):
        pass

    '''| Expression / Expression'''

    @_('Expression DIVIDE Expression')
    def Expression(self, p):
        pass

    '''| Expression == Expression'''

    @_('Expression DOUBLEEQUALS Expression')
    def Expression(self, p):
        pass

    '''| Expression != Expression'''

    @_('Expression NOTEQUALS Expression')
    def Expression(self, p):
        pass

    '''| Expression < Expression'''

    @_('Expression LESSTHAN Expression')
    def Expression(self, p):
        pass

    '''| Expression > Expression'''

    @_('Expression GREATERTHAN Expression')
    def Expression(self, p):
        pass

    '''| Expression <= Expression'''

    @_('Expression LESSOREQUAL Expression')
    def Expression(self, p):
        pass

    '''| Expression >= Expression'''

    @_('Expression GREATEROREQUAL Expression')
    def Expression(self, p):
        pass

    '''| Expression && Expression'''

    @_('Expression AND Expression')
    def Expression(self, p):
        pass

    '''| Expression || Expression'''

    @_('Expression OR Expression')
    def Expression(self, p):
        pass

    '''| ! Expression'''

    @_('EXCLAMATIONMARK Expression')
    def Expression(self, p):
        pass

    '''| + Expression'''

    @_('PLUS Expression')
    def Expression(self, p):
        pass

    '''| - Expression'''

    @_('MINUS Expression')
    def Expression(self, p):
        pass

    '''| num-literal'''

    @_('NUM_LITERAL')
    def Expression(self, p):
        pass

    '''| char-literal'''

    @_('CHAR_LITERAL')
    def Expression(self, p):
        pass

    '''| string-literal'''

    @_('STRING_LITERAL')
    def Expression(self, p):
        pass

    '''| true'''

    @_('TRUE')
    def Expression(self, p):
        pass

    '''| false'''

    @_('FALSE')
    def Expression(self, p):
        pass

    '''| null'''

    @_('NULL')
    def Expression(self, p):
        pass

    '''| identifier'''

    @_('IDENTIFIER')
    def Expression(self, p):
        pass

    '''| new Type  Arguments | Index'''

    @_('NEW Type Arguments')
    def Expression(self, p):
        pass

    @_('NEW Type Index')
    def Expression(self, p):
        pass

    '''| this'''

    @_('THIS')
    def Expression(self, p):
        pass

    '''| Expression . identifier'''

    @_('Expression PERIOD IDENTIFIER')
    def Expression(self, p):
        pass

    '''| Expression Index'''

    @_('Expression Index')
    def Expression(self, p):
        pass

    '''| Expression Arguments'''

    @_('Expression Arguments')
    def Expression(self, p):
        pass

    '''Arguments = ( OptionalArgumentList )'''

    @_('LPAREN OptionalArgumentList RPAREN')
    def Arguments(self, p):
        pass

    '''OptionalArgumentList = ArgumentList
        | empty '''

    @_('ArgumentList')
    def OptionalArgumentList(self, p):
        pass

    @_('empty')
    def OptionalArgumentList(self, p):
        pass

    '''ArgumentList = Expression RepeatCommaExpression'''

    @_('Expression RepeatCommaExpression')
    def ArgumentList(self, p):
        pass

    '''RepeatCommaExpression = RepeatCommaExpression , Expression
        | empty '''

    @_('RepeatCommaExpression COMMA Expression')
    def RepeatCommaExpression(self, p):
        pass

    @_('empty')
    def RepeatCommaExpression(self, p):
        pass

    '''Index ::= [ Expression ]'''

    @_('LBRACKET Expression RBRACKET')
    def Index(self, p):
        pass

    @_('')
    def empty(self, p):
        pass


if __name__ == '__main__':
    lexer = BigLexer()
    parser = BigParser()

    # pointfile = open("point.kxy", 'r')
    # parser.parse(lexer.tokenize(pointfile.read()))
    # for token in lexer.tokenize(pointfile.read()):
    #     print(f'{token.type}, {token.value}')

    # otherTests = open("othertests.kxy", 'r')
    # parser.parse(lexer.tokenize(otherTests.read()))
    # for token in lexer.tokenize(otherTests.read()):
    #     print(f'{token.type}, {token.value}')

    messytest = open("messytest.kxy", 'r')
    parser.parse(lexer.tokenize(messytest.read()))
    # for token in lexer.tokenize(messytest.read()):
    #     print(f'{token.type}, {token.value}')

    # while True:
    # try:
    #     text = input('calc > ')
    # except EOFError:
    #     break
    # if text:
    #     parser.parse(lexer.tokenize(text))
