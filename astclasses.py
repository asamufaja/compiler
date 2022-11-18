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


class Expression(Node):
    def __init__(self, op_type):
        self.op_type: OpTypes = op_type
        self.left = None
        self.right = None
        self.value = None
        self.type: TypeTypes = None
        self.args = None
        self.index = None

    def accept(self, v):
        v.visitExpr(self)


class Statement(Node):
    def __init__(self, statement_type):
        self.statement_type: StatementTypes = statement_type
        self.expr = None
        self.substatement = None
        self.else_statement = None
        self.case_list: list[Case] = []
        self.default_stmnts = []

    def accept(self, v):
        v.visitStmnt(self)


class ClassAndMemberDeclaration(Node):
    def __init__(self, ret_type):
        self.ret_type: TypeTypes = ret_type
        self.params: list[VariableDeclaration] = []
        self.modifier = None
        self.ident = ""
        self.body: list[Statement] = []
        self.class_members: list[ClassAndMemberDeclaration] = []
        self.array: bool = False
        self.child = None

    def accept(self, v):
        v.visitMemberDecl(self)


class VariableDeclaration(Node):
    def __init__(self, var_type):
        self.type: TypeTypes = var_type
        self.ident = ""
        self.init = None
        self.array: bool = False
        self.child = None

    def accept(self, v):
        v.visitVarDecl(self)


class Case(Node):
    def __init__(self, ident):
        self.ident = ident
        self.statements = []

    def accept(self, v):
        v.visitCase(self)


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

DOT NOTATION we actually do (x.y).z not x.(y.z)

"""