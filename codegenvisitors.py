import astclasses as ast
import semanticvisitors as sv


class RegManager:
    def __init__(self):
        # not R3 in regs, that's for TRP
        self.regs = ["R0", "R1", "R2", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11",
                     "R12", "R13", "R14", "R15", ]
        self.given_regs = []

        """
        using stack heavy instead of registers could work well, 
        pushing things onto stack and working off of it, use less registers
        desugaring things means less assembly and codegen visitors 
        tons of stuff can be desugared and that would be great
        """

    def getReg(self):
        try:
            reg = self.regs.pop()
            self.given_regs.append(reg)
            # print("get", reg, self.__class__)
            return reg
        except:
            print("TODO no free regs")  # TODO

    def freeReg(self, reg):
        try:
            self.given_regs.remove(reg)
            # print("free", reg, self.__class__)
            self.regs.append(reg)
        except:
            print("tried to free an already free reg")


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
            node.substatement.insert(0, iftrue)
            # ok maybe just putting this in the substatement list will do, to help generate code
            iffalse = ast.Statement(ast.StatementTypes.IF_FALSE)
            iffalse.is_while = node.is_while
            iffalse.expr = node.expr
            node.substatement.append(iffalse)

        if node.statement_type == ast.StatementTypes.SWITCH:
            endcase = ast.Statement(ast.StatementTypes.END_CASE)
            node.case_list.append(endcase)
        super().visitStmnt(node)


class AddThisVisitor(sv.Visitor):
    def __init__(self):
        pass

    def visitExpr(self, node: ast.Expression):
        # I gotta make it so that there can be local variable with same name as attribute in method
        # and if that is case then without the "this" it should default to the local one
        super().visitExpr(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        super().visitMemberDecl(node)


class VarsAndMembers(sv.Visitor):
    def __init__(self, sym_table, filename="a.asm"):
        self.regs = RegManager()
        self.asmfile = open(filename, "w+")
        self.in_main = False
        self.sym_table = sym_table
        self.memberlines = {}
        self.primtypes = [ast.TypeTypes.BOOL, ast.TypeTypes.INT, ast.TypeTypes.CHAR,]  # string? idk

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
            if node.type == ast.TypeTypes.STRING:  # IDK if I wanna put strings on the stack
                if node.init:
                    line = f"{node.ident}"
                    for c in node.init.value[1:]:
                        line += f" .BYT '{c}'\n"
                else:
                    line = ""
                self.asmfile.write(line)
            if node.is_obj:
                # give it all of it's fields
                # if node.init:
                #     fields = [x for x in self.sym_table[node.type].items()]  # gives the names of attrs and methods
                #     line = f"{node.ident}_{node.type} .INT\n"  # have its label be its ident and type
                #     for f in fields:
                #         if isinstance(f[1], list):  # is attr
                #             # what if I made a "line" for every member decl and when I get an object
                #             # I just get the line for its init
                #             # f is list of tuple for every decl the class has
                #             # ex: [(attr, [int, etc etc]), (method, {method stuff})]
                #             # if f[1][0] == ast.TypeTypes.INT:
                #             line += f"{f[0]}_{node.ident}"
                #             line += self.memberlines[node.type][f[0]]
                #         elif isinstance(f[1], dict):  # is method
                #             pass

                # actually I'm just gonna put an int and have it get assigned to the heap addr when it gets to that
                line = f"{node.ident} .INT \n"
                self.asmfile.write(line)

        super().visitVarDecl(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        if node.ident == "main":
            # self.asmfile.write(f"main MOV R0, R0")
            self.in_main = True

        # one idea I had here was to make a self.memberlines dict,
        # it would be like the sym table but it would have init values in it (get it?)

        super().visitMemberDecl(node)


class CodeGen(sv.Visitor):
    def __init__(self, asmfile):
        self.asmfile = asmfile
        self.regs = RegManager()
        self.expr_reg_result = None
        self.if_count = 0
        self.switch_count = 0
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
            if (node.left.type == ast.TypeTypes.INT or node.left.type == ast.TypeTypes.BOOL) \
                    and node.left.op_type == ast.OpTypes.IDENTIFIER \
                    and node.right.reg is not None:
                # this SHOULD cover like if the right is everything except just a num lit
                reg1 = self.regs.getReg()
                line += node.right.line
                line += f"LDR {reg1}, {node.left.value}\n"  # get the address
                line += f"STR {node.right.reg}, {reg1}\n"  # put data at address
                self.regs.freeReg(node.right.reg)
                node.right.reg = None
                self.regs.freeReg(reg1)
            elif node.left.type == ast.TypeTypes.INT and node.left.op_type == ast.OpTypes.IDENTIFIER \
                    and node.right.reg is None:
                # could be an int literal, could be dot with class attr, could be args with a dot and method
                # maybe
                if node.right.op_type == ast.OpTypes.NUM_LITERAL:
                    reg1 = self.regs.getReg()
                    reg2 = self.regs.getReg()
                    line += f"MOVI {reg1}, #{node.right.value}\n" \
                            f"LDR {reg2}, {node.left.value}\n" \
                            f"STR {reg1}, {reg2}\n"
                    self.regs.freeReg(reg1)
                    self.regs.freeReg(reg2)
                if node.right.op_type == ast.OpTypes.PERIOD:
                    # value = self.sym_table[node.right.left][node.right.right]
                    # node.right.left is an object in scope that has a data member
                    # so I gotta go to that object and get its data member's value
                    # TODO do that above stuff
                    # TODO or maybe just make it so the . will make it's own line to get the info
                    # if it's datamember, not func
                    pass
            elif node.left.type == ast.TypeTypes.BOOL and node.right.reg is None:
                if node.right.op_type == ast.OpTypes.TRUE:
                    line += f"MOVI \n"  # TODO something missing here obvioiusly

            node.line = line

        if node.op_type == ast.OpTypes.DOUBLEEQUALS:
            self.cmpExprs(node)

        if node.op_type == ast.OpTypes.LESSTHAN:
            # currently, should make these not write to file, but write to their node.line
            # also IDK but these are probably just the same as the == but maybe they only do int?
            self.cmpExprs(node)

        if node.op_type == ast.OpTypes.GREATERTHAN:
            # currently, should make these not write to file, but write to their node.line
            # also IDK but these are probably just the same as the == but maybe they only do int?
            self.cmpExprs(node)

        if node.op_type == ast.OpTypes.AND:
            # currently, should make these not write to file, but write to their node.line
            line = ""
            if node.left.line:
                line += node.left.line
            if node.right.line:
                line += node.right.line
            if node.left.op_type == ast.OpTypes.IDENTIFIER:
                line += f"LDR {reg1}, {node.left.value}\n" \
                        f"LDR {reg1}, {reg1}\n"
            elif node.left.op_type == ast.OpTypes.NUM_LITERAL:
                line += f"MOVI {reg1}, #{node.left.value}\n"
            elif node.left.reg:
                line += f"MOV {reg1}, {node.left.reg}\n"
                self.regs.freeReg(node.left.reg)
                node.left.reg = None
            if node.right.op_type == ast.OpTypes.IDENTIFIER:
                line += f"LDR {reg2}, {node.right.value}\n" \
                        f"LDR {reg2}, {reg2}\n"
            elif node.right.op_type == ast.OpTypes.NUM_LITERAL:
                line += f"MOVI {reg2}, #{node.right.value}\n"
            elif node.right.reg:
                line += f"MOV {reg2}, {node.right.reg}\n"
                self.regs.freeReg(node.right.reg)
                node.right.reg = None

        if node.op_type == ast.OpTypes.OR:
            pass  # currently, should make these not write to file, but write to their node.line

        if node.op_type == ast.OpTypes.EXCLAMATIONMARK:
            # currently, should make these not write to file, but write to their node.line
            # self.returns_bool = [ast.OpTypes.DOUBLEEQUALS, ast.OpTypes.LESSTHAN,
            #     ast.OpTypes.GREATERTHAN, ast.OpTypes.AND, ast.OpTypes.OR,]
            if node.right.op_type in self.returns_bool:
                line = node.right.line
                if node.right.op_type == ast.OpTypes.DOUBLEEQUALS:
                    # ok funny story, but like if you do 5 == 5 then in the reg you'll have 0, false!
                    pass  # so just pass idk, because it's like already logically not'ed

                else:
                    line += f"NOT {node.right.reg}\n"
                node.reg = node.right.reg
                node.right.reg = None  # don't free it, just take it for later
                node.line = line

        if node.op_type == ast.OpTypes.TRUE:
            pass
        if node.op_type == ast.OpTypes.FALSE:
            pass
        if node.op_type == ast.OpTypes.NULL:
            pass
        if node.op_type == ast.OpTypes.NEW:
            pass
        if node.op_type == ast.OpTypes.THIS:
            pass  # currently, should make these not write to file, but write to their node.line
        if node.op_type == ast.OpTypes.PERIOD:
            pass  # currently, should make these not write to file, but write to their node.line
        if node.op_type == ast.OpTypes.INDEX:
            pass  # currently, should make these not write to file, but write to their node.line
        if node.op_type == ast.OpTypes.ARGUMENTS:
            pass  # currently, should make these not write to file, but write to their node.line
        # super().visitExpr(node)

    def visitStmnt(self, node: ast.Statement):
        if node.statement_type == ast.StatementTypes.IF:
            line = f"IF{self.if_count}start MOV R0, R0\n"
            self.asmfile.write(line)
            node.expr.accept(self)  # this will cause an extra node visit... worth?
            self.ifCheckExpr(node, "false")

        if node.statement_type == ast.StatementTypes.RETURN:
            pass

        if node.statement_type == ast.StatementTypes.COUT:
            self.cinout(node, ("#1", "#3"))

        if node.statement_type == ast.StatementTypes.CIN:
            self.cinout(node, ("#2", "#4"))

        if node.statement_type == ast.StatementTypes.SWITCH:
            line = f"SWITCH{self.switch_count}start MOV R0, R0\n"

            def hashtagOrNot(notnode, hashtag):
                # write comparisons for each case's "ident"
                reg1 = self.regs.getReg()
                switchval = notnode.expr.value
                notline = ""
                for c in notnode.case_list:
                    if isinstance(c, ast.Case):
                        notline += f"MOVI {reg1}, {hashtag}{switchval}\n" \
                           f"CMPI {reg1}, {hashtag}{c.ident}\n" \
                           f"BRZ {reg1}, SWITCH{self.switch_count}case{c.ident}\n"
                self.regs.freeReg(reg1)
                notline += f"JMP DEFAULT{self.switch_count}start\n"
                return notline

            if node.expr.op_type == ast.OpTypes.NUM_LITERAL:
                line += hashtagOrNot(node, "#")
            elif node.expr.op_type == ast.OpTypes.CHAR_LITERAL:
                line += hashtagOrNot(node, "")
            self.asmfile.write(line)
        if node.statement_type == ast.StatementTypes.END_CASE:
            self.asmfile.write(f"DEFAULT{self.switch_count}start MOV R0, R0\n")

        if node.statement_type == ast.StatementTypes.BREAK:
            pass

        if node.statement_type == ast.StatementTypes.IF_TRUE:
            line = f"IF{self.if_count}true MOV R0 R0\n"
            self.asmfile.write(line)

        if node.statement_type == ast.StatementTypes.IF_FALSE:
            # write if-true's ending stuff
            line = ""
            if node.is_while:
                self.ifCheckExpr(node, "true")
            else:
                line += f"JMP IF{self.if_count}end\n"
                self.regs.freeReg(node.expr.reg)  # weird I have to free it here, the tree is deceiving
            # write if-false's beginning stuff
            line += f"IF{self.if_count}false MOV R0 R0\n"
            self.asmfile.write(line)

        super().visitStmnt(node)

        if node.statement_type == ast.StatementTypes.BRACES:
            pass

        if node.statement_type == ast.StatementTypes.EXPRESSION:
            self.asmfile.write(node.expr.line)

        if node.statement_type == ast.StatementTypes.IF:
            # now we are below the super() call
            line = f"IF{self.if_count}end MOV R0, R0\n"
            self.asmfile.write(line)
            self.if_count += 1

        if node.statement_type == ast.StatementTypes.RETURN:
            pass

        if node.statement_type == ast.StatementTypes.SWITCH:
            self.asmfile.write(f"SWITCH{self.switch_count}end MOV R0, R0\n")
            self.switch_count += 1

        if node.statement_type == ast.StatementTypes.BREAK:
            pass

    def visitVarDecl(self, node: ast.VariableDeclaration):
        """ok so the variables gotta go on the stack, so in main, I guess not use FP much,
        SP always points to top open space on stack. so put the variable there and increment by fours
        probably no matter the var just always give four bytes
        """
        if node.type == ast.TypeTypes.INT:
            line = ""

            if node.array:  # then it's gotta be just new
                if node.init:
                    numlines = node.init.index.value
                    # put the current SP address at the label created earlier for this var
                    reg1 = self.regs.getReg()
                    line = f"MOV {reg1}, SP\n" \
                           f"STR {reg1}, {node.ident}\n"
                    line += f"MOVI {reg1}, #{0}\t;put local var {node.ident} on stack\n"
                    for x in range(numlines):
                        line += f"STR {reg1}, SP\n"
                        line += f"ADI SP, #-4\n"
                    self.regs.freeReg(reg1)
            elif node.init.op_type in self.math_ops:
                reg1 = self.regs.getReg()
                node.init.reg = None
                line += f"MOV {reg1}, SP\n" \
                        f"STR {reg1}, {node.ident}\n"
                self.regs.freeReg(reg1)
                node.init.accept(self)  # doing manual visiting again...
                line += node.init.line
                line += f"STR {node.init.reg}, SP\n" \
                        f"ADI SP, #-4\n"
                self.regs.freeReg(node.init.reg)
                node.init.reg = None
            elif node.init.op_type == ast.OpTypes.NUM_LITERAL:
                reg1 = self.regs.getReg()
                line = f"MOV {reg1}, SP\n" \
                       f"STR {reg1}, {node.ident}\n" \
                       f"MOVI {reg1}, #{node.init.value}\n" \
                       f"STR {reg1}, SP\n" \
                       f"ADI SP, #-4\n"
                self.regs.freeReg(reg1)
            elif node.init.op_type == ast.OpTypes.PERIOD:
                reg1 = self.regs.getReg()
                line = f"MOV {reg1}, SP\n" \
                       f"STR {reg1}, {node.ident}\n" \
                       f"gotta get node.init.right (a datamember) into reg1" \
                       f"STR {reg1}, SP\n" \
                       f"ADI SP, #-4\n"
                self.regs.freeReg(reg1)
            self.asmfile.write(line)

        if node.type == ast.TypeTypes.CHAR:
            # if not node.array:
            #     line = f"{node.ident} .BYT "
            #     if node.init:
            #         line += f"{node.init.value}\n"
            #     self.asmfile.write(line)
            # else:
            #     line = f"{node.ident} .BYT\n"
            #     if node.init:  # should be a new
            #         numlines = node.init.index.value - 1  # - 1 for the first line already made
            #         for x in range(numlines):
            #             line += f" .BYT \n"

            # self.asmfile.write(line)
            pass
            # self.asmfile.write(line)

        if node.type == ast.TypeTypes.BOOL:
            # line = f"{node.ident} .INT "
            # if node.init:
            #     self.boolInit(node)
            # else:
            #     line += "\n"
            pass
            # self.asmfile.write(line)

        if node.type == ast.TypeTypes.STRING:
            # if node.init:
            #     line = f"{node.ident}"
            #     for c in node.init.value[1:]:
            #         line += f" .BYT '{c}'\n"
            # else:
            #     line = ""
            pass
            # self.asmfile.write(line)

        if node.is_obj:  # because I have node.type as the class ident if it's an object
            # give it all of it's fields
            # if node.init:
            #     fields = [x for x in self.sym_table[node.type].items()]  # gives the names of attrs and methods
            #     line = f"{node.ident}_{node.type} .INT\n"  # have its label be its ident and type
            #     for f in fields:
            #         if isinstance(f[1], list):  # is attr
            #             # what if I made a "line" for every member decl and when I get an object
            #             # I just get the line for its init
            #             # f is list of tuple for every decl the class has
            #             # ex: [(attr, [int, etc etc]), (method, {method stuff})]
            #             # if f[1][0] == ast.TypeTypes.INT:
            #             line += f"{f[0]}_{node.ident}"
            #             line += self.memberlines[node.type][f[0]]
            #         elif isinstance(f[1], dict):  # is method
            #             pass
            pass
            # self.asmfile.write(line)

        super().visitVarDecl(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        super().visitMemberDecl(node)
        if node.ident == "main":
            self.asmfile.write("TRP #0\n")

    def visitCase(self, node: ast.Case):
        self.asmfile.write(f"SWITCH{self.switch_count}case{node.ident} MOV R0, R0\n")
        super().visitCase(node)
        # self.asmfile.write(f"SWITCH{self.switch_count}case{node.ident}end MOV R0, R0\n")

    def mathExpr(self, node, op):
        line = ""
        reg1 = self.regs.getReg()
        reg2 = self.regs.getReg()
        math_expr = [ast.OpTypes.PLUS, ast.OpTypes.MINUS, ast.OpTypes.TIMES, ast.OpTypes.DIVIDE]
        # TODO add functionality for function return values and data members
        if node.left.line:
            line += node.left.line
        if node.right.line:
            line += node.right.line
        if node.left.op_type == ast.OpTypes.IDENTIFIER:
            line += f"LDR {reg1}, {node.left.value}\n" \
                    f"LDR {reg1}, {reg1}\n"
        elif node.left.op_type == ast.OpTypes.NUM_LITERAL:
            line += f"MOVI {reg1}, #{node.left.value}\n"
        elif node.left.reg:
            line += f"MOV {reg1}, {node.left.reg}\n"
            self.regs.freeReg(node.left.reg)
            node.left.reg = None
        if node.right.op_type == ast.OpTypes.IDENTIFIER:
            line += f"LDR {reg2}, {node.right.value}\n" \
                    f"LDR {reg2}, {reg2}\n"
        elif node.right.op_type == ast.OpTypes.NUM_LITERAL:
            line += f"MOVI {reg2}, #{node.right.value}\n"
        elif node.right.reg:
            line += f"MOV {reg2}, {node.right.reg}\n"
            self.regs.freeReg(node.right.reg)
            node.right.reg = None
        line += f"{op} {reg1}, {reg2}\t;doing {op} with {node.left.value}, {node.right.value}\n"
        # line += f"TRP #99\n"
        self.regs.freeReg(reg2)
        # self.asmfile.write(line)
        node.line = line
        node.reg = reg1

    def ifCheckExpr(self, node, tORf):
        line = node.expr.line
        if node.expr.op_type == ast.OpTypes.DOUBLEEQUALS:
            line += f"BNZ {node.expr.reg}, IF{self.if_count}{tORf}\n"  # if it's false, gonna branch to the false
            self.regs.freeReg(node.expr.reg)
            node.expr.reg = None
        if node.expr == ast.OpTypes.EXCLAMATIONMARK:
            pass
        # TODO add all the things that could be an if expr
        self.asmfile.write(line)  # I forgot that doing this func won't actually modify line outside of this

    def cmpExprs(self, node, ):
        def chooseLeftRight(nodeLR, reg):
            line = ""
            if nodeLR.op_type == ast.OpTypes.IDENTIFIER:
                line += f"LDR {reg}, {nodeLR.value}\n" \
                        f"LDR {reg}, {reg}\n"
            elif nodeLR.op_type == ast.OpTypes.NUM_LITERAL:
                line += f"MOVI {reg}, #{nodeLR.value}\n"
            elif nodeLR.op_type == ast.OpTypes.CHAR_LITERAL:
                line += f"MOVI {reg}, {nodeLR.value}\n"
            # no comparing strings I don't think
            # TODO nodes could be like any expression I think...
            # I think if the nodes are index, args (with dot), or dot then they will get accessed in those expr
            # instead of accessing them here and everywhere else they could be used
            return line

        reg1 = self.regs.getReg()
        reg2 = self.regs.getReg()
        line = chooseLeftRight(node.left, reg1)
        line += chooseLeftRight(node.right, reg2)
        line += f"CMP {reg1}, {reg2}\n"
        node.reg = reg1
        self.regs.freeReg(reg2)
        # self.asmfile.write(line)
        node.line = line

    def cinout(self, node, param):
        if node.expr.type == ast.TypeTypes.INT and node.expr.op_type == ast.OpTypes.IDENTIFIER:
            line = f"LDR R3, {node.expr.value}\n" \
                   f"LDR R3, R3\n" \
                   f"TRP {param[0]}\n"
        elif node.expr.type == ast.TypeTypes.INT and node.expr.op_type == ast.OpTypes.NUM_LITERAL:
            line = f"MOVI R3, #{node.expr.value}\n"
            line += f"TRP {param[0]}\n"
        elif node.expr.type == ast.TypeTypes.CHAR and node.expr.op_type == ast.OpTypes.IDENTIFIER:
            line = f"LDR R3, {node.expr.value}\n" \
                   f"LDR R3, R3\n" \
                   f"TRP {param[1]}\n"
        elif node.expr.type == ast.TypeTypes.CHAR and node.expr.op_type == ast.OpTypes.CHAR_LITERAL:
            line = f"MOVI R3, {node.expr.value}\n"
            line += f"TRP {param[1]}\n"
        else:  # TODO I guess node.expr is a very variety of possibilities
            node.expr.accept(self)  # early traversal
            line = node.expr.line
            reg1 = node.expr.reg
            line += f"MOV R3, {reg1}\n"
            self.regs.freeReg(node.expr.reg)
            node.expr.reg = None
            line += f"TRP {param[0]}\n"
        self.asmfile.write(line)


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
