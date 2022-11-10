# from lib2to3.pgen2.token import MINUS, PLUS
from sly import Lexer, Parser
import math
import astclasses as ast
import sys


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
    NUM_LITERAL = r"(?:0|[1-9])[0-9]*"

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
        ("right", EQUALS, PLUSEQUALS, MINUSEQUALS),
        ("right", TIMESEQUALS, DIVIDEEQUALS),
        ("left", OR, AND),
        ("left", DOUBLEEQUALS, NOTEQUALS),
        ("left", LESSTHAN, GREATERTHAN, LESSOREQUAL, GREATEROREQUAL),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ("right", NEW, EXCLAMATIONMARK),
        ("left", THIS),
        ("left", NUM_LITERAL, CHAR_LITERAL, STRING_LITERAL, TRUE, FALSE, NULL, IDENTIFIER),
        ("left", LPAREN, RPAREN)
    )

    def __init__(self):
        self.nodestack = []
        '''
        example: a program that declares an int variable
        first have a compilation unit node made. put on stack
        then have a statement node made, put on stack
        then the variabledeclaration node
        '''

    @_('{ ClassDefinition } VOID KXI2022 MAIN LPAREN RPAREN MethodBody')
    def CompilationUnit(self, p):
        """CompilationUnit = ClassDefinition* void kxi2022 main ( ) MethodBody"""
        # print("compilation unit")
        compu = ast.ClassAndMemberDeclaration(None)
        compu.ident = "compunit"
        compu.child = p.MethodBody
        compu.class_members.extend(p.ClassDefinition)
        print(f"\nSUSUSUS\n{compu.class_members}\nBYESUSSUS")
        return compu

    @_('CLASS IDENTIFIER LBRACE { ClassMemberDefinition } RBRACE')
    def ClassDefinition(self, p):
        """ClassDefinition = CLASS IDENTIFIER { ClassMemberDefinition* }"""
        print("ClassDefinition")
        classdef = ast.ClassAndMemberDeclaration(ast.TypeTypes.CLASS)
        classdef.ident = p.IDENTIFIER
        print(f"\nSUSUS\n{classdef.ident}\nSUSUS\n")
        classdef.class_members.extend(p.ClassMemberDefinition)
        return classdef

    @_('VOID')
    def Type(self, p):
        """Type ::= void"""
        print("Type VOID")

    @_('INT')
    def Type(self, p):
        """Type ::= int"""
        print("Type INT")

    @_('KEYWORDCHAR')
    def Type(self, p):
        """Type ::= char"""
        print("Type KEYWORDCHAR")

    @_('BOOL')
    def Type(self, p):
        """Type ::= bool"""
        print("Type BOOL")

    @_('STRING')
    def Type(self, p):
        """Type ::= string"""
        print("Type STRING")

    @_('IDENTIFIER')
    def Type(self, p):
        """Type ::= identifier"""
        print("Type IDENTIFIER")

    @_('PUBLIC')
    def Modifier(self, p):
        """Modifier ::= public"""
        print("Modifier PUBLIC")

    @_('PRIVATE')
    def Modifier(self, p):
        """Modifier ::= private"""
        print("Modifier PRIVATE")

    @_('MethodDeclaration')
    def ClassMemberDefinition(self, p):
        """ClassMemberDefinition ::= MethodDeclaration"""
        # print("ClassMemberDefinition MethodDeclaration")
        return p.MethodDeclaration

    @_('DataMemberDeclaration')
    def ClassMemberDefinition(self, p):
        """ClassMemberDefinition ::= DataMemberDeclaration"""
        # print("ClassMemberDefinition ::= DataMemberDeclaration")
        return p.DataMemberDeclaration

    @_('ConstructorDeclaration')
    def ClassMemberDefinition(self, p):
        """ClassMemberDefinition ::= ConstructorDeclaration"""
        # print("ClassMemberDefinition ::= ConstructorDeclaration")
        return p.ConstructorDeclaration

    @_('Modifier VariableDeclaration')
    def DataMemberDeclaration(self, p):
        """DataMemberDeclaration ::= Modifier VariableDeclaration"""
        # print("DataMemberDeclaration")
        memberdef = ast.ClassAndMemberDeclaration(p.VariableDeclaration.type)


    @_('Modifier Type OptionalBrackets IDENTIFIER MethodSuffix')
    def MethodDeclaration(self, p):
        """MethodDeclaration = Modifier Type OptionalBrackets identifier MethodSuffix"""
        print("MethodDeclaration")

    @_('LBRACKET RBRACKET')
    def OptionalBrackets(self, p):
        """OptionalBrackets = [ ]"""
        print("OptionalBrackets = [ ]")

    @_('empty')
    def OptionalBrackets(self, p):
        """OptionalBrackets = empty"""
        print("OptionalBrackets = empty")

    @_('IDENTIFIER MethodSuffix')
    def ConstructorDeclaration(self, p):
        """ConstructorDeclaration ::= identifier MethodSuffix"""
        print("ConstructorDeclaration")

    @_('EQUALS Expression')
    def Initializer(self, p):
        """Initializer ::= = Expression"""
        print("Initializer")

    @_('LPAREN OptionalParameterList RPAREN MethodBody')
    def MethodSuffix(self, p):
        """MethodSuffix ::= ( OptionalParameterList ) MethodBody"""
        print("MethodSuffix")

    @_('ParameterList')
    def OptionalParameterList(self, p):
        """OptionalParameterList = ParameterList"""
        print("OptionalParameterList = ParameterList")

    @_('empty')
    def OptionalParameterList(self, p):
        """OptionalParameterList = empty"""
        print("OptionalParameterList = empty")

    @_('LBRACE RepeatStatement RBRACE')
    def MethodBody(self, p):
        """MethodBody = { RepeatStatement }"""
        print("MethodBody")

    @_('RepeatStatement Statement')
    def RepeatStatement(self, p):
        """RepeatStatement = RepeatStatement Statement"""
        print("RepeatStatement = RepeatStatement Statement")

    @_('empty')
    def RepeatStatement(self, p):
        """RepeatStatement = empty"""
        print("RepeatStatement = empty")

    @_('Parameter RepeatCommaParameter')
    def ParameterList(self, p):
        """ParameterList = Parameter RepeatCommaParameter"""
        print("ParameterList")

    '''| empty'''

    @_('RepeatCommaParameter COMMA Parameter')
    def RepeatCommaParameter(self, p):
        """RepeatCommaParameter = RepeatCommaParameter , Parameter"""
        print("RepeatCommaParameter = RepeatCommaParameter , Parameter")

    @_('empty')
    def RepeatCommaParameter(self, p):
        """RepeatCommaParameter = empty"""
        print("epeatCommaParameter = empty")

    @_('Type OptionalBrackets IDENTIFIER')
    def Parameter(self, p):
        """Parameter = Type OptionalBrackets identifier"""
        print("Parameter")

    @_('Type OptionalBrackets IDENTIFIER OptionalInitializer SEMICOLON')
    def VariableDeclaration(self, p):
        """VariableDeclaration = Type OptionalBrackets identifier OptionalInitializer  ;"""
        print("VariableDeclaration")

    @_('Initializer')
    def OptionalInitializer(self, p):
        """OptionalInitializer = Initializer"""
        print("OptionalInitializer = Initializer")

    @_('empty')
    def OptionalInitializer(self, p):
        """OptionalInitializer = empty"""
        print("OptionalInitializer = empty")

    @_('LBRACE RepeatStatement RBRACE')
    def Statement(self, p):
        """Statement = { RepeatStatement }"""
        print("Statement = { RepeatStatement }")

    @_('Expression SEMICOLON')
    def Statement(self, p):
        """Statement = Expression;"""
        print("Statement = Expression;")

    @_('IF LPAREN Expression RPAREN Statement OptionalElseStatement')
    def Statement(self, p):
        """Statement = if (Expression) Statement OptionalElseStatement"""
        print("Statement = if (Expression) Statement OptionalElseStatement")

    @_('WHILE LPAREN Expression RPAREN Statement')
    def Statement(self, p):
        """Statement = while ( Expression ) Statement"""
        print("Statement = while ( Expression ) Statement")

    @_('RETURN OptionalExpression SEMICOLON')
    def Statement(self, p):
        """Statement = return OptionalExpression;"""
        print("Statement = return OptionalExpression;")

    @_('COUT LEFTSHIFT Expression SEMICOLON')
    def Statement(self, p):
        """Statement = cout << Expression ;"""
        print("Statement = cout << Expression ;")

    @_('CIN RIGHTSHIFT Expression SEMICOLON')
    def Statement(self, p):
        """Statement = cin >> Expression ;"""
        print("Statement = cin >> Expression ;")

    @_('SWITCH LPAREN Expression RPAREN CaseBlock')
    def Statement(self, p):
        """Statement = switch ( Expression ) CaseBlock"""
        print("Statement = switch ( Expression ) CaseBlock")

    @_('BREAK SEMICOLON')
    def Statement(self, p):
        """Statement = break;"""
        print("Statement = break;")

    @_('VariableDeclaration')
    def Statement(self, p):
        """Statement = VariableDeclaration"""
        print("Statement = VariableDeclaration")

    @_('ELSE Statement')
    def OptionalElseStatement(self, p):
        """OptionalElseStatement = else Statement"""
        print("OptionalElseStatement = else Statement")

    @_('empty')
    def OptionalElseStatement(self, p):
        """OptionalElseStatement = empty"""
        print("OptionalElseStatement = empty")

    @_('Expression')
    def OptionalExpression(self, p):
        """OptionalExpression = Expression"""
        print("OptionalExpression = Expression")

    @_('empty')
    def OptionalExpression(self, p):
        """OptionalExpression = empty"""
        print("OptionalExpression = empty")

    @_('LBRACE RepeatCase DEFAULT COLON RepeatStatement RBRACE')
    def CaseBlock(self, p):
        """CaseBlock = { RepeatCase default : RepeatStatement }"""
        print("CaseBlock")

    @_('RepeatCase Case')
    def RepeatCase(self, p):
        """RepeatCase = RepeatCase Case"""
        print("RepeatCase = RepeatCase Case")

    @_('empty')
    def RepeatCase(self, p):
        """RepeatCase = empty"""
        print("RepeatCase = empty")

    @_('CASE NUM_LITERAL COLON RepeatStatement')
    def Case(self, p):
        """Case = case num-literal : RepeatStatement"""
        print("Case = case num-literal : RepeatStatement")

    @_('CASE CHAR_LITERAL COLON RepeatStatement')
    def Case(self, p):
        """Case = case char-literal : RepeatStatement"""
        print("Case = case char-literal : RepeatStatement")

    @_('LPAREN Expression RPAREN')
    def Expression(self, p):
        """Expression ::= ( Expression )"""
        print("Expression ::= ( Expression )")

    @_('Expression EQUALS Expression')
    def Expression(self, p):
        """| Expression = Expression """
        print("| Expression = Expression ")

    @_('Expression PLUSEQUALS Expression')
    def Expression(self, p):
        """| Expression += Expression """
        print("| Expression += Expression ")

    @_('Expression MINUSEQUALS Expression')
    def Expression(self, p):
        """| Expression -= Expression"""
        print("| Expression -= Expression")

    @_('Expression TIMESEQUALS Expression')
    def Expression(self, p):
        """| Expression *= Expression"""
        print("| Expression *= Expression")

    @_('Expression DIVIDEEQUALS Expression')
    def Expression(self, p):
        """| Expression /= Expression"""
        print("| Expression /= Expression")

    @_('Expression PLUS Expression')
    def Expression(self, p):
        """| Expression + Expression"""
        print("| Expression + Expression")

    @_('Expression MINUS Expression')
    def Expression(self, p):
        """| Expression - Expression"""
        print("| Expression - Expression")

    @_('Expression TIMES Expression')
    def Expression(self, p):
        """| Expression * Expression"""
        print("| Expression * Expression")

    @_('Expression DIVIDE Expression')
    def Expression(self, p):
        """| Expression / Expression"""
        print("| Expression / Expression")

    @_('Expression DOUBLEEQUALS Expression')
    def Expression(self, p):
        """| Expression == Expression"""
        print("| Expression == Expression")

    @_('Expression NOTEQUALS Expression')
    def Expression(self, p):
        """| Expression != Expression"""
        print("| Expression != Expression")

    @_('Expression LESSTHAN Expression')
    def Expression(self, p):
        """| Expression < Expression"""
        print("| Expression < Expression")

    @_('Expression GREATERTHAN Expression')
    def Expression(self, p):
        """| Expression > Expression"""
        print("| Expression > Expression")

    @_('Expression LESSOREQUAL Expression')
    def Expression(self, p):
        """| Expression <= Expression"""
        print("| Expression <= Expression")

    @_('Expression GREATEROREQUAL Expression')
    def Expression(self, p):
        """| Expression >= Expression"""
        print("| Expression >= Expression")

    @_('Expression AND Expression')
    def Expression(self, p):
        """| Expression && Expression"""
        print("| Expression && Expression")

    @_('Expression OR Expression')
    def Expression(self, p):
        """| Expression || Expression"""
        print("| Expression || Expression")

    @_('EXCLAMATIONMARK Expression')
    def Expression(self, p):
        """| ! Expression"""
        print("| ! Expression")

    @_('PLUS Expression')
    def Expression(self, p):
        """| + Expression"""
        print("| + Expression")

    @_('MINUS Expression')
    def Expression(self, p):
        """| - Expression"""
        print("| - Expression")

    @_('NUM_LITERAL')
    def Expression(self, p):
        """| num-literal"""
        print("| num-literal")

    @_('CHAR_LITERAL')
    def Expression(self, p):
        """| char-literal"""
        print("| char-literal")

    @_('STRING_LITERAL')
    def Expression(self, p):
        """| string-literal"""
        print("| string-literal")

    @_('TRUE')
    def Expression(self, p):
        """| true"""
        print("| true")

    @_('FALSE')
    def Expression(self, p):
        """| false"""
        print("| false")

    @_('NULL')
    def Expression(self, p):
        """| null"""
        print("| null")

    @_('IDENTIFIER')
    def Expression(self, p):
        """| identifier"""
        print("| identifier")

    @_('NEW Type Arguments')
    def Expression(self, p):
        """| new Type  Arguments """
        print("| new Type  Arguments")

    @_('NEW Type Index')
    def Expression(self, p):
        """new Type Index"""
        print("new Type Index")

    @_('THIS')
    def Expression(self, p):
        """| this"""
        print("| this")

    @_('Expression PERIOD IDENTIFIER')
    def Expression(self, p):
        """| Expression . identifier"""
        print("| Expression . identifier")

    @_('Expression Index')
    def Expression(self, p):
        """| Expression Index"""
        print("| Expression Index")

    @_('Expression Arguments')
    def Expression(self, p):
        """| Expression Arguments"""
        print("| Expression Arguments")

    @_('LPAREN OptionalArgumentList RPAREN')
    def Arguments(self, p):
        """Arguments = ( OptionalArgumentList )"""
        print("Arguments")

    @_('ArgumentList')
    def OptionalArgumentList(self, p):
        """OptionalArgumentList = ArgumentList"""
        print("OptionalArgumentList = ArgumentList")

    @_('empty')
    def OptionalArgumentList(self, p):
        """OptionalArgumentList = empty"""
        print("OptionalArgumentList = empty")

    @_('Expression RepeatCommaExpression')
    def ArgumentList(self, p):
        """ArgumentList = Expression RepeatCommaExpression"""
        print("ArgumentList = Expression RepeatCommaExpression")

    @_('RepeatCommaExpression COMMA Expression')
    def RepeatCommaExpression(self, p):
        """RepeatCommaExpression = RepeatCommaExpression , Expression"""
        print("RepeatCommaExpression = RepeatCommaExpression , Expression")

    @_('empty')
    def RepeatCommaExpression(self, p):
        """RepeatCommaExpression = empty"""
        print("RepeatCommaExpression = empty")

    @_('LBRACKET Expression RBRACKET')
    def Index(self, p):
        """Index ::= [ Expression ]"""
        print("Index ::= [ Expression ]")

    @_('')
    def empty(self, p):
        """ e m p t y """
        print("e m p t y")


def main(args):
    lexer = BigLexer()
    parser = BigParser()

    kxi = open(args[0], 'r')
    parser.parse(lexer.tokenize(kxi.read()))


if __name__ == '__main__':
    main(sys.argv[1:])
    # lexer = BigLexer()
    # parser = BigParser()

    # messytest = open("messytest.kxi", 'r')
    # parser.parse(lexer.tokenize(messytest.read()))
