from enum import Enum


class node:
    def visit(self):
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
    BRACES = "{}"
    EXPRESSION = "expr"
    IF = "if"
    WHILE = "while"
    RETURN = "return"
    COUT = "cout"
    CIN = "cin"
    SWITCH = "switch"
    BREAK = "break"
    VAR_DECL = "var_decl"


class Expression(node):
    def __init__(self, op_type):
        self.op_type = op_type
        self.left = None
        self.right = None
        self.value = None
        self.type = None
        self.args = None


class Statement(node):
    def __init__(self, statement_type):
        self.statement_type = statement_type
        self.exp = None
        self.substatement = None
        self.case_list = None


class Declaration(node):
    def __init__(self, ret_type):
        self.ret_type = ret_type
        self.params = None
        self.modifier = None
        self.ident = ""
        self.init = None
        self.body: list[Statement]
        self.classdecl: list[classdecl]


class Type(node):
    def __init__(self, type_types):
        self.type_type = type_types
        self.name = ""
        self.array: bool
        self.subtype = ""
        self.param_list: list[Declaration]


if __name__ == '__main__':
    myexpr = Expression(OpTypes.PLUS)
    # print(myexpr.op_type)
    mystmnt = Statement(StatementTypes.IF)
    # print(mystmnt.statement_type)
    mydecl = Declaration(TypeTypes.INT)
    # print(mydecl.ret_type)
    mytype = Type(TypeTypes.BOOL)
    # print(mytype.type_type)
    mytype.param_list = "error?"
    # print(mytype.param_list)  # prints "error?". confirmed python types are just recommendations
