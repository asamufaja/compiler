import astclasses as ast
import pydot


class Visitor:
    def __init__(self):
        self.sym_table = None

    def visitExpr(self, node: ast.Expression):
        if node.left is not None:
            node.left.accept(self)
        if node.right is not None:
            node.right.accept(self)
        if node.index is not None:
            node.index.accept(self)
        if node.args is not None and not isinstance(node.args, str):  # funny situation adding this
            for arg in node.args:
                arg.accept(self)

    def visitStmnt(self, node: ast.Statement):
        if node.statement_type == ast.StatementTypes.BRACES:
            for stmnt in node.substatement:
                stmnt.accept(self)
        if node.statement_type == ast.StatementTypes.IF:
            node.expr.accept(self)
            for stmnt in node.substatement:
                stmnt.accept(self)
            if node.else_statement is not None \
                    and node.else_statement.statement_type == ast.StatementTypes.BRACES:
                for stmnt in node.else_statement.substatement:
                    stmnt.accept(self)
            elif node.else_statement is not None:
                node.else_statement.accept(self)
        if node.statement_type == ast.StatementTypes.WHILE:
            node.expr.accept(self)
            for stmnt in node.substatement:
                stmnt.accept(self)
        if node.statement_type == ast.StatementTypes.RETURN \
                or node.statement_type == ast.StatementTypes.COUT \
                or node.statement_type == ast.StatementTypes.CIN \
                or node.statement_type == ast.StatementTypes.EXPRESSION:
            if node.expr is not None:
                node.expr.accept(self)
        if node.statement_type == ast.StatementTypes.SWITCH:
            node.expr.accept(self)
            for casenode in node.case_list:
                casenode.accept(self)
            for stmnt in node.default_stmnts:
                stmnt.accept(self)
        # if node.statement_type == ast.StatementTypes.BREAK:
        #     pass
        # if node.statement_type == ast.StatementTypes.VAR_DECL:
        #     pass

    def visitVarDecl(self, node: ast.VariableDeclaration):
        if node.init is not None:
            node.init.accept(self)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        if node.params is not None:
            for p in node.params:
                p.accept(self)
        if node.body is not None:
            for stmnt in node.body:
                stmnt.accept(self)
        if node.class_members is not None:
            for decl in node.class_members:
                decl.accept(self)
        if node.init is not None:
            node.init.accept(self)
        if node.child is not None:  # the only place I use child for this node type is comp unit
            node.child.accept(self)

    def visitCase(self, node: ast.Case):
        if node.statements is not None:
            for stmnt in node.statements:
                stmnt.accept(self)

    def isInSym(self, x):
        if x in self.sym_table:
            return True, self.sym_table[x]
        for k, v in self.sym_table.items():
            if isinstance(v, dict):
                if x in v:
                    return True, v[x]
                for k1, v1 in v.items():
                    if isinstance(v1, dict):
                        if x in v1:
                            return True, v1[x]
        return False, None


class PrintAST(Visitor):
    def __init__(self):
        self.indentLevel = 0
        self.tab = "  "
        self.graph = pydot.Dot("ast", graph_type="graph")
        self.numExprs = 0
        self.numStmnts = 0
        self.numClassDecls = 0
        self.numVars = 0

    def visitExpr(self, node: ast.Expression):
        # print(f"{self.tab * self.indentLevel}{node.op_type}, type:{node.type}, value:{node.value}")
        if node.left is not None:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{node.left}"))
        if node.right is not None:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{node.right}"))
        if node.index is not None:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{node.index}"))
        if node.args is not None:
            for n in node.args:
                self.graph.add_edge(pydot.Edge(f"{node}", f"{n}"))
        super().visitExpr(node)

    def visitStmnt(self, node: ast.Statement):
        # print(f"{self.tab * self.indentLevel}{node.statement_type}")

        if node.expr is not None:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{node.expr}"))
        for n in node.substatement:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{n}"))

        if node.else_statement is not None \
                and node.else_statement.statement_type == ast.StatementTypes.BRACES:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{node.else_statement}"))
            for stmnt in node.else_statement.substatement:
                self.graph.add_edge(pydot.Edge(f"{node.else_statement}", f"{stmnt}"))
        elif node.else_statement is not None:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{node.else_statement}"))

        for n in node.case_list:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{n}"))
        for n in node.default_stmnts:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{n}"))

        self.indentLevel += 1
        super().visitStmnt(node)
        self.indentLevel -= 1

    def visitVarDecl(self, node: ast.VariableDeclaration):
        # print(f"{self.tab * self.indentLevel}{node.type}, {node.ident}")
        if node.init is not None:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{node.init}"))
        super().visitVarDecl(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        # print(f"{self.tab * self.indentLevel}{node.modifier}, {node.ret_type}, {node.ident}")

        if node.params is not None:
            for n in node.params:
                self.graph.add_edge(pydot.Edge(f"{node}", f"{n}"))
        for n in node.body:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{n}"))
        for n in node.class_members:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{n}"))
        if node.init is not None:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{node.init}"))
        if node.child is not None:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{node.child}"))

        if node.ret_type == ast.TypeTypes.CLASS \
                and node.body is not None:
            self.indentLevel += 1
        super().visitMemberDecl(node)
        if node.ret_type == ast.TypeTypes.CLASS \
                and node.body is not None:
            self.indentLevel -= 1

    def visitCase(self, node: ast.Case):
        if node.statements is not None:
            for n in node.statements:
                self.graph.add_edge(pydot.Edge(f"{node}", f"{n}"))
        super().visitCase(node)

    def makeTree(self):
        self.graph.write("output.png", format="png")


class PreSymbolTableVisitor(Visitor):
    def __init__(self, sym_table):
        # visitor to put classes and methods in the sym table to be semi-hoisted
        self.sym_table = sym_table
        self.isErrorState = False
        self.error_messages = []
        self.cur_method: ast.ClassAndMemberDeclaration = None
        self.cur_class: ast.ClassAndMemberDeclaration = None

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        if not self.isDuplicate(node):
            if node.member_type == ast.MemberTypes.CLASS:
                self.cur_class = node
                self.sym_table[self.cur_class.ident] = {}
                self.cur_method = None
            if node.member_type == ast.MemberTypes.METHOD \
                    or node.member_type == ast.MemberTypes.CONSTRUCTOR:
                self.cur_method = node
                self.sym_table[self.cur_class.ident][self.cur_method.ident] \
                    = {"self": [node.ret_type, 0, 0, self.cur_class.ident, node.modifier]}
            if node.member_type == ast.MemberTypes.DATAMEMBER:
                self.sym_table[self.cur_class.ident][node.ident] \
                    = [node.ret_type, 0, 0, self.cur_class.ident, node.array, node.modifier]
                self.cur_method = None
            if node.ident == 'main':
                self.cur_class = node
                self.cur_method = None
                self.sym_table[self.cur_class.ident] = {}
        if node.member_type == ast.MemberTypes.CONSTRUCTOR:
            if node.ident != self.cur_class.ident:
                # print(f"wrong constructor name {node.ident} for class {self.cur_class.ident}")
                self.error_messages.append(f"wrong constructor name {node.ident} for class {self.cur_class.ident}")
                self.isErrorState = True
        super().visitMemberDecl(node)

    def isDuplicate(self, node):
        if self.cur_class is None:
            return False
        if self.cur_method is not None:
            if node.ident in self.sym_table[self.cur_class.ident][self.cur_method.ident]:
                # print("duplicate declaration:", node, "in", self.cur_class)
                self.error_messages.append(f"duplicate declaration: {node} in {self.cur_class}")
                self.isErrorState = True
                return True
            if isinstance(node, ast.ClassAndMemberDeclaration):
                if node.ident in self.sym_table[self.cur_class.ident]:
                    # print("duplicate declaration:", node, "in", self.cur_class)
                    self.error_messages.append(f"duplicate declaration: {node} in {self.cur_class}")
                    self.isErrorState = True
                    return True
        else:
            if node.ident in self.sym_table[self.cur_class.ident]:
                # print("duplicate declaration:", node, "in", self.cur_class)
                self.error_messages.append(f"duplicate declaration: {node} in {self.cur_class}")
                self.isErrorState = True
                return True
        if isinstance(node, ast.ClassAndMemberDeclaration) and node.member_type == ast.MemberTypes.CLASS:
            if node.ident in self.sym_table:
                self.error_messages.append(f"duplicate class declaration: {node}")
                self.isErrorState = True
                return True
        return False


class SymbolTableVisitor(Visitor):
    def __init__(self, sym_table):
        self.sym_table = sym_table
        self.cur_class: ast.ClassAndMemberDeclaration = None
        self.cur_method: ast.ClassAndMemberDeclaration = None
        self.isErrorState = False
        self.error_messages: list[str] = []
        '''
        how about for sym table, a list of dict so instead of it all in a dict 
        so I can access different sub sym tables by index easier
        example of sym table?
        {
            class 1: {
                data member 1: [type, size, offset]
                data member 2: [type, size, offset]
                member function 1: {
                    self: [ret_type, size, offset]
                    local var 1: [type, size, offset]
                }
                member function 2: {
                    self: [ret_type, size, offset]
                    local var 1: [type, size, offset]
                }
            }
            class 2: {
                data member 1: [type, size, offset]
                member function 1: {
                    self: [ret_type, size, offset]
                    local var 1: [type, size, offset]
                }
            }
            compunit aka main(): {
                local var 1: [type, size, offset]
                local var 2: [type, size, offset]
                local var 3: [type, size, offset]
            }
        }
        then can validate by saying
        enter class 1's node, remember what class we're in
        when entering it's functions, remember what function we're in
        looking at when a variable is used (like the expression IDENTIFIER) 
        and then go through the classes dict looking at the keys to match IDENTIFIER
        if it's not in the classes, go through the function's dict (in the classes dict)
        if it's not found then it's undeclared
        actually, would that end up being like hoisting?
        I would have to remember like line number? but that might not always work
        with multiple expressions on same line
        maybe do undeclared checks with the sym table maker
        to say there's no var x yet, because as building sym table 
        also checking everything for undeclared
        
        should give each node a reference to where it is in the sym table
        '''

    def visitExpr(self, node: ast.Expression):
        if node.op_type == ast.OpTypes.IDENTIFIER:
            is_in_sym, node_value = self.isInSym(node.value)
            if is_in_sym:
                # get the node it's type, node_value is [type, size, offset, classtype/isparam, isarray?]
                if isinstance(node_value, list):
                    node.type = node_value[0]
                    node.classtype = node_value[3]
                    node.array = node_value[4]
                else:  # should be dict, identifier node is a method
                    node.type = node_value["self"][0]
                    node.args = "method"  # maybe a dumb way to mark this identifier as a method
                    node.classtype = node_value["self"][3]
                # now that q is a Quad, gotta see about allowing it to access Quad's stuff
            else:
                # print("Possibly an undeclared variable")
                self.error_messages.append("Possibly an undeclared variable")

        # if node.op_type == ast.OpTypes.IDENTIFIER:
            # check if variable is undeclared
            if self.cur_method is not None:
                if node.value not in self.sym_table[self.cur_class.ident][self.cur_method.ident] \
                        and node.value not in self.sym_table[self.cur_class.ident] \
                        and not self.isInSym(node.value):
                    self.error_messages.append(f"Couldn't find '{node.value}' in {self.cur_class} sym table")
                    self.isErrorState = True
            elif self.cur_method is None:
                # if node.value not in self.sym_table[self.cur_class.ident]:
                if node.type is None:  # this works right if the code above worked properly
                    # the code above should be what gives all expr identifier nodes a type
                    # based on what was found in the sym table as it was being built
                    self.error_messages.append(f"Couldn't find '{node.value}' in main()'s sym table")
                    self.isErrorState = True
        # check for accessing private datamember
        if node.op_type == ast.OpTypes.PERIOD:
            is_in_sym, node_value = self.isInSym(node.right.value)
            if is_in_sym and len(node_value) > 4 and node_value[5] == ast.ModifierTypes.PRIVATE \
                    and self.cur_class.ident != node_value[3]:
                self.error_messages.append(f"tried to access private data member {node.right.value}")
                self.isErrorState = True

        super().visitExpr(node)

        if node.op_type == ast.OpTypes.PERIOD:
            # check if node.left is valid, and then go see if the node.right is real
            # gotta be mindful of args, and indexes?
            if node.left.op_type == ast.OpTypes.ARGUMENTS:
                # this probably only works for the situation q.Get_ul().x
                # where Get_ul() returns an object with an x
                is_in_sym, node_value = self.isInSym(node.left.left.right.value)
                if is_in_sym:
                    if node.right.value not in self.sym_table[node.left.left.right.type]:
                        # node.left.type probably a class
                        # then it's bad
                        # print(f"'{node.right.value}' not found within '{node.left.value}'s scope")
                        self.error_messages.append(f"'{node.right.value}' not found within '{node.left.value}'s scope")
                        self.isErrorState = True
            else:
                is_in_sym, node_value = self.isInSym(node.left.value)

                if is_in_sym:
                    # if left is in sym, how do I know if right is valid?
                    # if left type is a class, then I should check if right is in that class
                    if node.right.value not in self.sym_table[node.left.type]:  # node.left.type probably a class
                        # then it's bad
                        # print(f"'{node.right.value}' not found within '{node.left.value}'s scope")
                        self.error_messages.append(f"'{node.right.value}' not found within '{node.left.value}'s scope")
                        self.isErrorState = True

    def visitStmnt(self, node: ast.Statement):
        # no returning 'this' apparently
        # and checking the ret type for function
        if node.statement_type == ast.StatementTypes.RETURN and node.expr is not None:
            if node.expr.op_type == ast.OpTypes.THIS:
                self.error_messages.append(f"returned 'this' in {self.cur_class.ident}")
                self.isErrorState = True
            # if self.cur_method is not None and \
            #         node.expr.type != self.sym_table[self.cur_class.ident][self.cur_method.ident]["self"][0]:
            #     self.error_messages.append(f"wrong ret type for func {self.cur_method.ident}")
            #     self.isErrorState = True
        super().visitStmnt(node)

    def visitVarDecl(self, node: ast.VariableDeclaration):
        # check duplicate variable
        if not self.isDuplicate(node):
            if self.cur_method is not None:
                # vars not in main
                self.sym_table[self.cur_class.ident][self.cur_method.ident][node.ident] \
                    = [node.type, 0, 0, node.is_param, node.array]
                normaltypes = [x for x in ast.TypeTypes]
                if node.type not in normaltypes:
                    # probably an object var
                    node.is_obj = True
            else:
                # vars in main
                self.sym_table[self.cur_class.ident][node.ident] = [node.type, 0, 0, None, node.array]
                normaltypes = [x for x in ast.TypeTypes]
                if node.type not in normaltypes:
                    # probably an object var
                    node.is_obj = True
        super().visitVarDecl(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        # if not self.isDuplicate(node):
        if node.member_type == ast.MemberTypes.CLASS:
            self.cur_class = node
            # self.sym_table[self.cur_class.ident] = {}
            self.cur_method = None
        if node.member_type == ast.MemberTypes.METHOD \
                or node.member_type == ast.MemberTypes.CONSTRUCTOR:
            self.cur_method = node
            # self.sym_table[self.cur_class.ident][self.cur_method.ident] \
            #     = {"self": [node.ret_type, 0, 0, self.cur_class.ident, node.modifier]}
        if node.member_type == ast.MemberTypes.DATAMEMBER:
            # self.sym_table[self.cur_class.ident][node.ident] \
            #     = [node.ret_type, 0, 0, self.cur_class.ident, node.array, node.modifier]
            node.classtype = self.cur_class.ident
            self.cur_method = None
        if node.ident == 'main':
            self.cur_class = node
            self.cur_method = None
            # self.sym_table[self.cur_class.ident] = {}
        if node.member_type == ast.MemberTypes.CONSTRUCTOR:
            if node.ident != self.cur_class.ident:
                # print(f"wrong constructor name {node.ident} for class {self.cur_class.ident}")
                self.error_messages.append(f"wrong constructor name {node.ident} for class {self.cur_class.ident}")
                self.isErrorState = True
        super().visitMemberDecl(node)

    def visitCase(self, node: ast.Case):
        super().visitCase(node)

    def isDuplicate(self, node):
        if self.cur_class is None:
            return False
        if self.cur_method is not None:
            if node.ident in self.sym_table[self.cur_class.ident][self.cur_method.ident]:
                # print("duplicate declaration:", node, "in", self.cur_class)
                self.error_messages.append(f"duplicate declaration: {node} in {self.cur_class}")
                self.isErrorState = True
                return True
            if isinstance(node, ast.ClassAndMemberDeclaration):
                if node.ident in self.sym_table[self.cur_class.ident]:
                    # print("duplicate declaration:", node, "in", self.cur_class)
                    self.error_messages.append(f"duplicate declaration: {node} in {self.cur_class}")
                    self.isErrorState = True
                    return True
        else:
            if node.ident in self.sym_table[self.cur_class.ident]:
                # print("duplicate declaration:", node, "in", self.cur_class)
                self.error_messages.append(f"duplicate declaration: {node} in {self.cur_class}")
                self.isErrorState = True
                return True
        if isinstance(node, ast.ClassAndMemberDeclaration) and node.member_type == ast.MemberTypes.CLASS:
            if node.ident in self.sym_table:
                self.error_messages.append(f"duplicate class declaration: {node}")
                self.isErrorState = True
                return True
        return False

    # def isInSym(self, x):
    #     if x in self.sym_table:
    #         return True, self.sym_table[x]
    #     for k, v in self.sym_table.items():
    #         if isinstance(v, dict):
    #             if x in v:
    #                 return True, v[x]
    #             for k1, v1 in v.items():
    #                 if isinstance(v1, dict):
    #                     if x in v1:
    #                         return True, v1[x]
    #     return False, None


class AssignmentVisitor(Visitor):
    def __init__(self, sym_table):
        self.sym_table = sym_table
        self.isErrorState = False
        self.error_messages: list[str] = []
        self.keywords = set(k.value for k in ast.Keywords)
        self.assignment_operators = [
            ast.OpTypes.EQUALS,
            ast.OpTypes.PLUSEQUALS,
            ast.OpTypes.MINUSEQUALS,
            ast.OpTypes.TIMESEQUALS,
            ast.OpTypes.DIVIDEEQUALS,
        ]

    def visitExpr(self, node: ast.Expression):
        # basic check for assigning things to keywords
        if node.op_type in self.assignment_operators:
            if node.left.value in self.keywords:
                # print(f"keyword '{node.left.value}' was assigned to")
                self.error_messages.append(f"keyword '{node.left.value}' was assigned to")
                self.isErrorState = True
            if node.left.op_type == ast.OpTypes.NEW or node.left.op_type == ast.OpTypes.ARGUMENTS:
                self.error_messages.append(f"tried to assign to arguments or new operator illegally")
                self.isErrorState = True

        # check for argument expression attached to not a function
        # and if it is a function, make sure arguments are right
        if node.op_type == ast.OpTypes.ARGUMENTS:
            # one issue is that with the dot operator, when there's args they get put above dot in ast
            # so the args .left is the dot, and the dot's left and right are var and method (hopefully)
            # check for accessing private function
            if self.isInSym(node.left.right.value):
                funcnode = node.left.right
                if funcnode.args != "method":
                    self.error_messages.append(f"{funcnode} is not a method")
                    self.isErrorState = True
                else:
                    _, nodeinfo = self.isInSym(funcnode.value)
                    if nodeinfo["self"][4] == ast.ModifierTypes.PRIVATE:
                        self.error_messages.append(f"tried to call private function {funcnode.value}")
                        self.isErrorState = True
            if node.left.args != "method" and node.left.right.args != "method":
                # arguments nodes have a left, which is an expr
                # exprs have .args, but usually only the arguments expression types use it.
                # identifiers also set it to be == "method" if they are a method's identifier
                self.error_messages.append(f"'{node.left.right.value}' is not a method")
                self.isErrorState = True
            else:
                funcnode = node.left.right  # the expr ident node for the method being called
                reqdparams = []  # a list of all reqd params ident and values
                # print(node.args)  # args used to call the method
                # print(node.left.right.args)  # should be "method"
                # print(self.sym_table[node.left.right.classtype])  # the class sym table entry
                # print(self.sym_table[funcnode.classtype][funcnode.value])  # the function's sym table entry
                for k, v in self.sym_table[funcnode.classtype][funcnode.value].items():
                    if v[3] == True:  # this could be True, False, or a class ident
                        # if true then it's a parameter variable
                        reqdparams.append((k, v))
                # print("reqd", reqdparams)
                # if node.args is not None:
                #     print("given", [n.value for n in node.args])
                # else:
                #     print("none given")
                self.checkFuncParams(reqdparams, node, funcnode)

        if node.op_type == ast.OpTypes.NEW and node.index is None:
            # print([n.value for n in node.args])  # the args given to new
            # new could have index instead of args though, just not here
            # get the node.type (should be class name) then check the classes constructor, if it has one
            # if you try something like int[] x = new int();
            # it will have a KeyError here because the primitive type isn't in the sym table
            reqdparams = []
            if node.type in self.sym_table[node.type]:  # has a constructor
                for k, v in self.sym_table[node.type][node.type].items():
                    if v[3] == True:
                        reqdparams.append((k, v))
            funcnode = ast.Expression(None)
            funcnode.value = node.type
            self.checkFuncParams(reqdparams, node, funcnode)
        # don't let index be used on vars that aren't arrays
        if node.op_type == ast.OpTypes.INDEX:
            if not node.left.array:
                self.error_messages.append(f"var {node.left.value} was indexed but is not an array")
                self.isErrorState = True
            # is_in_sym, node_val = self.isInSym(node.left.value)
            # if is_in_sym:
            #     print(node_val)
            # self.sym_table[node.left]
            # self.error_messages.append(f"new operator had args and indecies")
            # self.isErrorState = True
        super().visitExpr(node)

    def checkFuncParams(self, reqdparams, node, funcnode):
        try:
            for i in range(len(reqdparams)):
                if reqdparams[i][1][0] != node.args[i].type:
                    # print(reqdparams[i][0], node.args[i].value)
                    # print(reqdparams[i][1][0], node.args[i].type)
                    self.error_messages.append(f"invalid parameters for {funcnode.value}, {node.args[i].value}")
                    self.isErrorState = True
                    if node.args[i].type is None:
                        self.error_messages.append(f"argument {node.args[i].value} probably doesn't exist")
            if node.args is not None and len(node.args) > len(reqdparams):
                self.error_messages.append(f"too many arguments given for {funcnode.value}")
                self.isErrorState = True

        except Exception as e:
            self.error_messages.append(f"error {e}: not enough args")
            self.isErrorState = True

class BreakVisitor(Visitor):
    def __init__(self):
        self.in_while: bool = False
        self.in_case: bool = False
        self.in_switch: bool = False
        self.isErrorState = False
        self.error_messages: list[str] = []

    def visitStmnt(self, node: ast.Statement):
        if node.statement_type == ast.StatementTypes.WHILE:
            self.in_while = True
        if node.statement_type == ast.StatementTypes.SWITCH:
            self.in_switch = True
        if node.statement_type == ast.StatementTypes.BREAK:
            if not self.in_case and not self.in_while and not self.in_switch:
                self.error_messages.append(f"break statement in an invalid place")
                self.isErrorState = True
        super().visitStmnt(node)
        if node.statement_type == ast.StatementTypes.WHILE:
            self.in_while = False
        if node.statement_type == ast.StatementTypes.SWITCH:
            self.in_switch = False

    def visitCase(self, node: ast.Case):
        self.in_case = True
        super().visitCase(node)
        self.in_case = False


class CinVisitor(Visitor):
    def __init__(self, sym_table):
        self.isErrorState = False
        self.error_messages = []
        self.sym_table = sym_table

    def visitStmnt(self, node: ast.Statement):
        if node.statement_type == ast.StatementTypes.CIN:
            # I need to check cin's expr, it has to either be type int or char,
            # or be a dot where dot.right needs to be an int or char
            cinexpr = node.expr
            # if cinexpr.op_type == ast.OpTypes.PERIOD:
            #     if cinexpr.right.type is not ast.TypeTypes.INT \
            #             and cinexpr.right.type is not ast.TypeTypes.CHAR \
            #             or cinexpr.right.args == "method":
            #         self.error_messages.append(f"error using cin on invalid var {cinexpr}")
            #         self.isErrorState = True
            if cinexpr.op_type != ast.OpTypes.IDENTIFIER:
                self.error_messages.append(f"error using cin on invalid var {cinexpr}")
                self.isErrorState = True
        super().visitStmnt(node)


class ExpressionTypeVisitor(Visitor):
    def __init__(self, sym_table):
        self.cur_class = None
        self.cur_method = None
        self.isErrorState = False
        self.error_messages = []
        self.sym_table = sym_table
        self.returns_bool = [
            ast.OpTypes.DOUBLEEQUALS,
            ast.OpTypes.NOTEQUALS,
            ast.OpTypes.LESSTHAN,
            ast.OpTypes.GREATERTHAN,
            ast.OpTypes.LESSOREQUAL,
            ast.OpTypes.GREATEROREQUAL,
            ast.OpTypes.AND,
            ast.OpTypes.OR,
        ]
        self.returns_int = [
            ast.OpTypes.PLUS,
            ast.OpTypes.MINUS,
            ast.OpTypes.TIMES,
            ast.OpTypes.DIVIDE,
        ]

    def visitExpr(self, node: ast.Expression):
        super().visitExpr(node)
        if node.op_type in self.returns_int:
            # if node.left is not None and node.left.type != node.right.type:
            #     self.error_messages.append(f"wrong operands for {node.op_type.value}, "
            #                                f"{node.left.value} {node.right.value}, ")
            #     self.isErrorState = True
            # else:
            node.type = ast.TypeTypes.INT
        if node.op_type in self.returns_bool:
            dotindexargs = [ast.OpTypes.PERIOD, ast.OpTypes.INDEX, ast.OpTypes.ARGUMENTS]
            if node.left.op_type == ast.OpTypes.INDEX and node.right not in dotindexargs:
                if node.left.left.type != node.right.type:
                    self.error_messages.append(f"wrong operands for {node.op_type.value}, "
                                               f"{node.left.left.value} {node.right.value}, ")
                    self.isErrorState = True
                else:
                    node.type = ast.TypeTypes.BOOL
            elif node.right.op_type == ast.OpTypes.INDEX and node.left not in dotindexargs:
                if node.left.type != node.right.left.type:
                    self.error_messages.append(f"wrong operands for {node.op_type.value}, "
                                               f"{node.left.value} {node.right.left.value}, ")
                    self.isErrorState = True
                else:
                    node.type = ast.TypeTypes.BOOL
            elif node.left.op_type == ast.OpTypes.PERIOD and node.right not in dotindexargs:
                if node.left.right.type != node.right.type:
                    self.error_messages.append(f"wrong operands for {node.op_type.value}, "
                                               f"{node.left.value} {node.right.value}, ")
                    self.isErrorState = True
                else:
                    node.type = ast.TypeTypes.BOOL
            elif node.right.op_type == ast.OpTypes.PERIOD and node.left not in dotindexargs:
                if node.left.type != node.right.right.type:
                    self.error_messages.append(f"wrong operands for {node.op_type.value}, "
                                               f"{node.left.value} {node.right.right.value}, ")
                    self.isErrorState = True
                else:
                    node.type = ast.TypeTypes.BOOL
            elif node.left.op_type == ast.OpTypes.ARGUMENTS and node.right not in dotindexargs:
                # this is getting silly, I should rethink. lol
                if node.left.left.right.type != node.right.type:
                    self.error_messages.append(f"wrong operands for {node.op_type.value}, "
                                               f"{node.left.value} {node.right.value}, ")
                    self.isErrorState = True
                else:
                    node.type = ast.TypeTypes.BOOL
            elif node.right.op_type == ast.OpTypes.ARGUMENTS and node.left not in dotindexargs:
                if node.left.type != node.right.left.right.type:
                    self.error_messages.append(f"wrong operands for {node.op_type.value}, "
                                               f"{node.left.value} {node.right.value}, ")
                    self.isErrorState = True
                else:
                    node.type = ast.TypeTypes.BOOL
            elif node.left.type != node.right.type:
                self.error_messages.append(f"wrong operands for {node.op_type.value}, "
                                           f"{node.left.value} {node.right.value}, "
                                           f"they must be the same type")
                self.isErrorState = True
            else:
                node.type = ast.TypeTypes.BOOL
        # if node.op_type == ast.OpTypes.ARGUMENTS:
        #     if node.left.right.args == "method":
        #         print("sus")

    def visitStmnt(self, node: ast.Statement):
        if self.cur_method is not None and node.statement_type == ast.StatementTypes.RETURN:
            realnode = ast.Expression(None)
            if node.expr.op_type == ast.OpTypes.ARGUMENTS:
                realnode = node.expr.left.right
            if node.expr.type != self.sym_table[self.cur_class.ident][self.cur_method.ident]["self"][0] \
                    and realnode.type != self.sym_table[self.cur_class.ident][self.cur_method.ident]["self"][0]:
                self.error_messages.append(f"wrong ret type for func {self.cur_method.ident}")
                self.isErrorState = True
        if self.cur_class.ident == "main" and node.statement_type == ast.StatementTypes.RETURN:
            if node.expr is not None:
                self.error_messages.append(f"wrong ret type for func {self.cur_class.ident}")
                self.isErrorState = True
        super().visitStmnt(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        if node.member_type == ast.MemberTypes.METHOD:
            self.cur_method = node
        if node.member_type == ast.MemberTypes.CLASS:
            self.cur_class = node
        if node.ident == 'main':
            self.cur_class = node
            self.cur_method = None
        super().visitMemberDecl(node)


class TypesVisitor(Visitor):
    def __init__(self, sym_table):
        self.isErrorState = False
        self.error_messages = []
        self.sym_table = sym_table
        self.reg_types = [x for x in ast.TypeTypes]
        self.bool_ops = [
            ast.OpTypes.AND,
            ast.OpTypes.OR,
        ]
        self.math_ops = [
            ast.OpTypes.PLUS,
            ast.OpTypes.MINUS,
            ast.OpTypes.TIMES,
            ast.OpTypes.DIVIDE,
        ]
        self.assn_ops = [
            ast.OpTypes.PLUSEQUALS,
            ast.OpTypes.MINUSEQUALS,
            ast.OpTypes.TIMESEQUALS,
            ast.OpTypes.DIVIDEEQUALS,
            ast.OpTypes.EQUALS,
        ]

    def visitExpr(self, node: ast.Expression):
        if node.op_type in self.math_ops:
            if node.right.op_type == ast.OpTypes.NEW:
                pass  # TODO might want to figure out something like x = 3 + (new Test()).one()
                # where one() would return the number one or something
            # TODO this is pretty wack
            elif node.left is not None and node.right is not None and \
                    node.left.type is not None and node.right.type is not None and \
                    (node.left.type != ast.TypeTypes.INT or node.right.type != ast.TypeTypes.INT):
                self.error_messages.append(f"illegal operand(s) for {node.op_type.value}, "
                                           f"{node.left.value} {node.right.value}")
                self.isErrorState = True
            elif node.right is not None and node.right.type != ast.TypeTypes.INT:
                self.error_messages.append(f"illegal operand(s) for {node.op_type.value}, "
                                           f"{node.left} {node.right}")
                self.isErrorState = True
        if node.op_type in self.bool_ops:
            if node.left.type != ast.TypeTypes.BOOL and node.right.type != ast.TypeTypes.BOOL:
                self.error_messages.append(f"illegal operand(s) for {node.op_type.value}, "
                                           f"{node.left.type.value} {node.right.type.value}")
                self.isErrorState = True
        if node.op_type == ast.OpTypes.EXCLAMATIONMARK:
            if node.right.type != ast.TypeTypes.BOOL:
                self.error_messages.append(f"illegal operand(s) for {node.op_type.value}, "
                                           f"{node.right.type.value}")
                self.isErrorState = True
        if node.op_type == ast.OpTypes.NEW:
            if node.index is not None and node.index.type != ast.TypeTypes.INT:
                self.error_messages.append(f"can only index with int {node}")
                self.isErrorState = True
        if node.op_type == ast.OpTypes.INDEX:
            if node.index is not None and node.index.type != ast.TypeTypes.INT:
                self.error_messages.append(f"can only index into array {node.left.value} with int")
                self.isErrorState = True
        if node.op_type in self.assn_ops:
            if node.left.type is not None and node.right.type is not None:
                if node.left.type != node.right.type:  # probably wrong?
                    self.error_messages.append(f"invalid types in assignment {node.left.value} = {node.right.value}")
                    self.isErrorState = True
            if node.left.array and node.right.op_type != ast.OpTypes.NEW:
                self.error_messages.append(f"can only assign array '{node.left.value}' with a new array")
                self.isErrorState = True
            if node.left.op_type == ast.OpTypes.PERIOD and node.right.op_type != ast.OpTypes.NEW \
                    and node.left.right.array:
                self.error_messages.append(f"can only assign array '{node.left.value}' with a new array")
                self.isErrorState = True
            if node.left.op_type == ast.OpTypes.INDEX and node.left.index is not None:
                ind = node.left
                if ind.left.array and ind.left.type != node.right.type:
                    self.error_messages.append(f"invalid assignment {ind.left.value}[{ind.index.value}] = {node.right.type}")
                    self.isErrorState = True
            if node.left.op_type in self.math_ops:
                self.error_messages.append(f"invalid assignment to {node.left.op_type},  {node.right.value}")
                self.isErrorState = True
        super().visitExpr(node)

    def visitStmnt(self, node: ast.Statement):
        if node.statement_type == ast.StatementTypes.IF:
            if node.expr.type != ast.TypeTypes.BOOL:
                self.error_messages.append(f"if statement requires bool, got {node.expr.type}")
                self.isErrorState = True
        if node.statement_type == ast.StatementTypes.WHILE:
            if node.expr.type != ast.TypeTypes.BOOL:
                self.error_messages.append(f"while statement requires bool, got {node.expr.type}")
                self.isErrorState = True
        super().visitStmnt(node)

    def visitVarDecl(self, node: ast.VariableDeclaration):
        if node.init is not None and node.init.type is not None:
            if node.type != node.init.type and node.init.value != "null":
                self.error_messages.append(f"did invalid assignment in initializer for {node}")
                self.isErrorState = True
        if node.type not in self.reg_types and node.type not in self.sym_table:
            self.error_messages.append(f"did invalid type in var {node}")
            self.isErrorState = True
        super().visitVarDecl(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):

        if node.init is not None and node.init.type is not None:
            if node.ret_type != node.init.type and node.init.value != "null":
                self.error_messages.append(f"did invalid assignment in initializer for {node}")
                self.isErrorState = True

        super().visitMemberDecl(node)

    def visitCase(self, node: ast.Case):
        super().visitCase(node)


"""
wanna make a new visitor? just copy and update the name
class classname(Visitor):
    def __init__(self):
        self.isErrorState = False
        self.error_messages = []

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