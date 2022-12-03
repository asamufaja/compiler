import astclasses as ast
import semanticvisitors as sv


class RegManager:
    def __init__(self):
        self.regs = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11",
                     "R12", "R13", "R14", "R15", ]
        self.given_regs = []

    def getReg(self):
        try:
            reg = self.regs.pop()
            self.given_regs.append(reg)
            return reg
        except:
            print("TODO no free regs")  # TODO

    def freeReg(self, reg):
        try:
            self.given_regs.remove(reg)
            self.regs.append(reg)
        except:
            print("tried to free an already free reg")


class SetupDirectives(sv.Visitor):
    def __init__(self, filename="a.asm"):
        self.asmfile = open(filename, "w+")
        self.in_main = False

    def visitVarDecl(self, node: ast.VariableDeclaration):
        # if node.type == ast.TypeTypes.VOID:  # I don't think there should be void var decls
        #     pass
        if node.type == ast.TypeTypes.INT:
            if not node.array:
                line = f"{node.ident} .INT "
                if node.init:
                    line += f"{node.init.value}\n"
                else:
                    line += "\n"
                self.asmfile.write(line)
            else:
                line = f"{node.ident} .INT 0\n"
                if node.init:  # should be a new
                    numlines = node.init.index.value - 1  # - 1 for the first line already made
                    for x in range(numlines):
                        line += f" .INT 0\n"
                self.asmfile.write(line)

        if node.type == ast.TypeTypes.CHAR:
            if not node.array:
                line = f"{node.ident} .BYT "
                if node.init:
                    line += f"'{node.init.value}'\n"
                self.asmfile.write(line)
            else:
                line = f"{node.ident} .BYT\n"
                if node.init:  # should be a new
                    numlines = node.init.index.value - 1  # - 1 for the first line already made
                    for x in range(numlines):
                        line += f" .BYT \n"
                self.asmfile.write(line)

        if node.type == ast.TypeTypes.BOOL:
            line = f"{node.ident} .INT "
            if node.init:
                if node.init.value == "true":
                    line += f"1\n"
                elif node.init.value == "false":
                    line += f"0\n"
            else:
                line += "\n"
            self.asmfile.write(line)

        if node.type == ast.TypeTypes.STRING:
            if node.init:
                line = f"{node.ident}"
                for c in node.init.value[1:]:
                    line += f" .BYT '{c}'\n"
            else:
                line = ""
            self.asmfile.write(line)

        if node.is_obj:  # because I have node.type as the class ident if it's an object
            # give it all of it's fields
            pass

        # if node.type == ast.TypeTypes.METHOD:  # regular var decls aren't methods
        #     pass
        super().visitVarDecl(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        if node.ident == "main":
            self.in_main = True
        if node.member_type == ast.MemberTypes.CLASS:
            pass
        if node.member_type == ast.MemberTypes.DATAMEMBER:
            pass
        if node.member_type == ast.MemberTypes.METHOD:
            pass
        if node.member_type == ast.MemberTypes.CONSTRUCTOR:
            pass
        super().visitMemberDecl(node)


class ExpressionGen(sv.Visitor):
    def __init__(self, asmfile):
        self.asmfile = asmfile
        self.regs = RegManager()

    def visitExpr(self, node: ast.Expression):
        if node.op_type == ast.OpTypes.PLUS:
            line = ""
            reg1 = self.regs.getReg()
            reg2 = self.regs.getReg()
            if node.left.op_type == ast.OpTypes.IDENTIFIER:
                line += f"LDR {reg1}, {node.left.value}\n"
            elif node.left.op_type == ast.OpTypes.NUM_LITERAL:
                line += f"MOVI {reg1}, {node.left.value}"
            if node.right.op_type == ast.OpTypes.IDENTIFIER:
                line += f"LDR {reg2}, {node.right.value}\n"
            elif node.right.op_type == ast.OpTypes.NUM_LITERAL:
                line += f"MOVI {reg2}, {node.right.value}\n"
            line += f"ADD {reg1}, {reg2}\n"
            # keep reg 1 for giving to the assign or whatever?
            self.regs.freeReg(reg2)
            self.asmfile.write(line)
        if node.op_type == ast.OpTypes.MINUS:
            pass
        if node.op_type == ast.OpTypes.TIMES:
            pass
        if node.op_type == ast.OpTypes.DIVIDE:
            pass
        if node.op_type == ast.OpTypes.PLUSEQUALS:
            pass
        if node.op_type == ast.OpTypes.MINUSEQUALS:
            pass
        if node.op_type == ast.OpTypes.TIMESEQUALS:
            pass
        if node.op_type == ast.OpTypes.DIVIDEEQUALS:
            pass
        if node.op_type == ast.OpTypes.EQUALS:
            pass
        if node.op_type == ast.OpTypes.DOUBLEEQUALS:
            pass
        if node.op_type == ast.OpTypes.NOTEQUALS:
            pass
        if node.op_type == ast.OpTypes.LESSTHAN:
            pass
        if node.op_type == ast.OpTypes.GREATERTHAN:
            pass
        if node.op_type == ast.OpTypes.LESSOREQUAL:
            pass
        if node.op_type == ast.OpTypes.GREATEROREQUAL:
            pass
        if node.op_type == ast.OpTypes.AND:
            pass
        if node.op_type == ast.OpTypes.OR:
            pass
        if node.op_type == ast.OpTypes.EXCLAMATIONMARK:
            pass
        if node.op_type == ast.OpTypes.TRUE:
            pass
        if node.op_type == ast.OpTypes.FALSE:
            pass
        if node.op_type == ast.OpTypes.NULL:
            pass
        if node.op_type == ast.OpTypes.NEW:
            pass
        if node.op_type == ast.OpTypes.THIS:
            pass
        if node.op_type == ast.OpTypes.PERIOD:
            pass
        if node.op_type == ast.OpTypes.INDEX:
            pass
        if node.op_type == ast.OpTypes.ARGUMENTS:
            pass
        super().visitExpr(node)


class StatementGen(sv.Visitor):
    def visitExpr(self, node: ast.Expression):
        super().visitExpr(node)

    def visitStmnt(self, node: ast.Statement):

        super().visitStmnt(node)

    def visitVarDecl(self, node: ast.VariableDeclaration):
        super().visitVarDecl(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        super().visitMemberDecl(node)

    def visitCase(self, node: ast.Case):
        super().visitCase(node)


class CallFunctionsGen(sv.Visitor):
    def visitExpr(self, node: ast.Expression):
        super().visitExpr(node)

    def visitStmnt(self, node: ast.Statement):
        super().visitStmnt(node)

    def visitVarDecl(self, node: ast.VariableDeclaration):
        super().visitVarDecl(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        super().visitMemberDecl(node)

    def visitCase(self, node: ast.Case):
        super().visitCase(node)


"""
wanna make a new visitor? just copy and update the name
class classname(sv.Visitor):
    def __init__(self):
        pass

    def visitExpr(self, node: ast.Expression):
        super().visitExpr(node)

    def visitStmnt(self, node: ast.Statement):
        super().visitStmnt(node)

    def visitVarDecl(self, node: ast.VariableDeclaration):
        super().visitVarDecl(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        super().visitMemberDecl(node)

    def visitCase(self, node: ast.Case):
        super().visitCase(node)
"""
