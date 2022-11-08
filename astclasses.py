from enum import Enum

class node:
    def visit(self):
        pass

class Op_type(Enum):
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


class Type_types(Enum):
    VOID = "void"
    INT = "int"
    CHAR = "char"
    BOOL = "bool"
    STRING = "string"
    CLASS = "class"
    METHOD = "method"


class Statement_types(Enum):
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


class expression(node):
    def __init__(self, op_type):
        self.op_type = op_type
        self.left = None
        self.right = None
        self.value = None
        self.type = None
        self.args = None


class statement(node):
    def __init__(self, statement_type):
        self.statement_type = statement_type
        self.exp = None
        self.substatement = None
        self.case_list = None


class declaration(node):
    def __init__(self, ret_type):
        self.ret_type = ret_type
        self.params = None
        self.modifier = None
        self.ident = ""
        self.init = None
        self.body : list(statement)
        self.classdecl : list(classdecl)


class type(node):
    def __init__(self, type_types):
        self.type_types = type_types
        self.name = ""
        self.array : bool
        self.subtype = ""
        self.param_list : list(declaration)


if __name__ == '__main__':
    myexpr = expression(Op_type.PLUS)
    # print(myexpr.op_type)
    mystmnt = statement(Statement_types.IF)
    # print(mystmnt.statement_type)
    mydecl = declaration(Type_types.INT)
    # print(mydecl.ret_type)
    mytype = type(Type_types.BOOL)
    # print(mytype.type_types)
    mytype.param_list = "error?"
    # print(mytype.param_list)  # prints "error?". confirmed python types are just recommendations
