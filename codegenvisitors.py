import re

import astclasses as ast
import semanticvisitors as sv


class RegManager:
    def __init__(self):
        # not R3 in regs, that's for TRP
        self.regs = ["R0", "R1", "R2", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11",
                     "R12", "R13", "R14", "R15"]
        self.given_regs = []

        """
        using stack heavy instead of registers could work well, 
        pushing things onto stack and working off of it, use less registers
        desugaring things means less assembly and codegen visitors 
        tons of stuff can be desugared and that would be great
        """

    def getReg(self, node):
        # try:
        reg = self.regs.pop()
        self.given_regs.append(reg)
        # print(node, reg)
        return reg
        # except:
        #     print("TODO no free regs")  # TODO

    def freeReg(self, reg):
        try:
            self.given_regs.remove(reg)
            # print("free", reg, self.__class__)
            self.regs.append(reg)
        except:
            # print("tried to free an already free reg")
            pass


"""nodes to desugar
        PLUS
        MINUS
        TIMES
        DIVIDE
        # these math should be one function that takes the op type and they basically work the same
        PLUSEQUALS
        MINUSEQUALS
        TIMESEQUALS
        DIVIDEEQUALS
        # these math assign should be the equals and then the math type above
        # MakeMathVisitor
        EQUALS
        DOUBLEEQUALS
        # these are not really changed
        NOTEQUALS
        # this will be not and then equals
        # NotEqualsVisitor
        LESSTHAN
        GREATERTHAN
        # these are not really changed
        LESSOREQUAL
        GREATEROREQUAL
        # these are going to be their < or > and then the double equals
        # LessOrGreater
        AND
        OR
        EXCLAMATIONMARK
        # these are not really changed
        NUM_LITERAL
        CHAR_LITERAL
        STRING_LITERAL
        TRUE
        FALSE
        NULL
        IDENTIFIER
        # these are pretty much without sugar already
        NEW
        # this is just gonna be itself, have to make a thing like a literal but
        # much more complicated to make and gotta slap on heap
        THIS
        # has to be on members to know if it's a member or not
        PERIOD
        # if it's an attribute gotta just load it I guess, if it's a method gotta call it
        INDEX
        # need to offset the variable to get to different things
        ARGUMENTS
        # this is just a list of params to be given to the function call to call
        """

"""nodes to desugar
        BRACES
        # this means a list of statements like a body
        EXPRESSION
        # this is a parent to most expressions (not initializers in var decls though) I'll keep it
        IF
        # "everything is an if" has expr, true statements, false statements (or just end)
        WHILE
        # turn into if
        # WhileToIf
        RETURN
        # opposite of the dot op, maybe can make them do something similar
        COUT
        CIN
        # these are TRP 1-4 and use R3 for the data to go to/from
        SWITCH
        # make it an if?
        # SwitchToIf
        BREAK
        # like a jump used in what are now ifs
        VAR_DECL
        # if these are in main, they should be put on the directives, maybe just put em all there though
        # could prefix ones in methods with the method name
        """

"""a case has it's ident which is the thing to match, and a true body to execute
        with switch these become if"""


class MathAssignDesugar(sv.Visitor):
    def visitExpr(self, node: ast.Expression):
        if node.op_type == ast.OpTypes.PLUSEQUALS:
            self.makeMath(ast.OpTypes.PLUS, node)
        if node.op_type == ast.OpTypes.MINUSEQUALS:
            self.makeMath(ast.OpTypes.MINUS, node)
        if node.op_type == ast.OpTypes.TIMESEQUALS:
            self.makeMath(ast.OpTypes.TIMES, node)
        if node.op_type == ast.OpTypes.DIVIDEEQUALS:
            self.makeMath(ast.OpTypes.DIVIDE, node)
        super().visitExpr(node)

    def makeMath(self, op, node):
        # node.left  # should be unchanged
        oldright = node.right
        if oldright is not None:
            node.right = ast.Expression(op)
            node.right.left = node.left
            node.right.right = oldright
            node.right.type = oldright.type
        node.op_type = ast.OpTypes.EQUALS


class NotEqualsVisitor(sv.Visitor):
    def visitExpr(self, node: ast.Expression):
        if node.op_type == ast.OpTypes.NOTEQUALS:
            self.makeNotEquals(node)
        super().visitExpr(node)

    def makeNotEquals(self, node):
        # node.left  # should be unchanged
        oldright = node.right
        if oldright is not None:
            node.right = ast.Expression(ast.OpTypes.DOUBLEEQUALS)
            node.right.left = node.left
            node.right.right = oldright
            node.right.type = oldright.type
        node.op_type = ast.OpTypes.EXCLAMATIONMARK
        node.left = None


class LessOrGreater(sv.Visitor):  # shockingly similar to the others, but small differences, figured it's fine
    def visitExpr(self, node: ast.Expression):
        if node.op_type == ast.OpTypes.LESSOREQUAL:
            self.makeLessGreater(ast.OpTypes.LESSTHAN, node)
        if node.op_type == ast.OpTypes.GREATEROREQUAL:
            self.makeLessGreater(ast.OpTypes.GREATERTHAN, node)
        super().visitExpr(node)

    def makeLessGreater(self, op, node):
        # node.left  # should be unchanged
        oldright = node.right
        oldleft = node.left
        if oldright is not None:
            node.right = ast.Expression(ast.OpTypes.DOUBLEEQUALS)
            node.right.left = oldleft
            node.right.right = oldright
            node.right.type = node.type
        if oldleft is not None:
            node.left = ast.Expression(op)
            node.left.left = oldleft
            node.left.right = oldright
            node.left.type = node.type
        node.op_type = ast.OpTypes.OR


class WhileToIf(sv.Visitor):
    def visitStmnt(self, node: ast.Statement):
        if node.statement_type == ast.StatementTypes.WHILE:
            node.statement_type = ast.StatementTypes.IF
            node.is_while = True  # sneaky
        super().visitStmnt(node)


# class SwitchToIf(sv.Visitor):
#     """I realized that switch's default should be just like the if's optional else but not optional
#     but it is a little different, oops"""
#     def __init__(self):
#         self.cur_method: ast.ClassAndMemberDeclaration = None
#         self.switch_ind = 0
#         self.cur_switch = None
#
#     def visitStmnt(self, node: ast.Statement):
#         if node.statement_type == ast.StatementTypes.SWITCH:
#             self.switch_ind = self.cur_method.body.index(node)
#             self.cur_switch = node
#         super().visitStmnt(node)
#
#     def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
#         if node.ident == "main" or node.member_type == ast.MemberTypes.METHOD \
#                 or node.member_type == ast.MemberTypes.CONSTRUCTOR:
#             self.cur_method = node
#         super().visitMemberDecl(node)
#
#     def visitCase(self, node: ast.Case):
#         # make a new if node
#         # get the current switches expression
#         # get the current case node's ident
#         # make an expression that is a bool type for the new if node
#         # set the new if node's substatement to the case node's substatement
#         # any breaks inside will need to go to the end of the default
#         # now I'm thinking maybe not desugar this more, just writing the code sounds easier
#
#         super().visitCase(node)


class IfTrueFalse(sv.Visitor):
    def __init__(self):
        pass

    def visitStmnt(self, node: ast.Statement):
        if node.statement_type == ast.StatementTypes.IF:
            iftrue = ast.Statement(ast.StatementTypes.IF_TRUE)
            iftrue.if_count = node.if_count
            node.substatement.insert(0, iftrue)
            # ok maybe just putting this in the substatement list will do, to help generate code
            iffalse = ast.Statement(ast.StatementTypes.IF_FALSE)
            iffalse.if_count = node.if_count
            iffalse.is_while = node.is_while
            iffalse.expr = node.expr
            node.substatement.append(iffalse)

        if node.statement_type == ast.StatementTypes.SWITCH:
            endcase = ast.Statement(ast.StatementTypes.END_CASE)
            node.case_list.append(endcase)
        super().visitStmnt(node)


class AddThisVisitor(sv.Visitor):
    def __init__(self, sym_table):
        self.prev_node = None
        self.cur_method = None
        self.cur_class = None
        self.sym_table = sym_table
        self.in_main = False

    def visitExpr(self, node: ast.Expression):
        # I gotta make it so that there can be local variable with same name as attribute in method
        # and if that is case then without the "this" it should default to the local one
        if not self.in_main:
            if node.op_type == ast.OpTypes.PERIOD and node.left.op_type == ast.OpTypes.THIS:
                node.left.type = self.cur_class.ident
            elif node.op_type == ast.OpTypes.PERIOD:
                pass
            elif node.op_type == ast.OpTypes.IDENTIFIER:
                if node.value not in self.sym_table[self.cur_class.ident][self.cur_method.ident]:
                    if isinstance(self.prev_node, ast.Statement):
                        dot = ast.Expression(ast.OpTypes.PERIOD)
                        self.prev_node.expr = dot
                        mythis = ast.Expression(ast.OpTypes.THIS)
                        mythis.type = self.cur_class.ident
                        dot.left = mythis
                        dot.right = node
                    if isinstance(self.prev_node, ast.Expression):
                        if self.prev_node.left == node:
                            dot = ast.Expression(ast.OpTypes.PERIOD)
                            self.prev_node.left = dot
                            mythis = ast.Expression(ast.OpTypes.THIS)
                            mythis.type = self.cur_class.ident
                            dot.left = mythis
                            dot.right = node
                        if self.prev_node.right == node:
                            dot = ast.Expression(ast.OpTypes.PERIOD)
                            self.prev_node.right = dot
                            mythis = ast.Expression(ast.OpTypes.THIS)
                            mythis.type = self.cur_class.ident
                            dot.left = mythis
                            dot.right = node
                super().visitExpr(node)
            else:
                self.prev_node = node
                super().visitExpr(node)

    def visitStmnt(self, node: ast.Statement):
        self.prev_node = node
        super().visitStmnt(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        if node.ident == "main":
            self.in_main = True
        if node.member_type == ast.MemberTypes.CLASS:
            self.cur_class = node
        if node.member_type == ast.MemberTypes.METHOD or node.member_type == ast.MemberTypes.CONSTRUCTOR:
            self.cur_method = node
        super().visitMemberDecl(node)


class VarInitToEquals(sv.Visitor):
    def __init__(self):
        pass

    def visitVarDecl(self, node: ast.VariableDeclaration):
        if node.init:
            oldinit = node.init
            eq = ast.Expression(ast.OpTypes.EQUALS)
            eq.right = oldinit
            identer = ast.Expression(ast.OpTypes.IDENTIFIER)
            identer.value = node.ident
            identer.type = node.type
            eq.left = identer
            node.init = eq
        super().visitVarDecl(node)


class VarsAndMembers(sv.Visitor):
    def __init__(self, sym_table, filename="a.asm"):
        self.cur_classname = None
        self.cur_funcname = None
        self.regs = RegManager()
        self.asmfile = open(filename, "w+")
        self.sym_table = sym_table
        self.in_main = False
        self.memberlines = {}
        self.primtypes = [ast.TypeTypes.BOOL, ast.TypeTypes.INT, ast.TypeTypes.CHAR, ]  # string? idk

    def visitVarDecl(self, node: ast.VariableDeclaration):
        """ok so the variables gotta go on the stack, so in main, I guess not use FP much,
        SP always points to top open space on stack. so put the variable there and increment by fours
        probably no matter the var just always give four bytes
        """
        if self.in_main:
            if node.type in self.primtypes:
                line = ""
                if node.array:  # then it's gotta be just new
                    if node.init:
                        line += f"{node.ident} .INT \n" \
                                f".INT {node.init.index.value}\n"
                        # so the plan is to put a label has the offset to real var in stack
                        # and the len of the array in next spot if it is one....
                    else:
                        line += f"{node.ident} .INT \n" \
                                f".INT 0\n"  # gotta update that with size if this gets a new int[] later
                else:
                    line = f"{node.ident} .INT \n"  # this would be to store the FP offset to stack memory
                self.asmfile.write(line)
            if node.type == ast.TypeTypes.STRING or node.is_obj:
                self.asmfile.write(f"{node.ident} .INT\n")
                self.asmfile.write(f"{node.ident}_{node.type}_{node.type} .INT\n")
        else:
            if node.type in self.primtypes:
                line = ""
                if node.array:  # then it's gotta be just new
                    if node.init:
                        line += f"{node.ident}_{self.cur_classname}_{self.cur_funcname} .INT \n" \
                                f".INT {node.init.index.value}\n"
                        # so the plan is to put a label has the offset to real var in stack
                        # and the len of the array in next spot if it is one....
                    else:
                        line += f"{node.ident}_{self.cur_classname}_{self.cur_funcname} .INT \n" \
                                f".INT 0\n"  # gotta update that with size if this gets a new int[] later
                elif not node.is_param:
                    line = f"{node.ident}_{self.cur_classname}_{self.cur_funcname} .INT \n"
                    # this would be to store the FP offset to stack memory
                self.asmfile.write(line)
            if node.type == ast.TypeTypes.STRING or node.is_obj:
                self.asmfile.write(f"{node.ident}_{self.cur_classname}_{self.cur_funcname} .INT \n")

        super().visitVarDecl(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        if node.ident == "main":
            self.in_main = True
            self.asmfile.write(f"universal_FP .INT\t;I'm putting this here to have a safe place to keep FP sometimes\n")

        if node.member_type == ast.MemberTypes.CLASS:
            self.cur_classname = node.ident
            self.asmfile.write(f"{node.ident}_~newval .INT\n")

        if node.member_type == ast.MemberTypes.METHOD or node.member_type == ast.MemberTypes.CONSTRUCTOR:
            self.cur_funcname = node.ident

        super().visitMemberDecl(node)

        if node.ident == "main":
            self.asmfile.write(f"JMP main\n")


class CodeGen(sv.Visitor):
    def __init__(self, asmfile, sym_table):
        self.in_if = []
        self.in_switch = []
        self.in_main = False
        self.cur_funcname = None
        self.cur_classname = None
        self.asmfile = asmfile
        self.sym_table = sym_table
        self.regs = RegManager()
        self.expr_reg_result = None
        self.if_count = 0
        self.switch_count = 0
        self.less_count = 0
        self.greater_count = 0
        self.equals_count = 0
        self.print_count = 0
        self.classnodes = {}
        self.funcnodes = {}
        self.math_ops = [
            ast.OpTypes.PLUS, ast.OpTypes.MINUS, ast.OpTypes.TIMES, ast.OpTypes.DIVIDE
        ]
        self.returns_bool = [
            ast.OpTypes.DOUBLEEQUALS,
            ast.OpTypes.LESSTHAN,
            ast.OpTypes.GREATERTHAN,
            ast.OpTypes.AND,
            ast.OpTypes.OR,
            ast.OpTypes.EXCLAMATIONMARK,
        ]

    def visitExpr(self, node: ast.Expression):
        if node.op_type == ast.OpTypes.DOUBLEEQUALS:
            node.reg = self.regs.getReg(node)
            # reg2 = self.regs.getReg(node)

        if node.op_type == ast.OpTypes.LESSTHAN:
            node.reg = self.regs.getReg(node)
            # reg2 = self.regs.getReg(node)

        if node.op_type == ast.OpTypes.GREATERTHAN:
            node.reg = self.regs.getReg(node)
            # reg2 = self.regs.getReg(node)

        super().visitExpr(node)

        if node.op_type == ast.OpTypes.PLUS:
            self.mathExpr(node, "ADD")
        if node.op_type == ast.OpTypes.MINUS:
            self.mathExpr(node, "SUB")
        if node.op_type == ast.OpTypes.TIMES:
            self.mathExpr(node, "MUL")
        if node.op_type == ast.OpTypes.DIVIDE:
            self.mathExpr(node, "DIV")

        if node.op_type == ast.OpTypes.EQUALS:
            line = ""
            if node.right.op_type == ast.OpTypes.EQUALS:
                line += node.right.line
                node.right = node.right.right  # I'll just destroy the tree on my way up
            if node.left.op_type == ast.OpTypes.IDENTIFIER and node.right.op_type == ast.OpTypes.IDENTIFIER:
                reg1 = self.regs.getReg(node)
                reg2 = self.regs.getReg(node)
                if node.left.classtype is True:  # is param
                    offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][2]
                    line += f"MOV {reg1}, FP\n" \
                            f"ADI {reg1}, #{offset}\n"
                elif not self.in_main:  # func local
                    line += f"LDR {reg1}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                            f"ADD {reg1}, FP\n"
                else:  # main param
                    line += f"LDR {reg1}, {node.left.value}\n"
                if node.right.classtype is True:
                    offset = self.sym_table[self.cur_classname][self.cur_funcname][node.right.value][2]
                    line += f"MOV {reg2}, FP\n" \
                            f"ADI {reg2}, #{offset}\n"
                elif not self.in_main:
                    line += f"LDR {reg2}, {node.right.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                            f"ADD {reg2}, FP\n"
                else:
                    line += f"LDR {reg2}, {node.right.value}\n"

                if node.left.type == ast.TypeTypes.STRING:
                    line += f"STR {reg2}, {node.left.value}\n"  # just copy the address over
                else:
                    line += f"LDR {reg2}, {reg2}\n" \
                        f"STR {reg2}, {reg1}\n"
                self.regs.freeReg(reg1)
                self.regs.freeReg(reg2)

            if (node.left.type == ast.TypeTypes.INT or node.left.type == ast.TypeTypes.BOOL) \
                    and node.left.op_type == ast.OpTypes.IDENTIFIER \
                    and node.right.reg is not None:
                # this SHOULD cover like if the right is everything except just a num lit
                reg1 = self.regs.getReg(node)
                line += node.right.line
                # line += f"LDR {reg1}, {node.left.value}\n"  # get the address
                if node.left.classtype is True:  # node is param
                    offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][2]
                    line += f"MOV {reg1}, FP\n" \
                            f"ADI {reg1}, #{offset}\n"
                elif not self.in_main:
                    line += f"LDR {reg1}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                        f"ADD {reg1}, FP\n"
                else:
                    line += f"LDR {reg1}, {node.left.value}\n"
                line += f"STR {node.right.reg}, {reg1}\n"  # put data at address
                self.regs.freeReg(node.right.reg)
                node.right.reg = None
                self.regs.freeReg(reg1)
            elif (node.left.type == ast.TypeTypes.INT or node.left.type == ast.TypeTypes.BOOL) \
                    and node.left.op_type == ast.OpTypes.IDENTIFIER \
                    and node.right.reg is None:
                # could be an int literal, could be dot with class attr, could be args with a dot and method
                # maybe
                if node.right.op_type == ast.OpTypes.NUM_LITERAL:
                    reg1 = self.regs.getReg(node)
                    reg2 = self.regs.getReg(node)
                    line += f"MOVI {reg1}, #{node.right.value}\n"
                    # line += f"LDR {reg2}, {node.left.value}\n"
                    if node.left.classtype is True:  # node is param
                        offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][2]
                        line += f"MOV {reg2}, FP\n" \
                                f"ADI {reg2}, #{offset}\n"
                    elif not self.in_main:
                        line += f"LDR {reg2}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                            f"ADD {reg2}, FP\n"
                    else:
                        line += f"LDR {reg2}, {node.left.value}\n"

                    line += f"STR {reg1}, {reg2}\n"
                    self.regs.freeReg(reg1)
                    self.regs.freeReg(reg2)
                if node.right.op_type == ast.OpTypes.TRUE:
                    reg1 = self.regs.getReg(node)
                    reg2 = self.regs.getReg(node)
                    line += f"MOVI {reg1}, #1\n"
                    # line += f"LDR {reg2}, {node.left.value}\n"
                    if node.left.classtype is True:  # node is param
                        offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][2]
                        line += f"MOV {reg2}, FP\n" \
                                f"ADI {reg2}, #{offset}\n"
                    elif not self.in_main:
                        line += f"LDR {reg2}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                            f"ADD {reg2}, FP\n"
                    else:
                        line += f"LDR {reg2}, {node.left.value}\n"
                    line += f"STR {reg1}, {reg2}\n"
                    self.regs.freeReg(reg1)
                    self.regs.freeReg(reg2)
                if node.right.op_type == ast.OpTypes.FALSE:
                    reg1 = self.regs.getReg(node)
                    reg2 = self.regs.getReg(node)
                    line += f"MOVI {reg1}, #0\n"
                    # line += f"LDR {reg2}, {node.left.value}\n"
                    if node.left.classtype is True:  # node is param
                        offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][2]
                        line += f"MOV {reg2}, FP\n" \
                                f"ADI {reg2}, #{offset}\n"
                    elif not self.in_main:
                        line += f"LDR {reg2}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                                f"ADD {reg2}, FP\n"
                    else:
                        line += f"LDR {reg2}, {node.left.value}\n"
                    line += f"STR {reg1}, {reg2}\n"
                    self.regs.freeReg(reg1)
                    self.regs.freeReg(reg2)

            if node.left.type == ast.TypeTypes.CHAR \
                    and node.left.op_type == ast.OpTypes.IDENTIFIER \
                    and node.right.reg is not None:
                # this SHOULD cover like if the right is everything except just a literal
                reg1 = self.regs.getReg(node)
                line += node.right.line
                # line += f"LDR {reg1}, {node.left.value}\n"  # get the address
                if node.left.classtype is True:  # node is param
                    offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][2]
                    line += f"MOV {reg1}, FP\n" \
                            f"ADI {reg1}, #{offset}\n"
                elif not self.in_main:
                    line += f"LDR {reg1}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                            f"ADD {reg1}, FP\n"
                else:
                    line += f"LDR {reg1}, {node.left.value}\n"
                line += f"STR {node.right.reg}, {reg1}\n"  # put data at address
                self.regs.freeReg(node.right.reg)
                node.right.reg = None
                self.regs.freeReg(reg1)
            elif node.left.type == ast.TypeTypes.CHAR or node.left.type == ast.TypeTypes.STRING \
                    and node.left.op_type == ast.OpTypes.IDENTIFIER \
                    and node.right.reg is None:
                if node.right.op_type == ast.OpTypes.CHAR_LITERAL:
                    reg1 = self.regs.getReg(node)
                    reg2 = self.regs.getReg(node)
                    if node.right.value == r"'\n'":
                        node.right.value = re.sub(r'\\n', '#10', node.right.value)
                        node.right.value = node.right.value[1:-1]
                    if node.right.value == r"'\t'":
                        node.right.value = re.sub(r'\\t', '#9', node.right.value)
                        node.right.value = node.right.value[1:-1]
                    if node.right.value == r"'\r'":
                        node.right.value = re.sub(r'\\r', '#12', node.right.value)
                        node.right.value = node.right.value[1:-1]
                    if node.right.value == "' '":
                        line += f"MOVI {reg1}, #32\n"
                    else:
                        line += f"MOVI {reg1}, {node.right.value}\n"
                    # line += f"LDR {reg2}, {node.left.value}\n"
                    if node.left.classtype is True:  # node is param
                        offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][2]
                        line += f"MOV {reg2}, FP\n" \
                                f"ADI {reg2}, #{offset}\n"
                    elif not self.in_main:
                        line += f"LDR {reg2}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                                f"ADD {reg2}, FP\n"  # TODO I hope this local var defining is correct... lol
                    else:
                        line += f"LDR {reg2}, {node.left.value}\n"

                    line += f"STR {reg1}, {reg2}\n"
                    self.regs.freeReg(reg1)
                    self.regs.freeReg(reg2)

                elif node.right.op_type == ast.OpTypes.STRING_LITERAL:  # assign str lit to var
                    # strings are kept on "heap"!
                    reg1 = self.regs.getReg(node)
                    reg2 = self.regs.getReg(node)
                    val = node.right.value
                    val = re.sub(r'\\n', '\n', val)
                    val = re.sub(r'\\t', '\t', val)
                    val = re.sub(r'\\r', '\r', val)
                    off = 0
                    if self.in_main:
                        self.sym_table[self.cur_classname][node.left.value][4] = len(val[1:-1])
                    else:
                        if node.left.value in self.sym_table[self.cur_classname]:
                            self.sym_table[self.cur_classname][node.left.value][4] = len(val[1:-1])
                        else:
                            self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][4] = len(val[1:-1])
                    for c in val[1:]:
                        if c == '\n':
                            line += f"MOVI {reg1}, #10\n"
                        elif c == '\t':
                            line += f"MOVI {reg1}, #9\n"
                        elif c == '\r':
                            line += f"MOVI {reg1}, #12\n"
                        elif c == ' ':
                            line += f"MOVI {reg1}, #32\n"
                        else:
                            line += f"MOVI {reg1}, '{c}'\n"
                        if node.left.classtype is True:  # node is param
                            # string param in a function and try to write to it, maybe this is illegal
                            offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][2]
                            line += f"MOV {reg2}, FP\n" \
                                    f"ADI {reg2}, #{offset}\n"
                        elif not self.in_main:
                            line += f"LDR {reg2}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n"
                        else:
                            line += f"LDR {reg2}, {node.left.value}\n"
                        line += f"ADI {reg2}, #{off}\n"
                        line += f"STR {reg1}, {reg2}\n"
                        off += 4
                    self.regs.freeReg(reg1)
                    self.regs.freeReg(reg2)

            if node.right.op_type == ast.OpTypes.NEW:
                line += node.right.line
                if node.left.classtype is True:  # param
                    pass  # this is just if I'm giving an object that was passed in a new.
                elif not self.in_main:  # local func
                    reg1 = self.regs.getReg(node)
                    line += f"LDR {reg1}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                            f"ADD {reg1}, FP\n" \
                            f"LDR {node.right.reg}, {node.left.type}_~newval\n" \
                            f"STR {node.right.reg}, {reg1}\n"
                    self.regs.freeReg(reg1)
                else:  # main param
                    line += f"LDR {node.right.reg}, {node.left.type}_~newval\n" \
                            f"STR {node.right.reg}, {node.left.value}\n" \
                            f"STR {node.right.reg}, {node.left.value}_{node.left.type}_{node.left.type}\n"
                            # this one's for constructors to modify?
                self.regs.freeReg(node.right.reg)
                node.right.reg = None

            def assnToDotArg(line, reg1):
                # if an expr . called this, gotta get addr
                reg2 = self.regs.getReg(node)
                # calculate node.right
                if node.right.reg:
                    line += node.right.line
                elif node.right.op_type == ast.OpTypes.NUM_LITERAL:
                    line += f"MOVI {reg1}, #{node.right.value}\n"
                elif node.right.op_type == ast.OpTypes.CHAR_LITERAL:
                    if node.right.value == "' '":
                        line += f"MOVI {reg1}, #32\n"
                    else:
                        line += f"MOVI {reg1}, {node.right.value}\n"
                elif node.right.op_type == ast.OpTypes.STRING_LITERAL:
                    pass  # TODO assign string lits to data members
                elif node.right.op_type == ast.OpTypes.TRUE:
                    line += f"MOVI {reg1}, #1\n"
                elif node.right.op_type == ast.OpTypes.FALSE:
                    line += f"MOVI {reg1}, #0\n"
                elif node.right.op_type == ast.OpTypes.IDENTIFIER:
                    if node.right.classtype is True:  # param
                        offset = self.sym_table[self.cur_classname][self.cur_funcname][node.right.value][2]
                        line += f"MOV {reg1}, FP\n" \
                                f"ADI {reg1}, #{offset}\n" \
                                f"LDR {reg1}, {reg1}\n"
                    elif not self.in_main:  # local
                        line += f"LDR {reg1}, {node.right.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                                f"ADD {reg1}, FP\n" \
                                f"LDR {reg1}, {reg1}\n"
                    else:  # in main
                        line += f"LDR {reg1}, {node.right.value}\n" \
                                f"LDR {reg1}, {reg1}\n"

                # get node.left addr to put node.right stuff in
                if node.left.op_type == ast.OpTypes.PERIOD:
                    if node.left.left.classtype is True:  # param
                        offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.left.value][2]
                        line += f"MOV {reg2}, FP\n" \
                                f"ADI {reg2}, #{offset}\n" \
                                f"LDR {reg2}, {reg2}\n"
                    elif not self.in_main:  # local var?
                        if self.cur_classname == self.cur_funcname:  # if in constructor do something slightly different
                            line += f"MOV {reg2}, FP\n" \
                                    f"ADI {reg2}, #-8\t;access self in constructor\n" \
                                    f"LDR {reg2}, {reg2}\n"
                        else:
                            if node.left.left.value not in self.sym_table[self.cur_classname][self.cur_funcname]:
                                # must be a this.datamember?
                                line += f"MOV {reg2}, FP\n" \
                                    f"ADI {reg2}, #-8\t;access self\n" \
                                    f"LDR {reg2}, {reg2}\n"
                            else:
                                line += f"LDR {reg2}, {node.left.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                                    f"ADD {reg2}, FP\n" \
                                    f"LDR {reg2}, {reg2}\n"
                    else:  # in main
                        line += f"LDR {reg2}, {node.left.left.value}\n"
                    # gotta offset reg2 to get to the right spot...
                    memlist = list(self.sym_table[node.left.left.type].keys())[1:]
                    off = memlist.index(node.left.right.value)
                    line += f"ADI {reg2}, #{off * 4}\n"
                else:  # node == ARGS
                    pass

                # finally do the store
                if node.right.reg:
                    line += f"STR {node.right.reg}, {reg2}\n"
                    self.regs.freeReg(node.right.reg)
                    node.right.reg = None
                else:
                    line += f"STR {reg1}, {reg2}\n"
                self.regs.freeReg(reg2)
                return line

            if node.left.op_type == ast.OpTypes.PERIOD:
                self.regs.freeReg(node.left.reg)
                reg1 = self.regs.getReg(node)
                line += assnToDotArg("", reg1)
                self.regs.freeReg(reg1)

            if node.left.op_type == ast.OpTypes.ARGUMENTS:
                reg1 = self.regs.getReg(node)
                line += assnToDotArg("", reg1)
                self.regs.freeReg(reg1)

            node.line = line

        if node.op_type == ast.OpTypes.DOUBLEEQUALS:
            self.cmpExprs(node, node.reg)

        if node.op_type == ast.OpTypes.LESSTHAN:
            self.cmpExprs(node, node.reg)

        if node.op_type == ast.OpTypes.GREATERTHAN:
            self.cmpExprs(node, node.reg)

        if node.op_type == ast.OpTypes.AND:
            self.andOr(node, "AND")

        if node.op_type == ast.OpTypes.OR:
            self.andOr(node, "OR")

        if node.op_type == ast.OpTypes.EXCLAMATIONMARK:
            # currently, should make these not write to file, but write to their node.line
            # self.returns_bool = [ast.OpTypes.DOUBLEEQUALS, ast.OpTypes.LESSTHAN,
            #     ast.OpTypes.GREATERTHAN, ast.OpTypes.AND, ast.OpTypes.OR,]
            if node.right.op_type in self.returns_bool:
                line = node.right.line
                line += f"NOT {node.right.reg}\n"
                node.reg = node.right.reg
                node.right.reg = None  # don't free it, just take it for later
                node.line = line
            elif node.right.op_type == ast.OpTypes.TRUE:
                reg0 = self.regs.getReg(node)
                line = f"MOVI {reg0}, #0"
                node.reg = reg0
                node.line = line
            elif node.right.op_type == ast.OpTypes.FALSE:
                reg0 = self.regs.getReg(node)
                line = f"MOVI {reg0}, #1"
                node.reg = reg0
                node.line = line

        # if node.op_type == ast.OpTypes.NULL:
        #     pass
        if node.op_type == ast.OpTypes.NEW and not node.index:
            def write_param(param):
                # a param could be something with a line and reg,
                # it could be a num/char/string lit or true/false,
                # it could be identifier, hopefully I'm not missing something here
                pline = ""
                if self.in_main and param.op_type == ast.OpTypes.IDENTIFIER:
                    pline += f"LDR R3, {param.value}\n" \
                            f"LDR R3, R3\n"
                elif not self.in_main and param.op_type == ast.OpTypes.IDENTIFIER and param.classtype is False:
                    reg1 = self.regs.getReg(node)
                    pline += f"LDR R3, {param.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                             f"ADD {reg1}, FP\n" \
                             f"LDR R3, {reg1}\n"  # FP - offset to get value
                    self.regs.freeReg(reg1)
                elif not self.in_main and param.op_type == ast.OpTypes.IDENTIFIER and param.classtype is True:
                    offset = self.sym_table[self.cur_classname][self.cur_funcname][param.value][2]
                    pline += f"MOV R3, FP\n" \
                            f"ADI R3, #{offset}\n" \
                            f"LDR R3, R3\n"

                elif param.op_type == ast.OpTypes.NUM_LITERAL:
                    pline += f"MOVI R3, #{param.value}\n"
                elif param.op_type == ast.OpTypes.CHAR_LITERAL:
                    if param.value == "' '":
                        pline += f"MOVI R3, #32\n"
                    else:
                        pline += f"MOVI R3, {param.value}\n"
                elif param.op_type == ast.OpTypes.STRING_LITERAL:
                    pass  # TODO: make strings passable to constructors
                elif param.op_type == ast.OpTypes.TRUE:
                    pline += f"MOVI R3, #1\n"
                elif param.op_type == ast.OpTypes.FALSE:
                    pline += f"MOVI R3, #0\n"
                elif param.line and param.reg:
                    pline += param.line
                    pline += f"MOV R3, {param.reg}\n"
                    self.regs.freeReg(param.reg)
                    param.reg = None
                pline += f"STR R3, SP\n" \
                        f"ADI SP, #-4\n"
                # STR R3, SP          ;STORE param-1's value on Stack
                # ADI SP, #-4         ;point to next int on stack
                return pline

            reg0 = self.regs.getReg(node)
            reg1 = self.regs.getReg(node)
            reg2 = self.regs.getReg(node)
            # make a call to ALLC, with a reg that gets the addr,
            # and a #number that says how many spaces (a space is 4 bytes)
            size = self.sym_table[node.type]["self"][0]
            constructor = self.sym_table[node.type]["self"][1]
            line = f"ALLC {reg0}, #{size}\n" \
                   f"STR {reg0}, {node.type}_~newval\n"  # put addr of new thing in directives for temp storage
            # activation record goes from bottom up ret addr/val, prev frame ptr, param1 ...
            if constructor:
                initlist = self.sym_table[node.type]["self"][2]
                line += f"""
    MOV {reg1}, SP          ;save current SP into {reg1} so we can assign it to FP
    MOV {reg2}, SP          ;save sp
    ADI {reg2}, #-16
    CMP {reg2}, SL
    BLT {reg2}, STACKOVERFLOW

    ADI SP, #-4         ;reserve space for ret addr on stack
    STR FP, SP          ;store FP => 0, into PFP
    ADI SP, #-4         ;point to next int on stack
    ; params
    ; first one gonna be addr of space on heap
    STR {reg0}, SP
    ADI SP, #-4
"""
                if node.args:
                    for a in node.args:
                        line += write_param(a)

                line += f"""
    MOV FP, {reg1}          ;set FP == Former/Original SP
    ; put that below params
    MOV {reg1}, SP          ;save sp - check for stack overflow
    CMP {reg1}, SL
    BLT {reg1}, STACKOVERFLOW
    MOV {reg1}, PC          ;save current PC (which points at next instruction when executing
    ADI {reg1}, #36
    STR {reg1}, FP
    JMP {node.type}_{node.type}

    MOV SP, FP          ;get rid of top (no longer needed) frame
    MOV {reg1}, FP          ;SP <= FP
    ADI {reg1}, #-4         ;get the PFP

    LDR R3, FP          ;get ret val to put in frame

    LDR FP, {reg1}          ;FP = PFP
    MOV {reg2}, SP          ;check for stackunderflow
    CMP {reg2}, SB
    BGT {reg2}, STACKUNDERFLOW
"""
            else:  # no constructor, gonna init things
                def datamemberCode(node):
                    # code that was in the if-datamember section
                    def doInitReg():
                        line = node.init.line
                        line += f"MOV {reg1}, {node.init.reg}\n"
                        self.regs.freeReg(node.init.reg)
                        node.init.reg = None

                    reg1 = self.regs.getReg(node)
                    if node.init and node.ret_type == ast.TypeTypes.INT or node.ret_type == ast.TypeTypes.BOOL:
                        if node.init.reg:
                            line = doInitReg()
                        else:
                            line = f"MOVI {reg1}, #{node.init.value}\n"
                    elif node.init and node.ret_type == ast.TypeTypes.CHAR:
                        if node.init.reg:
                            line = doInitReg()
                        else:
                            line = f"MOVI {reg1}, {node.init.value}\n"
                    elif node.init and node.ret_type == ast.TypeTypes.STRING:
                        line = f"ALLC {reg1}, #{len(node.init.value[1:])}\n"
                        reg2 = self.regs.getReg(node)
                        reg3 = self.regs.getReg(node)
                        line += f"MOV {reg3}, {reg1}\n"
                        val = node.init.value[1:]
                        val = re.sub(r'\\n', '\n', val)
                        val = re.sub(r'\\t', '\t', val)
                        val = re.sub(r'\\r', '\r', val)
                        off = 4
                        for c in val:
                            if c == '\n':
                                line += f"MOVI {reg2}, #10\n"
                            elif c == '\t':
                                line += f"MOVI {reg2}, #9\n"
                            elif c == '\r':
                                line += f"MOVI {reg2}, #12\n"
                            elif c == ' ':
                                line += f"MOVI {reg2}, #32\n"
                            else:
                                line += f"MOVI {reg2}, '{c}'\n"
                            line += f"STR {reg2}, {reg3}\n" \
                                    f"ADI {reg3}, #{off}\n"
                            off += 4
                        self.regs.freeReg(reg2)
                        self.regs.freeReg(reg3)
                    else:
                        line = f"MOVI {reg1}, #0\n"
                    node.line = line
                    node.reg = reg1
                    # end of datamember code

                # memlist = list(self.sym_table[node.type].items())[1:]
                decllist = self.sym_table[node.type]["self"][2]
                line += f"MOV {reg2}, {reg0}\n"
                off = 4
                for n in decllist:
                    if n is not None:
                        datamemberCode(n)
                        line += n.line
                        line += f"STR {n.reg}, {reg2}\n" \
                                f"ADI {reg2}, #{off}\n"
                        off += 4
                        self.regs.freeReg(n.reg)
                        n.reg = None
                    else:  # functions put none in spot
                        # just put a 0 in that spot
                        line += f"ADI {reg2}, #{off}\n"
            node.line = line
            node.reg = reg0
            self.regs.freeReg(reg1)
            self.regs.freeReg(reg2)

        if node.op_type == ast.OpTypes.PERIOD:
            """expr period"""
            if node.right.args == "method":
                pass  # this is handled in expr arguments
            else:
                line = ""
                reg1 = self.regs.getReg(node)
                # access the data member that is node.right
                # follow the node.left (an identifier) to the data member
                # I think should put value in reg to plug and play with rest of expressions
                # except for the expr equals, will have to do same thing but not dereference
                attrlist = list(self.sym_table[node.left.type].keys())[1:]
                heapoff = attrlist.index(node.right.value)
                heapoff *= 4
                if node.left.classtype is True:  # param obj
                    offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][2]
                    line += f"MOV {reg1}, FP\n" \
                            f"ADI {reg1}, #{offset}\n" \
                            f"LDR {reg1}, {reg1}\n" \
                            f"ADI {reg1}, #{heapoff}\n" \
                            f"LDR {reg1}, {reg1}\n"
                elif not self.in_main:  # local func obj
                    if node.right.value not in self.sym_table[self.cur_classname][self.cur_funcname]:
                        # it's a data member, not local func var
                        line = f"MOV {reg1}, FP\n" \
                                f"ADI {reg1}, #-8\n" \
                                f"LDR {reg1}, {reg1}\n"
                        memlist = list(self.sym_table[node.left.type].keys())[1:]
                        off = memlist.index(node.right.value)
                        line += f"ADI {reg1}, #{off * 4}\n" \
                                f"LDR {reg1}, {reg1}\n"  # at this point should finally have data member's value
                    else:
                        line += f"LDR {reg1}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                            f"ADD {reg1}, FP\n" \
                            f"LDR {reg1}, {reg1}\t;dereference to get the heap addr\n" \
                            f"ADI {reg1}, #{heapoff}\n" \
                            f"LDR {reg1}, {reg1}\n"
                else:  # main decl'd obj
                    line += f"LDR {reg1}, {node.left.value}\n" \
                            f"ADI {reg1}, #{heapoff}\n" \
                            f"LDR {reg1}, {reg1}\n"

                node.line = line
                node.reg = reg1


        if node.op_type == ast.OpTypes.INDEX:
            pass  # should make these not write to file, but write to their node.line

        if node.op_type == ast.OpTypes.ARGUMENTS:
            """expr args"""
            def write_param(param):
                # a param could be something with a line and reg,
                # it could be a num/char/string lit or true/false,
                # it could be identifier, hopefully I'm not missing something here
                pline = ""
                if self.in_main and param.op_type == ast.OpTypes.IDENTIFIER:
                    prims = [ast.TypeTypes.CHAR, ast.TypeTypes.BOOL, ast.TypeTypes.INT]
                    if param.type == ast.TypeTypes.STRING or param.type not in prims:
                        pline += f"LDR R3, {param.value}\n"
                    else:
                        pline += f"LDR R3, {param.value}\n" \
                             f"LDR R3, R3\n"
                elif not self.in_main and param.op_type == ast.OpTypes.IDENTIFIER and param.classtype is False:
                    # TODO pass strings to func that are local var
                    pline += f"LDR R3, {param.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                             f"ADD R3, FP\n" \
                             f"LDR R3, R3\n"  # FP - offset to get value
                elif not self.in_main and param.op_type == ast.OpTypes.IDENTIFIER and param.classtype is True:
                    # TODO pass strings to func that are param vars
                    offset = self.sym_table[self.cur_classname][self.cur_funcname][param.value][2]
                    pline += f"MOV R3, FP\n" \
                             f"ADI R3, #{offset}\n" \
                             f"LDR R3, R3\n"

                elif param.op_type == ast.OpTypes.NUM_LITERAL:
                    pline += f"MOVI R3, #{param.value}\n"
                elif param.op_type == ast.OpTypes.CHAR_LITERAL:
                    if param.value == "' '":
                        pline += f"MOVI R3, #32\n"
                    else:
                        pline += f"MOVI R3, {param.value}\n"
                elif param.op_type == ast.OpTypes.STRING_LITERAL:
                    pass  # TODO: make string lits passable
                elif param.op_type == ast.OpTypes.TRUE:
                    pline += f"MOVI R3, #1\n"
                elif param.op_type == ast.OpTypes.FALSE:
                    pline += f"MOVI R3, #0\n"
                elif param.line and param.reg:
                    pline += param.line
                    pline += f"MOV R3, {param.reg}\n"
                    self.regs.freeReg(param.reg)
                    param.reg = None
                pline += f"STR R3, SP\n" \
                         f"ADI SP, #-4\n"
                # STR R3, SP          ;STORE param-1's value on Stack
                # ADI SP, #-4         ;point to next int on stack
                return pline

            reg1 = self.regs.getReg(node)
            reg2 = self.regs.getReg(node)
            reg3 = self.regs.getReg(node)
            line = ""

            if not self.in_main and node.left.right == self.cur_funcname and node.args:
                off = -12  # magic number, to skip past the ret addr spot and pfp spot
                for a in node.args:
                    # this is like starting to build the next frame
                    line += f"MOV {reg1}, SP\t;trying to put old params on stack to recurse\n" \
                           f"ADI {reg1}, #{off}\n" \
                           f"MOV R3, FP\n" \
                           f"ADI R3, #{off}\n" \
                           f"LDR R3, R3\n" \
                           f"STR R3, {reg1}\n"
                    off -= 4
            funcsize = self.sym_table[node.left.right.classtype][node.left.right.value]["self"][2]
            # activation record goes from bottom up ret addr/val, prev frame ptr, param1 ...
            line += f"""
            
            MOV {reg1}, SP          ;save current SP into {reg1} so we can assign it to FP
            STR {reg1}, universal_FP
            MOV {reg2}, SP          ;save sp
            ADI {reg2}, #{funcsize}  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP {reg2}, SL
            BLT {reg2}, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params\n\n"""
            # add addr of "this" as first param, for possibly changing its data members
            if node.left.left.op_type == ast.OpTypes.THIS:
                # get FP -8 (this addr) and put it on stack again
                line += f"MOV R3, FP\n" \
                        f"ADI R3, #-8\n" \
                        f"LDR R3, R3\n" \
                        f"STR R3, SP\n" \
                        f"ADI SP, #-4\n"
            else:
                if self.in_main:
                    # get {node.left.left.value} put that on stack
                    line += f"LDR R3, {node.left.left.value}\n" \
                            f"STR R3, SP\n" \
                            f"ADI SP, #-4\n"
                else:
                    if node.left.left.value not in self.sym_table[self.cur_classname][self.cur_funcname]:
                        # what about a datamember obj? (this.obj.func() or this.obj.attr)
                        # gotta get this's obj member
                        line += f"MOV R3, FP\n" \
                                f"ADI R3, #-8\n" \
                                f"LDR R3, R3\n"
                        memlist = list(self.sym_table[node.left.left.type].keys())[1:]
                        off = memlist.index(node.left.right.value)
                        line += f"ADI R3, #{off * 4}\n" \
                                f"LDR R3, R3\n;idk lel\n" \
                                f"STR R3, SP\n" \
                                f"ADI SP, #-4\n"  # TODO fiddling with "this" in args
                    else:
                        # or maybe {node.left.left.value}_{self.cur_classname}_{self.cur_funcname}
                        # if it's a func local var obj
                        line += f"LDR R3, {node.left.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                            f"STR R3, SP\n" \
                            f"ADI SP, #-4\n"
            if node.args:
                for a in node.args:
                    line += write_param(a)

            line += f"""
            LDR {reg1}, universal_FP
            MOV FP, {reg1}          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV {reg1}, SP          ;save sp - check for stack overflow
            CMP {reg1}, SL
            BLT {reg1}, STACKOVERFLOW
            MOV {reg1}, PC          ;save current PC (which points at next instruction when executing
            ADI {reg1}, #36
            STR {reg1}, FP
            JMP {node.left.right.value}_{node.left.right.classtype}

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV {reg1}, FP          ;SP <= FP
            ADI {reg1}, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR {reg3}, FP      ;and one for oher uses just in case
        
            LDR FP, {reg1}          ;FP = PFP
            MOV {reg2}, SP          ;check for stackunderflow
            CMP {reg2}, SB
            BGT {reg2}, STACKUNDERFLOW\n"""
            node.line = line
            node.reg = reg3
            self.regs.freeReg(reg1)
            self.regs.freeReg(reg2)

        # super().visitExpr(node)

    def visitStmnt(self, node: ast.Statement):
        if node.statement_type == ast.StatementTypes.IF:
            node.if_count = self.if_count
            self.if_count += 1
            for s in node.substatement:
                s.if_count = node.if_count
            line = f"IF{node.if_count}start MOV R0, R0\n"
            self.asmfile.write(line)
            node.expr.accept(self)  # this will cause an extra node visit... worth?
            self.ifCheckExpr(node, "false")
            self.in_if.append(node)

        if node.statement_type == ast.StatementTypes.RETURN:
            reg0 = self.regs.getReg(node)
            node.reg = reg0

        if node.statement_type == ast.StatementTypes.SWITCH:
            node.switch_count = self.switch_count
            self.switch_count += 1
            for s in node.case_list:
                s.switch_count = node.switch_count
            line = f"SWITCH{node.switch_count}start MOV R0, R0\n"
            self.in_switch.append(node)
            def hashtagOrNot(notnode, hashtag):
                # write comparisons for each case's "ident"
                reg1 = self.regs.getReg(node)
                switchval = notnode.expr.value
                notline = ""
                for c in notnode.case_list:
                    if isinstance(c, ast.Case):
                        if notnode.expr.op_type == ast.OpTypes.IDENTIFIER:
                            if self.in_main:
                                notline += f"LDR {reg1}, {notnode.expr.value}\n" \
                                        f"LDR {reg1}, {reg1}\n"
                            elif not self.in_main and notnode.expr.classtype is False:
                                notline += f"LDR {reg1}, {notnode.expr.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                                        f"ADD {reg1}, FP\n" \
                                        f"LDR {reg1}, {reg1}\n"
                            elif not self.in_main and notnode.expr.classtype is True:
                                offset = self.sym_table[self.cur_classname][self.cur_funcname][notnode.expr.value][2]
                                notline += f"MOV {reg1}, FP\n" \
                                        f"ADI {reg1}, #{offset}\n" \
                                        f"LDR {reg1}, {reg1}\n"
                            switchval = reg1  # which means we don't need it
                        else:
                            notline += f"MOVI {reg1}, {hashtag}{switchval}\n"

                        notline += f"CMPI {reg1}, {hashtag}{c.ident}\n" \
                                   f"BRZ {reg1}, SWITCH{notnode.switch_count}case{c.ident}\n"

                self.regs.freeReg(reg1)
                notline += f"JMP DEFAULT{node.switch_count}start\n"
                return notline

            if node.expr.type == ast.TypeTypes.INT:
                line += hashtagOrNot(node, "#")
            elif node.expr.type == ast.TypeTypes.CHAR:
                line += hashtagOrNot(node, "")
            self.asmfile.write(line)

        if node.statement_type == ast.StatementTypes.END_CASE:
            self.asmfile.write(f"DEFAULT{node.switch_count}start MOV R0, R0\n")

        if node.statement_type == ast.StatementTypes.BREAK:
            if self.in_if:
                self.asmfile.write(f"JMP IF{self.in_if[-1].if_count}end\n")
            elif self.in_switch:
                self.asmfile.write(f"JMP SWITCH{self.in_switch[-1].switch_count}end\n")

        if node.statement_type == ast.StatementTypes.IF_TRUE:
            line = f"IF{node.if_count}true MOV R0 R0\n"
            self.asmfile.write(line)

        if node.statement_type == ast.StatementTypes.IF_FALSE:
            # write if-true's ending stuff
            line = ""
            if node.is_while:
                self.ifCheckExpr(node, "true")  # should free the expr's reg
            else:
                line += f"JMP IF{node.if_count}end\n"
                self.regs.freeReg(node.expr.reg)  # weird I have to free it here, the tree is deceiving
                node.expr.reg = None
                # write if-false's beginning stuff
            line += f"IF{node.if_count}false MOV R0 R0\n"
            self.asmfile.write(line)

        super().visitStmnt(node)

        if node.statement_type == ast.StatementTypes.COUT:
            self.cinout(node, ("#1", "#3"), "cout")

        if node.statement_type == ast.StatementTypes.CIN:
            self.cinout(node, ("#2", "#4"), "cin")

        if node.statement_type == ast.StatementTypes.COUT or node.statement_type == ast.StatementTypes.CIN:
            self.regs.freeReg(node.expr.reg)
            node.expr.reg = None

        if node.statement_type == ast.StatementTypes.BRACES:
            pass

        if node.statement_type == ast.StatementTypes.EXPRESSION:
            if node.expr.line:
                self.asmfile.write(node.expr.line)
                self.regs.freeReg(node.expr.reg)
                node.expr.reg = None

        if node.statement_type == ast.StatementTypes.IF:
            # now we are below the super() call
            line = f"IF{node.if_count}end MOV R0, R0\n"
            self.asmfile.write(line)
            self.in_if.pop()

        if node.statement_type == ast.StatementTypes.IF_FALSE:
            pass

        if node.statement_type == ast.StatementTypes.RETURN:
            line = f"LDR {node.reg}, FP          ; load ret addr\n"
            reg1 = self.regs.getReg(node)
            if node.expr.op_type == ast.OpTypes.ARGUMENTS:  # probably recurse?
                line += node.expr.line
                line += f"LDR {node.reg}, FP\n"  # above I make new line to not put this line in  until now
                line += f"MOV R3, R3\n"
            elif node.expr.reg:
                line += node.expr.line
                line += f"MOV R3, {node.expr.reg}\n"
                # TODO this doesn't work for NEW
                if node.expr.left and (node.expr.left.op_type == ast.OpTypes.ARGUMENTS or node.expr.right.op_type == ast.OpTypes.ARGUMENTS):
                    line += f"LDR {node.reg}, FP\n"  # I just put this here because it can help... but not great solution
                self.regs.freeReg(node.expr.reg)
                node.expr.reg = None
            elif node.expr.op_type == ast.OpTypes.NUM_LITERAL:
                line += f"MOVI R3, #{node.expr.value}\n"
            elif node.expr.op_type == ast.OpTypes.CHAR_LITERAL:
                if {node.expr.value} == "' '":  # temp fix? todo
                    line += f"MOVI R3, #32\n"
                else:
                    line += f"MOVI R3, {node.expr.value}\n"
            elif node.expr.op_type == ast.OpTypes.STRING_LITERAL:
                pass  # TODO make funcs return strings
            elif node.expr.op_type == ast.OpTypes.TRUE:
                line += f"MOVI R3, #1\n"
            elif node.expr.op_type == ast.OpTypes.FALSE:
                line += f"MOVI R3, #0\n"

            elif node.expr.op_type == ast.OpTypes.IDENTIFIER:
                if node.expr.classtype is True:  # it's param
                    offset = self.sym_table[self.cur_classname][self.cur_funcname][node.expr.value][2]
                    line += f"MOV R3, FP\n" \
                            f"ADI R3, #{offset}\n"
                    if node.expr.type != ast.TypeTypes.STRING:  # just dereference if it's not a string
                        line += f"LDR R3, R3\n"
                elif not self.in_main:  # it's local var
                    line += f"LDR R3, {node.expr.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                            f"ADD R3, FP\n"
                    if node.expr.type != ast.TypeTypes.STRING:
                        line += f"LDR R3, R3\n"
            line += f"""
            MOV {reg1}, R3          ; get ret val
            STR {reg1}, FP          ; store ret val where ret addr was\n"""
            self.regs.freeReg(reg1)
            line += f"JMR {node.reg}\n\n\n"
            self.asmfile.write(line)
            self.regs.freeReg(node.reg)

        if node.statement_type == ast.StatementTypes.SWITCH:
            self.asmfile.write(f"SWITCH{node.switch_count}end MOV R0, R0\n")
            self.in_switch.pop()

    def visitVarDecl(self, node: ast.VariableDeclaration):
        """ok so the variables gotta go on the stack, so in main, I guess not use FP much,
        SP always points to top open space on stack. so put the variable there and increment by fours
        probably no matter the var just always give four bytes
        """
        reg1 = self.regs.getReg(node)
        if not self.in_main and not node.is_param:
            if node.type == ast.TypeTypes.STRING:
                if node.init and node.init.right:
                    strlen = len(node.init.right.value)  # might not always be there...
                    line = f"ALLC {reg1}, #{strlen}\n" \
                           f"STR {reg1}, {node.ident}_{self.cur_classname}_{self.cur_funcname}\n"
                else:
                    strlen = 32  # TODO just giving default length for string here
                    line = f"ALLC {reg1}, #{strlen}\n" \
                           f"STR {reg1}, {node.ident}_{self.cur_classname}_{self.cur_funcname}\n"
            else:
                line = f"MOV R3, FP\n" \
                   f"MOV {reg1}, SP\n" \
                   f"SUB {reg1}, R3\n" \
                   f"STR {reg1}, {node.ident}_{self.cur_classname}_{self.cur_funcname}\n" \
                   f"ADI SP, #-4\n"  # trying to make local vars idents store their offset

        elif node.is_param:
            line = f""

        else:  # TODO ADI SP up here messes with arrays? maybe not if they're on heap
            if node.type == ast.TypeTypes.STRING:
                if node.init and node.init.right:
                    strlen = len(node.init.right.value)  # might not always be there...
                    line = f"ALLC {reg1}, #{strlen}\n" \
                           f"STR {reg1}, {node.ident}\n"
                else:
                    strlen = 32  # TODO just giving default length for string here
                    line = f"ALLC {reg1}, #{strlen}\n" \
                           f"STR {reg1}, {node.ident}\n"
            else:
                line = f"MOV {reg1}, SP\n" \
                   f"STR {reg1}, {node.ident}\n" \
                   f"ADI SP, #-4\n"
        #
        # start calling their initializers
        if node.type == ast.TypeTypes.INT:
            if node.array:  # TODO should be on heap
                if node.init:
                    numlines = node.init.index.value
                    line += f"MOVI {reg1}, #{0}\t;put local var array {node.ident} on stack\n"
                    for x in range(numlines):
                        line += f"STR {reg1}, SP\n"
                        line += f"ADI SP, #-4\n"
            elif node.init:
                node.init.accept(self)  # pre traversal watch out
                line += node.init.line

        if node.type == ast.TypeTypes.CHAR:
            if node.array:  # then it's gotta be just new
                if node.init:
                    numlines = node.init.index.value
                    line += f"MOVI {reg1}, #{0}\t;put local var array {node.ident} on stack\n"
                    for x in range(numlines):
                        line += f"STR {reg1}, SP\n"
                        line += f"ADI SP, #-4\n"
            elif node.init:
                node.init.accept(self)  # pre traversal watch out
                line += node.init.line

        if node.type == ast.TypeTypes.BOOL:
            if node.array:  # then it's gotta be just new
                if node.init:
                    numlines = node.init.index.value
                    line += f"MOVI {reg1}, #{0}\t;put local var array {node.ident} on stack\n"
                    for x in range(numlines):
                        line += f"STR {reg1}, SP\n"
                        line += f"ADI SP, #-4\n"
            elif node.init:
                node.init.accept(self)  # pre traversal watch out
                line += node.init.line

        if node.type == ast.TypeTypes.STRING:
            if node.array:  # then it's gotta be just new
                if node.init:
                    numlines = node.init.index.value
                    # put the current SP address at the label created earlier for this var
                    reg1 = self.regs.getReg(node)
                    line = f"MOV {reg1}, SP\n" \
                           f"STR {reg1}, {node.ident}\n"
                    line += f"MOVI {reg1}, #{0}\t;put local var array {node.ident} on stack\n"
                    for x in range(numlines):
                        line += f"STR {reg1}, SP\n"
                        line += f"ADI SP, #-4\n"
                    self.regs.freeReg(reg1)
            if node.init:
                node.init.accept(self)
                line += node.init.line

        super().visitVarDecl(node)

        if node.is_obj:
            if node.array:  # then it's gotta be just new
                if node.init:
                    numlines = node.init.index.value
                    # put the current SP address at the label created earlier for this var
                    line += f"MOVI {reg1}, #{0}\t;put local var array {node.ident} on stack\n"
                    for x in range(numlines):
                        line += f"STR {reg1}, SP\n"
                        line += f"ADI SP, #-4\n"
            elif node.init:
                line += node.init.line

        self.asmfile.write(line)
        self.regs.freeReg(reg1)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        if node.ident == "main":
            self.asmfile.write("main MOV R0, R0\n")
            self.in_main = True
            self.cur_classname = node.ident
        if node.member_type == ast.MemberTypes.CLASS:
            self.classnodes[node.ident] = node
            self.cur_classname = node.ident

        if node.member_type == ast.MemberTypes.DATAMEMBER:
            pass

        if node.member_type == ast.MemberTypes.METHOD \
                or node.member_type == ast.MemberTypes.CONSTRUCTOR:
            self.funcnodes[node.ident] = node
            self.cur_funcname = node.ident
            # gotta do the pre function things
            line = f"{node.ident}_{node.classtype} MOV R0, R0\n"
            self.asmfile.write(line)
            # just gonna set offset values for function's params here
            off = -12  # 4 for ret addr/val, 4 for PFP, 4 for addr to 'this' on heap
            if node.params:
                for n in node.params:
                    self.sym_table[node.classtype][node.ident][n.ident][2] = off
                    off -= 4

        super().visitMemberDecl(node)

        if node.member_type == ast.MemberTypes.METHOD \
                or node.member_type == ast.MemberTypes.CONSTRUCTOR:
            # gotta do the post function things
            if node.ret_type == ast.TypeTypes.VOID or node.member_type == ast.MemberTypes.CONSTRUCTOR:
                reg0 = self.regs.getReg(node)
                line = f"""
        LDR {reg0}, FP          ; load ret addr
        JMR {reg0}\n\n\n"""
                self.asmfile.write(line)
                self.regs.freeReg(reg0)

        if node.ident == "main":
            line = "TRP #0\n" \
                   "STACKOVERFLOW TRP #99\n" \
                   "TRP #0\n" \
                   "STACKUNDERFLOW TRP #99\n" \
                   "TRP #0\n"
            self.asmfile.write(line)

    def visitCase(self, node: ast.Case):
        self.asmfile.write(f"SWITCH{node.switch_count}case{node.ident} MOV R0, R0\n")
        super().visitCase(node)
        # self.asmfile.write(f"SWITCH{self.switch_count}case{node.ident}end MOV R0, R0\n")

    def mathExpr(self, node, op):
        line = ""
        reg1 = self.regs.getReg(node)
        reg2 = self.regs.getReg(node)
        math_expr = [ast.OpTypes.PLUS, ast.OpTypes.MINUS, ast.OpTypes.TIMES, ast.OpTypes.DIVIDE]
        # TODO add functionality for function return values and data members
        if node.left and node.left.line:
            if node.left.op_type == ast.OpTypes.ARGUMENTS:
                line += """\n; before frame make
            ADI SP, #-4          ; should be extra space for ret value to keep in this frame\n"""
            line += node.left.line
            if node.left.op_type == ast.OpTypes.ARGUMENTS:
                line += f"""
            ; after frame make
            MOV {reg1}, FP         ; put the ret of fib(x-1) on stack
            ADI {reg1}, #{4 * (-(len(node.left.args)) - 8)}   ;-12 because FP is ret addr, FP-4 is PFP, FP-8 is the int x param
            STR R3, {reg1}\n"""
        if node.right.line:
            line += node.right.line
        if self.in_main and node.left and node.left.op_type == ast.OpTypes.IDENTIFIER:
            line += f"LDR {reg1}, {node.left.value}\n" \
                    f"LDR {reg1}, {reg1}\n"
        elif not self.in_main and node.left and node.left.op_type == ast.OpTypes.IDENTIFIER \
                and node.left.classtype is False:
            line += f"LDR {reg1}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                    f"ADD {reg1}, FP\n" \
                    f"LDR {reg1}, {reg1}\n"
        elif not self.in_main and node.left and node.left.op_type == ast.OpTypes.IDENTIFIER \
                and node.left.classtype is True:
            offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][2]
            line += f"MOV {reg1}, FP\n" \
                    f"ADI {reg1}, #{offset}\n" \
                    f"LDR {reg1}, {reg1}\n"
        elif node.left and node.left.op_type == ast.OpTypes.NUM_LITERAL:
            line += f"MOVI {reg1}, #{node.left.value}\n"
        elif node.left and node.left.reg:
            if node.left.op_type == ast.OpTypes.ARGUMENTS:
                # line += f"MOV {reg1}, {node.left.reg}\n" \
                #         f"LDR {reg1}, {reg1}\n"
                line += f"""\nMOV {reg1}, FP
            ADI {reg1}, #{4 * (-(len(node.left.args)) - 8)}  ; the offset I put on earlier
            LDR {reg1}, {reg1}\n"""
            else:
                line += f"MOV {reg1}, {node.left.reg}\n"
            self.regs.freeReg(node.left.reg)
            node.left.reg = None
        else:
            line += f"MOVI {reg1}, #0\n"
        if self.in_main and node.right.op_type == ast.OpTypes.IDENTIFIER:
            line += f"LDR {reg2}, {node.right.value}\n" \
                    f"LDR {reg2}, {reg2}\n"
        elif not self.in_main and node.right.op_type == ast.OpTypes.IDENTIFIER and node.right.classtype is False:
            line += f"LDR {reg2}, {node.right.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                f"ADD {reg2}, FP\n" \
                f"LDR {reg2}, {reg2}\n"
        elif not self.in_main and node.right.op_type == ast.OpTypes.IDENTIFIER and node.right.classtype is True:
            offset = self.sym_table[self.cur_classname][self.cur_funcname][node.right.value][2]
            line += f"MOV {reg2}, FP\n" \
                    f"ADI {reg2}, #{offset}\n" \
                    f"LDR {reg2}, {reg2}\n"
        elif node.right.op_type == ast.OpTypes.NUM_LITERAL:
            line += f"MOVI {reg2}, #{node.right.value}\n"
        elif node.right.reg:
            if node.right.op_type == ast.OpTypes.ARGUMENTS:
                line += f"MOV {reg2}, {node.right.reg}\n"
            else:
                line += f"MOV {reg2}, {node.right.reg}\n"
            self.regs.freeReg(node.right.reg)
            node.right.reg = None

        line += f"{op} {reg1}, {reg2}\t;doing {op} with {node.left}, {node.right}\n"
        # line += f"TRP #99\n"
        self.regs.freeReg(reg2)
        # self.asmfile.write(line)
        node.line = line
        node.reg = reg1

    def ifCheckExpr(self, node, tORf):
        line = node.expr.line
        # ok so if it's a while or if, I want this to say this for the start, with a false
        if tORf == "false":
            line += f"BRZ {node.expr.reg}, IF{node.if_count}{tORf}\n"
        else:
            line += f"BGT {node.expr.reg}, IF{node.if_count}true\n"
        self.regs.freeReg(node.expr.reg)
        node.expr.reg = None
        self.asmfile.write(line)

    def cmpExprs(self, node, reg):
        def chooseLeftRight(nodeLR, reg):
            line = ""
            if self.in_main and nodeLR.op_type == ast.OpTypes.IDENTIFIER:
                line += f"LDR {reg}, {nodeLR.value}\n" \
                        f"LDR {reg}, {reg}\n"
            elif not self.in_main and nodeLR.op_type == ast.OpTypes.IDENTIFIER and nodeLR.classtype is False:
                if nodeLR.value not in self.sym_table[self.cur_classname][self.cur_funcname]:
                    # it's a data member, not local func var
                    line += f"MOV {reg}, FP\n" \
                            f"ADI {reg}, #-8\n" \
                            f"LDR {reg}, {reg}\n"
                    memlist = list(self.sym_table[nodeLR.left.type].keys())[1:]
                    off = memlist.index(nodeLR.right.value)
                    line += f"ADI {reg}, #{off * 4}\n" \
                            f"LDR {reg}, {reg}\n"  # at this point should finally have data member's value
                else:
                    line += f"LDR {reg}, {nodeLR.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                        f"ADD {reg}, FP\n" \
                        f"LDR {reg}, {reg}\n"
            elif not self.in_main and nodeLR.op_type == ast.OpTypes.IDENTIFIER and nodeLR.classtype is True:
                offset = self.sym_table[self.cur_classname][self.cur_funcname][nodeLR.value][2]
                line += f"MOV {reg}, FP\n" \
                        f"ADI {reg}, #{offset}\n" \
                        f"LDR {reg}, {reg}\n"
            if nodeLR.op_type == ast.OpTypes.NUM_LITERAL:
                line += f"MOVI {reg}, #{nodeLR.value}\n"
            elif nodeLR.op_type == ast.OpTypes.CHAR_LITERAL:
                if nodeLR.value == "' '":
                    line += f"MOVI {reg}, #32\n"
                else:
                    line += f"MOVI {reg}, {nodeLR.value}\n"

            elif nodeLR.reg is not None:
                line += nodeLR.line
                line += f"MOV {reg}, {nodeLR.reg}\n"
                self.regs.freeReg(nodeLR.reg)
                nodeLR.reg = None
            return line

        reg1 = reg
        reg2 = self.regs.getReg(node)
        line = chooseLeftRight(node.left, reg1)
        line += chooseLeftRight(node.right, reg2)
        line += f"CMP {reg1}, {reg2}\n"
        if node.op_type == ast.OpTypes.LESSTHAN:
            line += f"BLT {reg1}, less{self.less_count}\n" \
                    f"MOVI {reg1}, #0\n" \
                    f"JMP less{self.less_count}end\n" \
                    f"less{self.less_count} MOVI {reg1}, #1\n" \
                    f"less{self.less_count}end MOV R0, R0\n"
            self.less_count += 1
        elif node.op_type == ast.OpTypes.GREATERTHAN:
            line += f"BGT {reg1}, great{self.greater_count}\n" \
                    f"MOVI {reg1}, #0\n" \
                    f"JMP great{self.greater_count}end\n" \
                    f"great{self.greater_count} MOVI {reg1}, #1\n" \
                    f"great{self.greater_count}end MOV R0, R0\n"
            self.greater_count += 1
        elif node.op_type == ast.OpTypes.DOUBLEEQUALS:
            line += f"BRZ {reg1}, equal{self.equals_count}\n" \
                    f"MOVI {reg1}, #0\n" \
                    f"JMP equal{self.equals_count}end\n" \
                    f"equal{self.equals_count} MOVI {reg1}, #1\n" \
                    f"equal{self.equals_count}end MOV R0, R0\n"
            self.equals_count += 1
        self.regs.freeReg(reg2)
        # node.reg is already reg1
        node.line = line

    def cinout(self, node, param, c):
        if c == "cin":
            if self.in_main and node.expr.op_type == ast.OpTypes.IDENTIFIER \
                    and (node.expr.type == ast.TypeTypes.INT or node.expr.type == ast.TypeTypes.BOOL):
                reg1 = self.regs.getReg(node)
                line = f"TRP {param[0]}\n" \
                       f"LDR {reg1}, {node.expr.value}\n" \
                       f"STR R3, {reg1}\n"
                self.regs.freeReg(reg1)
            elif not self.in_main and node.expr.op_type == ast.OpTypes.IDENTIFIER and node.expr.classtype is False \
                    and (node.expr.type == ast.TypeTypes.INT or node.expr.type == ast.TypeTypes.BOOL):
                reg1 = self.regs.getReg(node)
                line = f"TRP {param[0]}\n" \
                       f"LDR {reg1}, {node.expr.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                       f"ADD {reg1}, FP\n" \
                       f"STR R3, {reg1}\n"
                self.regs.freeReg(reg1)
            elif not self.in_main and node.expr.op_type == ast.OpTypes.IDENTIFIER and node.expr.classtype is True \
                    and (node.expr.type == ast.TypeTypes.INT or node.expr.type == ast.TypeTypes.BOOL):
                offset = self.sym_table[self.cur_classname][self.cur_funcname][node.expr.value][2]
                reg1 = self.regs.getReg(node)
                line = f"TRP {param[0]}\n" \
                       f"MOV {reg1}, FP\n" \
                       f"ADI {reg1}, #{offset}\n" \
                       f"STR R3, {reg1}\n"
                self.regs.freeReg(reg1)
            elif self.in_main and node.expr.type == ast.TypeTypes.CHAR and node.expr.op_type == ast.OpTypes.IDENTIFIER:
                reg1 = self.regs.getReg(node)
                line = f"TRP {param[1]}\n" \
                       f"LDR {reg1}, {node.expr.value}\n" \
                       f"STB R3, {reg1}\n"
                self.regs.freeReg(reg1)
            elif not self.in_main and node.expr.op_type == ast.OpTypes.IDENTIFIER and node.expr.classtype is False \
                    and node.expr.type == ast.TypeTypes.CHAR:
                reg1 = self.regs.getReg(node)
                line = f"TRP {param[1]}\n" \
                       f"LDR {reg1}, {node.expr.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                       f"ADD {reg1}, FP\n" \
                       f"STB R3, {reg1}\n"
                self.regs.freeReg(reg1)
            elif not self.in_main and node.expr.op_type == ast.OpTypes.IDENTIFIER and node.expr.classtype is True \
                    and node.expr.type == ast.TypeTypes.CHAR:
                offset = self.sym_table[self.cur_classname][self.cur_funcname][node.expr.value][2]
                reg1 = self.regs.getReg(node)
                line = f"" \
                       f"TRP {param[0]}\n" \
                       f"MOV {reg1}, FP\n" \
                       f"ADI {reg1}, #{offset}\n" \
                       f"STB R3, {reg1}\n"
                self.regs.freeReg(reg1)
            else:
                # node.expr.accept(self)  # early traversal
                line = node.expr.line
                reg1 = node.expr.reg
                line += f"MOV R3, {reg1}\n"
                self.regs.freeReg(node.expr.reg)
                node.expr.reg = None
                line += f"TRP {param[0]}\n"

        if c == "cout":
            if self.in_main and node.expr.op_type == ast.OpTypes.IDENTIFIER \
                    and (node.expr.type == ast.TypeTypes.INT or node.expr.type == ast.TypeTypes.BOOL):
                line = f"LDR R3, {node.expr.value}\n" \
                       f"LDR R3, R3\n" \
                       f"TRP {param[0]}\n"
            elif not self.in_main and node.expr.op_type == ast.OpTypes.IDENTIFIER and node.expr.classtype is False \
                    and (node.expr.type == ast.TypeTypes.INT or node.expr.type == ast.TypeTypes.BOOL):
                line = f"LDR R3, {node.expr.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                       f"ADD R3, FP\n" \
                        f"LDR R3, R3\n" \
                       f"TRP {param[0]}\n"
            elif not self.in_main and node.expr.op_type == ast.OpTypes.IDENTIFIER and node.expr.classtype is True \
                    and (node.expr.type == ast.TypeTypes.INT or node.expr.type == ast.TypeTypes.BOOL):
                offset = self.sym_table[self.cur_classname][self.cur_funcname][node.expr.value][2]
                line = f"MOV R3, FP\n" \
                        f"ADI R3, #{offset}\n" \
                        f"LDR R3, R3\n" \
                       f"TRP {param[0]}\n"
            elif node.expr.type == ast.TypeTypes.INT and node.expr.op_type == ast.OpTypes.NUM_LITERAL:
                line = f"MOVI R3, #{node.expr.value}\n"
                line += f"TRP {param[0]}\n"
            elif node.expr.type == ast.TypeTypes.BOOL and node.expr.op_type == ast.OpTypes.TRUE:
                line = f"MOVI R3, #1\n"
                line += f"TRP {param[0]}\n"
            elif node.expr.type == ast.TypeTypes.BOOL and node.expr.op_type == ast.OpTypes.FALSE:
                line = f"MOVI R3, #0\n"
                line += f"TRP {param[0]}\n"

            elif self.in_main and node.expr.op_type == ast.OpTypes.IDENTIFIER \
                    and (node.expr.type == ast.TypeTypes.CHAR or node.expr.type == ast.TypeTypes.STRING):
                if node.expr.type == ast.TypeTypes.CHAR:
                    line = f"LDR R3, {node.expr.value}\n" \
                       f"LDR R3, R3\n" \
                       f"TRP {param[1]}\n"
                else:  # STRING
                    off = 0  # going down the heap
                    line = ""
                    strlen = self.sym_table["main"][node.expr.value][4]
                    # since this is just for nodes in main I can know where am in sym table
                    for x in range(strlen):  # I put a number in its is_array to say how long
                        line += f"LDR R3, {node.expr.value}\n" \
                           f"ADI R3, #{off}\n" \
                           f"LDR R3, R3\n" \
                           f"TRP {param[1]}\n"
                        off += 4
                    if strlen is False:  # the assembly loop, because above loop didn't work
                        reg1 = self.regs.getReg(node)
                        reg2 = self.regs.getReg(node)
                        line = f"MOVI {reg1}, #-4\n" \
                               f"printstr{self.print_count} LDR R3, {node.expr.value}\n" \
                               f"ADI {reg1}, #4\n" \
                               f"ADD R3, {reg1}\t;offsetting through heap\n" \
                               f"LDR R3, R3\n" \
                               f"MOV {reg2}, R3\n" \
                               f"CMPI {reg2}, '\"'\n" \
                               f"BRZ {reg2}, printstr{self.print_count}end\n" \
                               f"TRP {param[1]}\n" \
                               f"JMP printstr{self.print_count}\n" \
                               f"printstr{self.print_count}end MOV R0, R0\n"
                        self.print_count += 1
                        self.regs.freeReg(reg1)
                        self.regs.freeReg(reg2)
            elif not self.in_main and node.expr.op_type == ast.OpTypes.IDENTIFIER and node.expr.classtype is False \
                    and (node.expr.type == ast.TypeTypes.CHAR or node.expr.type == ast.TypeTypes.STRING):
                # for local function vars
                if node.expr.type == ast.TypeTypes.CHAR:
                        line = f"LDR R3, {node.expr.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                           f"ADD R3, FP\n" \
                           f"LDR R3, R3\n" \
                           f"TRP {param[1]}\n"
                else:  # STRING
                    off = 0  # going down the heap
                    line = ""
                    strlen = self.sym_table[self.cur_classname][self.cur_funcname][node.expr.value][4]
                    for x in range(strlen):
                        line += f"LDR R3, {node.expr.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                               f"ADI R3, #{off}\n" \
                               f"LDR R3, R3\n" \
                               f"TRP {param[1]}\n"
                        off += 4
            elif not self.in_main and node.expr.op_type == ast.OpTypes.IDENTIFIER and node.expr.classtype is True \
                    and (node.expr.type == ast.TypeTypes.CHAR or node.expr.type == ast.TypeTypes.STRING):
                # for parameter vars
                if node.expr.type == ast.TypeTypes.CHAR:
                    offset = self.sym_table[self.cur_classname][self.cur_funcname][node.expr.value][2]
                    line = f"MOV R3, FP\n" \
                       f"ADI R3, #{offset}\n" \
                       f"LDR R3, R3\n" \
                       f"TRP {param[1]}\n"
                else:  # STRING
                    offset = self.sym_table[self.cur_classname][self.cur_funcname][node.expr.value][2]
                    reg1 = self.regs.getReg(node)
                    reg2 = self.regs.getReg(node)
                    # so I decided to write a loop to go until it reads the terminating " I put in strs
                    line = f"MOVI {reg1}, #-4\n" \
                           f"printstr{self.print_count} MOV R3, FP\n" \
                           f"ADI R3, #{offset}\n" \
                           f"LDR R3, R3\t;getting the address to the heap\n" \
                           f"ADI {reg1}, #4\n" \
                           f"ADD R3, {reg1}\t;offsetting through heap\n" \
                           f"LDR R3, R3\n" \
                           f"MOV {reg2}, R3\n" \
                           f"CMPI {reg2}, '\"'\n" \
                           f"BRZ {reg2}, printstr{self.print_count}end\n" \
                           f"TRP {param[1]}\n" \
                           f"JMP printstr{self.print_count}\n" \
                           f"printstr{self.print_count}end MOV R0, R0\n"
                    self.print_count += 1
                    self.regs.freeReg(reg1)
                    self.regs.freeReg(reg2)
            elif node.expr.type == ast.TypeTypes.CHAR and node.expr.op_type == ast.OpTypes.CHAR_LITERAL:
                if node.expr.value == "' '":
                    line = f"MOVI R3, #32\n"
                    line += f"TRP #3\n"
                elif node.expr.value == r"'\n'":
                    line = f"MOVI R3, #10\n"
                    line += f"TRP #3\n"
                elif node.expr.value == r"'\t'":
                    line = f"MOVI R3, #9\n"
                    line += f"TRP #3\n"
                else:
                    line = f"MOVI R3, {node.expr.value}\n"
                    line += f"TRP {param[1]}\n"
            elif node.expr.op_type == ast.OpTypes.STRING_LITERAL:
                val: str = node.expr.value[1:-1]
                val = re.sub(r"\\n", '\n', val)
                val = re.sub(r"\\t", '\t', val)
                line = ""
                for c in val:  # maybe should exclude the "'s
                    if c == " ":
                        line += f"MOVI R3, #32\n"
                    elif c == '\n':
                        line += f"MOVI R3, #10\n"
                    elif c == '\t':
                        line += f"MOVI R3, #9\n"
                    else:
                        line += f"MOVI R3, '{c}'\n"
                    line += f"TRP #3\n"
            else:
                # node.expr.accept(self)  # early traversal could probably avoid
                line = node.expr.line
                reg1 = node.expr.reg
                if node.expr.op_type == ast.OpTypes.ARGUMENTS and node.expr.left.right.type == ast.TypeTypes.STRING:
                    # node.expr.left.right.type  # just looks awful
                    # gotta dereference, func calls that return strings just return their addr
                    reg3 = self.regs.getReg(node)
                    line += f"LDR {reg1}, {reg1}\n" \
                            f"MOV R3, {reg1}\n" \
                            f"MOV {reg3}, {reg1}\n"
                    # line += f"LDR {reg1}, {reg1}\n"  # turns out gotta dereference twice? gonna do later
                    reg2 = self.regs.getReg(node)
                    line += f"MOVI {reg1}, #-4\n" \
                           f"printstr{self.print_count} MOV R3, {reg3}\n" \
                            f"ADI {reg1}, #4\n" \
                           f"ADD R3, {reg1}\t;offsetting through heap\n" \
                           f"LDR R3, R3\n" \
                           f"MOV {reg2}, R3\n" \
                           f"CMPI {reg2}, '\"'\n" \
                           f"BRZ {reg2}, printstr{self.print_count}end\n" \
                           f"TRP {param[1]}\n" \
                           f"JMP printstr{self.print_count}\n" \
                           f"printstr{self.print_count}end MOV R0, R0\n"
                    self.print_count += 1
                    self.regs.freeReg(node.expr.reg)
                    node.expr.reg = None
                    self.regs.freeReg(reg2)
                    self.regs.freeReg(reg3)
                else:
                    line += f"MOV R3, {reg1}\n"
                    self.regs.freeReg(node.expr.reg)
                    node.expr.reg = None
                    if node.expr.op_type == ast.OpTypes.PERIOD and node.expr.right.type == ast.TypeTypes.CHAR:
                        line += f"TRP {param[1]}\n"
                    else:
                        line += f"TRP {param[0]}\n"

        self.asmfile.write(line)

    def andOr(self, node, op):
        line = ""
        reg1 = self.regs.getReg(node)
        reg2 = self.regs.getReg(node)
        if node.left.line:
            line += node.left.line
        if node.right.line:
            line += node.right.line

        if self.in_main and node.left.op_type == ast.OpTypes.IDENTIFIER:
            line += f"LDR {reg1}, {node.left.value}\n" \
                    f"LDR {reg1}, {reg1}\n"
        elif not self.in_main and node.left.op_type == ast.OpTypes.IDENTIFIER and node.left.classtype is False:
            if node.left.value not in self.sym_table[self.cur_classname][self.cur_funcname]:
                # it's a data member, not local func var
                line += f"MOV {reg1}, FP\n" \
                        f"ADI {reg1}, #-8\n" \
                        f"LDR {reg1}, {reg1}\n"
                memlist = list(self.sym_table[node.left.left.type].keys())[1:]
                off = memlist.index(node.left.right.value)
                line += f"ADI {reg1}, #{off * 4}\n" \
                        f"LDR {reg1}, {reg1}\n"  # at this point should finally have data member's value
            else:
                line += f"LDR {reg1}, {node.left.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                    f"ADD {reg1}, FP\n" \
                    f"LDR {reg1}, {reg1}\n"
        elif not self.in_main and node.left.op_type == ast.OpTypes.IDENTIFIER and node.left.classtype is True:
            offset = self.sym_table[self.cur_classname][self.cur_funcname][node.left.value][2]
            line += f"MOV {reg1}, FP\n" \
                    f"ADI {reg1}, #{offset}\n" \
                    f"LDR {reg1}, {reg1}\n"
        elif node.left.op_type == ast.OpTypes.TRUE:
            line += f"MOVI {reg1}, #1\n"
        elif node.left.op_type == ast.OpTypes.FALSE:
            line += f"MOVI {reg1}, #0\n"
        elif node.left.reg:
            line += f"MOV {reg1}, {node.left.reg}\n"
            self.regs.freeReg(node.left.reg)
            node.left.reg = None
        if self.in_main and node.right.op_type == ast.OpTypes.IDENTIFIER:
            line += f"LDR {reg2}, {node.right.value}\n" \
                    f"LDR {reg2}, {reg2}\n"
        elif not self.in_main and node.right.op_type == ast.OpTypes.IDENTIFIER and node.right.classtype is False:
            if node.left.value not in self.sym_table[self.cur_classname][self.cur_funcname]:
                # it's a data member, not local func var
                line += f"MOV {reg2}, FP\n" \
                        f"ADI {reg2}, #-8\n" \
                        f"LDR {reg2}, {reg2}\n"
                memlist = list(self.sym_table[node.left.left.type].keys())[1:]
                off = memlist.index(node.left.right.value)
                line += f"ADI {reg2}, #{off * 4}\n" \
                        f"LDR {reg2}, {reg2}\n"  # at this point should finally have data member's value
            else:
                line += f"LDR {reg2}, {node.right.value}_{self.cur_classname}_{self.cur_funcname}\n" \
                    f"ADD {reg2}, FP\n" \
                    f"LDR {reg2}, {reg2}\n"
        elif not self.in_main and node.right.op_type == ast.OpTypes.IDENTIFIER and node.right.classtype is True:
            offset = self.sym_table[self.cur_classname][self.cur_funcname][node.right.value][2]
            line += f"MOV {reg2}, FP\n" \
                    f"ADI {reg2}, #{offset}\n" \
                    f"LDR {reg2}, {reg2}\n"
        elif node.right.op_type == ast.OpTypes.TRUE:
            line += f"MOVI {reg2}, #1\n"
        elif node.right.op_type == ast.OpTypes.FALSE:
            line += f"MOVI {reg2}, #0\n"
        elif node.right.reg:
            line += f"MOV {reg2}, {node.right.reg}\n"
            self.regs.freeReg(node.right.reg)
            node.right.reg = None

        line += f"{op} {reg1}, {reg2}\t;{op}ing {node.left.value}, {node.right.value}\n"
        self.regs.freeReg(reg2)
        node.reg = reg1
        node.line = line


class CloseFileVisitor(sv.Visitor):
    def __init__(self, asmfile):
        self.asmfile = asmfile
        asmfile.close()


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
