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

    IF_TRUE = "if_true"
    IF_FALSE = "if_false"
    END_CASE = "end_case"


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
        self.classtype: ClassAndMemberDeclaration = None  # for method expr identifiers
        self.array: bool = None
        self.reg = None
        self.line = None
        self.param_list = []

    def accept(self, v):
        v.visitExpr(self)

    def __str__(self):
        return f"expr:{self.op_type.value} value:{self.value} at:{self.__repr__()[-10:-1]}"


class Statement(Node):
    def __init__(self, statement_type):
        self.statement_type: StatementTypes = statement_type
        self.expr: Expression = None
        self.substatement: list[Statement] = []
        self.else_statement: Statement = None
        self.case_list: list[Case] = []
        self.default_stmnts: list[Statement] = []
        self.is_while = False
        self.line = None
        self.reg = None
        self.if_count = None
        self.switch_count = None

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
        self.init: Expression = None
        self.classtype = None
        self.child: ClassAndMemberDeclaration = None
        self.reg = None
        self.line = None

    def accept(self, v):
        v.visitMemberDecl(self)

    def calcSize(self):
        # I think just give every datamember and function an int on heap,
        # functions get one int to store addr, datas get that space for their value
        return len(self.class_members)
    def calcFuncSize(self):
        vars = [s for s in self.body if isinstance(s, VariableDeclaration) or isinstance(s, ClassAndMemberDeclaration)]
        try:
            params = [p for p in self.params]
        except:
            params = []
        return 4 * (len(vars) + len(params) + 2)  # maybe not very accurate...

    def __str__(self):
        return f"class/member:{self.ident} at:{self.__repr__()[-10:-1]}"

    def hasConstruct(self):
        for n in self.class_members:
            if n.ident == self.ident:
                return True
        return False


class VariableDeclaration(Node):
    def __init__(self, var_type):
        self.type: TypeTypes = var_type
        self.ident: str = ""
        self.init: Expression = None
        self.array: bool = None
        self.is_param: bool = None
        self.is_obj: bool = None

    def accept(self, v):
        v.visitVarDecl(self)

    def __str__(self):
        return f"var:{self.type} {self.ident} at:{self.__repr__()[-10:-1]}"


class Case(Node):
    def __init__(self, ident):
        self.ident: str = ident
        self.statements: list[Statement] = []
        self.switch_count = None

    def accept(self, v):
        v.visitCase(self)

    def __str__(self):
        return f"case:{self.ident} at:{self.__repr__()[-10:-1]}"


class Keywords(Enum):  # copied from the lexer
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
    NULL = r'null '
    PUBLIC = r'public '
    PRIVATE = r'private '
    RETURN = r'return'
    STRING = r'string'
    SWITCH = r'switch'
    TRUE = r'true'
    VOID = r'void'
    WHILE = r'while'
    MAIN = r'main'
    THIS = r'this'
    # adding these for fun
    NUM_LITERAL = "num_literal"
    CHAR_LITERAL = "char_literal"
    STRING_LITERAL = "string_literal"
