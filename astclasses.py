from enum import Enum
import abc


class Node:
    @abc.abstractmethod
    def accept(self, v):
        pass


class OpTypes(Enum):
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIVIDE = "/"
    PLUSEQUALS = "+="
    MINUSEQUALS = "-="
    TIMESEQUALS = "*="
    DIVIDEEQUALS = "/="
    EQUALS = "="
    DOUBLEEQUALS = "=="
    NOTEQUALS = "!="
    LESSTHAN = "<"
    GREATERTHAN = ">"
    LESSOREQUAL = "<="
    GREATEROREQUAL = ">="
    AND = "&&"
    OR = "||"
    EXCLAMATIONMARK = "!"
    NUM_LITERAL = "num_literal"
    CHAR_LITERAL = "char_literal"
    STRING_LITERAL = "string_literal"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    IDENTIFIER = "identifier"
    NEW = "new"
    THIS = "this"
    PERIOD = "."
    INDEX = "[]"
    ARGUMENTS = "()"


class TypeTypes(Enum):
    VOID = "void"
    INT = "int"
    CHAR = "char"
    BOOL = "bool"
    STRING = "string"
    CLASS = "class"
    METHOD = "method"


class StatementTypes(Enum):
    BRACES = "{ statement* }"
    EXPRESSION = "expr"
    IF = "if"
    WHILE = "while"
    RETURN = "return"
    COUT = "cout"
    CIN = "cin"
    SWITCH = "switch"
    BREAK = "break"
    VAR_DECL = "var_decl"


class ModifierTypes(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    NONE = "none"


class MemberTypes(Enum):
    CLASS = "class"
    DATAMEMBER = "datamember"
    METHOD = "method"
    CONSTRUCTOR = "constructor"


class Expression(Node):
    def __init__(self, op_type):
        self.op_type: OpTypes = op_type
        self.left: Expression = None
        self.right: Expression = None
        self.value = None  # anything
        self.type: TypeTypes = None
        self.args: list[Expression] = []
        self.index: Expression = None

    def accept(self, v):
        v.visitExpr(self)

    def __str__(self):
        return f"expr:{self.op_type.value} value:{self.value} at:{self.__repr__()[-10:-1]}"


class Statement(Node):
    def __init__(self, statement_type):
        self.statement_type: StatementTypes = statement_type
        self.expr: Expression = None
        self.substatement: list[Statement] = []
        self.else_statement: list[Statement] = []
        self.case_list: list[Case] = []
        self.default_stmnts: list[Statement] = []

    def accept(self, v):
        v.visitStmnt(self)

    def __str__(self):
        return f"stmnt:{self.statement_type.value} at:{self.__repr__()[-10:-1]}"


class ClassAndMemberDeclaration(Node):
    def __init__(self, ret_type):
        self.ret_type: TypeTypes = ret_type
        self.member_type: MemberTypes = None
        self.params: list[VariableDeclaration] = []
        self.modifier: ModifierTypes = None
        self.ident: str = ""
        self.body: list[Statement] = []
        self.class_members: list[ClassAndMemberDeclaration] = []
        self.array: bool = None
        self.child: ClassAndMemberDeclaration = None

    def accept(self, v):
        v.visitMemberDecl(self)

    def __str__(self):
        return f"class/member:{self.ident} at:{self.__repr__()[-10:-1]}"


class VariableDeclaration(Node):
    def __init__(self, var_type):
        self.type: TypeTypes = var_type
        self.ident: str = ""
        self.init: Expression = None
        self.array: bool = None

    def accept(self, v):
        v.visitVarDecl(self)

    def __str__(self):
        return f"var:{self.type} {self.ident} at:{self.__repr__()[-10:-1]}"


class Case(Node):
    def __init__(self, ident):
        self.ident: str = ident
        self.statements: list[Statement] = []

    def accept(self, v):
        v.visitCase(self)

    def __str__(self):
        return f"case:{self.ident} at:{self.__repr__()[-10:-1]}"


# class Variable(Node):  # what if variable is an expression actually? lol
#     def __init__(self, type_types):
#         self.type_type: TypeTypes = type_types
#         self.name = ""
#         self.array: bool
#         self.subtype = ""
#         self.param_list: list[Declaration] = []
#         self.child = None


"""
alduous says node does traverse, because it knows its children
typically post order, children accept visitor first.
the visitor then is maybe just existing and it gets called sometimes.
if we say child.accept(), we want to have it go to right visitor use virtual dispatch because it's taht type
visitor is gonna have like visit_if() and such, simulate overloading
have abstract visitor that do nothing,
if the specific visitors don't ask for it, then it goes to the do nothing
in python can change visit methods to get intermediate results from child accepts
and can pass forward. 

DOT NOTATION is actually do (x.y).z not x.(y.z)

"""