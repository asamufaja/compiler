# from lib2to3.pgen2.token import MINUS, PLUS
from sly import Lexer, Parser
import math
import astclasses as ast
import sys
import semanticvisitors as v


class BigLexer(Lexer):
    tokens = {BOOL, BREAK, CASE, CLASS, KEYWORDCHAR, CIN, COUT, DEFAULT, ELSE, FALSE, IF, INT, KXI2022, NEW,
              NULL, PUBLIC, PRIVATE, RETURN, STRING, SWITCH, TRUE, VOID, WHILE,
              COLON, SEMICOLON, LBRACE, RBRACE, LBRACKET, RBRACKET, DOUBLEEQUALS, EQUALS,
              IDENTIFIER, CHAR_LITERAL, STRING_LITERAL, NUM_LITERAL, MAIN,
              EXCLAMATIONMARK, PLUS, LPAREN, RPAREN, COMMA, LRBRACKET
              # ALPHA,  UNESCAPED_CHAR, ESCAPED_CHAR, LINE_ENDING, CHAR, DIGIT, COMMENT,
              }

    IDENTIFIER = r"(?:[A-Za-z]|_)(?:[A-Za-z]|_|[0-9])*"

    ignore = ' \t'
    # Ignored pattern
    ignore_newline = r'\n+'
    ignore_comment = r'//[^\n]*'

    # keywords
    IDENTIFIER['bool'] = BOOL
    IDENTIFIER['break'] = BREAK
    IDENTIFIER['case'] = CASE
    IDENTIFIER['class'] = CLASS
    IDENTIFIER['char'] = KEYWORDCHAR
    IDENTIFIER['cin'] = CIN
    IDENTIFIER['cout'] = COUT
    IDENTIFIER['default'] = DEFAULT
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['false'] = FALSE
    IDENTIFIER['if'] = IF

    # INT = r'int'
    IDENTIFIER['int'] = INT

    IDENTIFIER['kxi2022'] = KXI2022
    IDENTIFIER['new'] = NEW
    IDENTIFIER['null'] = NULL
    IDENTIFIER['public'] = PUBLIC
    IDENTIFIER['private'] = PRIVATE
    IDENTIFIER['return'] = RETURN
    IDENTIFIER['string'] = STRING
    IDENTIFIER['switch'] = SWITCH
    IDENTIFIER['true'] = TRUE
    IDENTIFIER['void'] = VOID
    IDENTIFIER['while'] = WHILE
    IDENTIFIER['main'] = MAIN
    IDENTIFIER[','] = COMMA

    # COMMENT = r"//[^\n]*"

    # symbols  : ; { } ( ) [ ] = == != >= <= > < && || ! + - * / += -= *= /= << >> . ,
    # COLON, SEMICOLON, LBRACE, RBRACE, LBRACKET, RBRACKET, EQUALS, NOTEQUALS, GREATEROREQUAL, LESSOREQUAL, GREATERTHAN, LESSTHAN, AND, OR, PLUSEQUALS, MINUSEQUALS, TIMESEQUALS, DIVIDEEQUALS, LEFTSHIFT(for cout), RIGHTSHIFT(for cin), PERIOD, COMMA
    COLON = r":"
    SEMICOLON = r";"
    LBRACE = r"{"
    RBRACE = r"}"
    LRBRACKET = r"\[]"
    LBRACKET = r"\["
    RBRACKET = r"\]"
    LPAREN = r"\("
    RPAREN = r"\)"
    DOUBLEEQUALS = r"=="
    EQUALS = r"="
    EXCLAMATIONMARK = r"!"
    PLUS = r"\+"

    # Tokens
    # ALPHA = r"[A-Za-z]"
    # DIGIT = r"[0-9]"

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
        self.index += 1
        raise Exception(f"Illegal character {t.value[0]}")


class BigParser(Parser):
    tokens = BigLexer.tokens
    debugfile = 'parser.out'

    precedence = (
        ("right", EQUALS),
        ("left", DOUBLEEQUALS),
        ('left', PLUS),
        ("left", NEW, EXCLAMATIONMARK),
        ("left", IDENTIFIER),
        ("left", LRBRACKET),
        ("left", LBRACKET, RBRACKET),
        # ("left", LPAREN, RPAREN),
    )

    def error(self, p):
        if p:
            raise Exception(f"Syntax error at token {p.type}, {p}")
            # Just discard the token and tell the parser it's okay.
            # self.errok()
        else:
            raise Exception("Syntax error at EOF")

    @_('{ ClassDefinition } VOID KXI2022 MAIN LPAREN RPAREN MethodBody')
    def CompilationUnit(self, p):
        """CompilationUnit = ClassDefinition* void kxi2022 main ( ) MethodBody"""
        print("compilation unit")
        compu = ast.ClassAndMemberDeclaration(None)
        compu.ident = "compunit"
        compu.class_members.extend(p.ClassDefinition)
        mainfunc = ast.ClassAndMemberDeclaration(ast.TypeTypes.VOID)
        mainfunc.body = p.MethodBody
        mainfunc.ident = "main"
        compu.child = mainfunc

        return compu

    @_('CLASS IDENTIFIER LBRACE { ClassMemberDefinition } RBRACE')
    def ClassDefinition(self, p):
        """ClassDefinition = CLASS IDENTIFIER { ClassMemberDefinition* }"""
        print("ClassDefinition")
        classdef = ast.ClassAndMemberDeclaration(ast.TypeTypes.CLASS)
        classdef.ident = p.IDENTIFIER
        classdef.member_type = ast.MemberTypes.CLASS
        classdef.class_members.extend(p.ClassMemberDefinition)
        return classdef

    @_('VOID')
    def Type(self, p):
        """Type ::= void"""
        print("Type VOID")
        return ast.TypeTypes.VOID

    @_('INT')
    def Type(self, p):
        """Type ::= int"""
        print("Type INT")
        return ast.TypeTypes.INT

    @_('KEYWORDCHAR')
    def Type(self, p):
        """Type ::= char"""
        print("Type KEYWORDCHAR")
        return ast.TypeTypes.CHAR

    @_('BOOL')
    def Type(self, p):
        """Type ::= bool"""
        print("Type BOOL")
        return ast.TypeTypes.BOOL

    @_('STRING')
    def Type(self, p):
        """Type ::= string"""
        print("Type STRING")
        return ast.TypeTypes.STRING

    @_('IDENTIFIER Index')
    def Expression(self, p):
        print('sussy expr index')
        expr = ast.Expression(ast.OpTypes.INDEX)
        identexpr = ast.Expression(ast.OpTypes.IDENTIFIER)
        identexpr.value = p.IDENTIFIER
        expr.left = identexpr
        expr.index = p.Index
        return expr

    # @_('IDENTIFIER')
    # def Type(self, p):
    #     """Type ::= identifier"""
    #     print("Type IDENTIFIER")
    #     # return ast.TypeTypes.CLASS
    #     return p.IDENTIFIER

    @_('PUBLIC')
    def Modifier(self, p):
        """Modifier ::= public"""
        print("Modifier PUBLIC")
        return ast.ModifierTypes.PUBLIC

    @_('PRIVATE')
    def Modifier(self, p):
        """Modifier ::= private"""
        print("Modifier PRIVATE")
        return ast.ModifierTypes.PRIVATE

    @_('MethodDeclaration')
    def ClassMemberDefinition(self, p):
        """ClassMemberDefinition ::= MethodDeclaration"""
        print("ClassMemberDefinition MethodDeclaration")
        return p.MethodDeclaration

    @_('DataMemberDeclaration')
    def ClassMemberDefinition(self, p):
        """ClassMemberDefinition ::= DataMemberDeclaration"""
        print("ClassMemberDefinition ::= DataMemberDeclaration")
        return p.DataMemberDeclaration

    @_('ConstructorDeclaration')
    def ClassMemberDefinition(self, p):
        """ClassMemberDefinition ::= ConstructorDeclaration"""
        print("ClassMemberDefinition ::= ConstructorDeclaration")
        return p.ConstructorDeclaration

    @_('Modifier VariableDeclaration')
    def DataMemberDeclaration(self, p):
        """DataMemberDeclaration ::= Modifier VariableDeclaration"""
        print("DataMemberDeclaration")
        memberdef = ast.ClassAndMemberDeclaration(p.VariableDeclaration.type)
        memberdef.modifier = p.Modifier
        memberdef.member_type = ast.MemberTypes.DATAMEMBER
        memberdef.ident = p.VariableDeclaration.ident
        return memberdef

    @_('Modifier Type OptionalBrackets IDENTIFIER MethodSuffix')
    def MethodDeclaration(self, p):
        """MethodDeclaration = Modifier Type OptionalBrackets identifier MethodSuffix"""
        print("MethodDeclaration")
        methoddecl = ast.ClassAndMemberDeclaration(p.Type)
        methoddecl.modifier = p.Modifier
        methoddecl.array = p.OptionalBrackets
        methoddecl.ident = p.IDENTIFIER
        methoddecl.member_type = ast.MemberTypes.METHOD
        methoddecl.params = p.MethodSuffix.params
        methoddecl.body.extend(p.MethodSuffix.body)
        return methoddecl

    # @_('LBRACKET RBRACKET')
    @_('LRBRACKET')
    def OptionalBrackets(self, p):
        """OptionalBrackets = [ ]"""
        print("OptionalBrackets = [ ]")
        return True

    @_('empty')
    def OptionalBrackets(self, p):
        """OptionalBrackets = empty"""
        print("OptionalBrackets = empty")
        return False

    @_('IDENTIFIER MethodSuffix')
    def ConstructorDeclaration(self, p):
        """ConstructorDeclaration ::= identifier MethodSuffix"""
        print("ConstructorDeclaration")
        constrdecl = ast.ClassAndMemberDeclaration(ast.TypeTypes.CLASS)
        constrdecl.ident = p.IDENTIFIER
        constrdecl.member_type = ast.MemberTypes.CONSTRUCTOR
        constrdecl.modifier = ast.ModifierTypes.PUBLIC
        constrdecl.params = p.MethodSuffix.params
        constrdecl.body.extend(p.MethodSuffix.body)
        return constrdecl

    @_('EQUALS Expression')
    def Initializer(self, p):
        """Initializer ::= = Expression"""
        print("Initializer")
        # expr = ast.Expression(p.Expression.type)
        # return expr
        return p.Expression

    # @_('LPAREN OptionalParameterList RPAREN MethodBody')
    @_('LPAREN [ ParameterList ] RPAREN MethodBody')
    def MethodSuffix(self, p):
        """MethodSuffix ::= ( OptionalParameterList ) MethodBody"""
        print("MethodSuffix")
        methodsuff = ast.ClassAndMemberDeclaration(None)
        methodsuff.params = p.ParameterList
        methodsuff.body = p.MethodBody  # p.MethodBody should be list of statements
        return methodsuff


    # @_('LBRACE RepeatStatement RBRACE')
    @_('LBRACE { Statement } RBRACE')
    def MethodBody(self, p):
        """MethodBody = { RepeatStatement }"""
        print("MethodBody")
        # methodbody = ast.ClassAndMemberDeclaration(None)
        # methodbody.body.extend(p.Statement)
        return p.Statement


    # @_('Parameter RepeatCommaParameter')
    @_('Parameter { COMMA Parameter }')
    def ParameterList(self, p):
        """ParameterList = Parameter RepeatCommaParameter"""
        print("ParameterList")
        paramlist = [p.Parameter0]
        paramlist.extend(p.Parameter1)
        return paramlist

    @_('Type OptionalBrackets IDENTIFIER')
    def Parameter(self, p):
        """Parameter = Type OptionalBrackets identifier"""
        print("Parameter")
        param = ast.VariableDeclaration(p.Type)
        param.array = p.OptionalBrackets
        param.ident = p.IDENTIFIER
        param.is_param = True
        return param

    # @_('Type OptionalBrackets IDENTIFIER OptionalInitializer SEMICOLON')
    @_('Type OptionalBrackets IDENTIFIER [ Initializer ] SEMICOLON')
    def VariableDeclaration(self, p):
        """VariableDeclaration = Type OptionalBrackets identifier OptionalInitializer  ;"""
        print("VariableDeclaration")
        vardecl = ast.VariableDeclaration(p.Type)
        vardecl.array = p.OptionalBrackets
        vardecl.ident = p.IDENTIFIER
        vardecl.init = p.Initializer
        vardecl.is_param = False
        return vardecl


    # @_('LBRACE RepeatStatement RBRACE')
    @_('LBRACE { Statement } RBRACE')
    def Statement(self, p):
        """Statement = { RepeatStatement }"""
        print("Statement = { RepeatStatement }")
        stmntlist = ast.Statement(ast.StatementTypes.BRACES)
        stmntlist.substatement = p.Statement  # should automatically be a list
        return stmntlist

    @_('Expression SEMICOLON')
    def Statement(self, p):
        """Statement = Expression;"""
        print("Statement = Expression;")
        exprstmnt = ast.Statement(ast.StatementTypes.EXPRESSION)
        exprstmnt.expr = p.Expression
        return exprstmnt


    @_('RETURN OptionalExpression SEMICOLON')
    def Statement(self, p):
        """Statement = return OptionalExpression;"""
        print("Statement = return OptionalExpression;")
        retstmnt = ast.Statement(ast.StatementTypes.RETURN)
        retstmnt.expr = p.OptionalExpression
        return retstmnt


    @_('VariableDeclaration')
    def Statement(self, p):
        """Statement = VariableDeclaration"""
        print("Statement = VariableDeclaration")
        return p.VariableDeclaration

    @_('Expression')
    def OptionalExpression(self, p):
        """OptionalExpression = Expression"""
        print("OptionalExpression = Expression")
        return p.Expression

    @_('empty')
    def OptionalExpression(self, p):
        """OptionalExpression = empty"""
        print("OptionalExpression = empty")
        return None


    @_('LPAREN Expression RPAREN')
    def Expression(self, p):
        """Expression ::= ( Expression )"""
        print("Expression ::= ( Expression )")
        # TODO IDK about this one
        return p.Expression

    @_('Expression EQUALS Expression')
    def Expression(self, p):
        """| Expression = Expression """
        print("| Expression = Expression ")
        expr = ast.Expression(ast.OpTypes.EQUALS)
        expr.left = p.Expression0
        expr.right = p.Expression1
        expr.value = p.Expression1.value
        return expr

    @_('Expression PLUS Expression')
    def Expression(self, p):
        """| Expression + Expression"""
        print("| Expression + Expression")
        expr = ast.Expression(ast.OpTypes.PLUS)
        expr.left = p.Expression0
        expr.right = p.Expression1
        return expr

    @_('PLUS Expression')
    def Expression(self, p):
        """| + Expression"""
        print("| + Expression")
        expr = ast.Expression(ast.OpTypes.PLUS)
        expr.right = p.Expression
        expr.type = p.Expression.type
        return expr

    @_('NUM_LITERAL')
    def Expression(self, p):
        """| num-literal"""
        print("| num-literal")
        expr = ast.Expression(ast.OpTypes.NUM_LITERAL)
        expr.type = ast.TypeTypes.INT
        expr.value = p.NUM_LITERAL
        return expr




    @_('IDENTIFIER')
    def Expression(self, p):
        """| identifier"""
        print("Expr| identifier")
        expr = ast.Expression(ast.OpTypes.IDENTIFIER)
        expr.value = p.IDENTIFIER
        return expr
    # there's a reduce/reduce conflict between these two, for now it works better to have idents be expr
    @_('IDENTIFIER')
    def Type(self, p):
        """Type ::= identifier"""
        print("Type IDENTIFIER")
        # return ast.TypeTypes.CLASS
        return p.IDENTIFIER

    @_('Expression Index')
    def Expression(self, p):
        """| Expression Index"""
        print("| Expression Index")
        expr = ast.Expression(ast.OpTypes.INDEX)
        expr.left = p.Expression
        expr.index = p.Index
        return expr


    @_('NEW Type Arguments')
    def Expression(self, p):
        """| new Type  Arguments """
        print("| new Type  Arguments")
        expr = ast.Expression(ast.OpTypes.NEW)
        expr.type = p.Type
        expr.args = p.Arguments
        expr.value = "new"
        return expr

    @_('NEW Type Index')
    def Expression(self, p):
        """new Type Index"""
        print("new Type Index")
        expr = ast.Expression(ast.OpTypes.NEW)
        expr.type = p.Type
        expr.index = p.Index
        expr.value = "new"
        return expr




    @_('Expression Arguments')
    def Expression(self, p):
        """| Expression Arguments"""
        print("| Expression Arguments")
        expr = ast.Expression(ast.OpTypes.ARGUMENTS)
        expr.left = p.Expression
        expr.args = p.Arguments
        return expr

    @_('LPAREN [ ArgumentList ] RPAREN')
    def Arguments(self, p):
        """Arguments = ( OptionalArgumentList )"""
        print("Arguments")
        return p.ArgumentList

    # @_('Expression RepeatCommaExpression')
    @_('Expression { COMMA Expression }')
    def ArgumentList(self, p):
        """ArgumentList = Expression RepeatCommaExpression"""
        print("ArgumentList = Expression RepeatCommaExpression")
        arglist = [p.Expression0]
        arglist.extend(p.Expression1)
        return arglist


    @_('LBRACKET Expression RBRACKET')
    def Index(self, p):
        """Index ::= [ Expression ]"""
        print("Index ::= [ Expression ]")
        # expr = ast.Expression(ast.OpTypes.INDEX)
        # expr.index = p.Expression
        return p.Expression

    @_('')
    def empty(self, p):
        """ e m p t y """
        print("e m p t y")


# if __name__ == '__main__':
#     main.main(sys.argv[1:])
    # lexer = BigLexer()
    # parser = BigParser()

    # messytest = open("messytest.kxi", 'r')
    # parser.parse(lexer.tokenize(messytest.read()))
