import astclasses as ast
import pydot


class Visitor:
    def visitExpr(self, node: ast.Expression):
        if node.left is not None:
            node.left.accept(self)
        if node.right is not None:
            node.right.accept(self)
        if node.index is not None:
            node.index.accept(self)
        if node.args is not None:
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
            if node.else_statement is not None:
                for stmnt in node.else_statement:
                    stmnt.accept(self)
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
        if node.child is not None:  # the only place I use child for this node type is comp unit
            node.child.accept(self)

    def visitCase(self, node: ast.Case):
        if node.statements is not None:
            for stmnt in node.statements:
                stmnt.accept(self)


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
        for n in node.else_statement:
            self.graph.add_edge(pydot.Edge(f"{node}", f"{n}"))
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


class SymbolTableVisitor(Visitor):
    def __init__(self):
        self.sym_table = dict()
        self.cur_class = None
        self.cur_method = None
        '''
        how about for sym table, a list of dict so instead of it all in a dict 
        so I can access different sub sym tables by index easier
        example of sym table?
        {
            class 1: {
                data member 1: [type, size, offset]
                data member 2: [type, size, offset]
                member function 1: {
                    local var 1: [type, size offset]
                }
                member function 2: {
                    local var 1: [type, size offset]
                }
            }
            class 2: {
                data member 1: [type, size offset]
                member function 1: {
                    local var 1: [type, size offset]
                }
            }
            compunit aka main(): {
                local var 1: [type, size offset]
                local var 2: [type, size offset]
                local var 3: [type, size offset]
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
                # get the node it's type, node_value is [type, size, offset]
                node.type = node_value[0]
                print(node.value, node.type)
                # now that q is a Quad, gotta see about allowing it to access Quad's stuff
        if node.op_type == ast.OpTypes.PERIOD:
            # check if node.left is valid, and then go see if the node.right is real
            is_in_sym, node_value = self.isInSym(node.left.value)
            if is_in_sym:
                # if left is in sym, how do I know if right is valid?
                # if left type is a class, then I should check if right is in that class

                pass

        if node.op_type == ast.OpTypes.IDENTIFIER:
            # check if variable is undeclared
            if self.cur_method is not None:
                if node.value not in self.sym_table[self.cur_class][self.cur_method] \
                        and node.value not in self.sym_table[self.cur_class]:
                    print(self.cur_class, self.cur_method)
                    print("1didn't find", node, "in sym table")
            elif self.cur_method is None:
                if node.value not in self.sym_table[self.cur_class]:
                    print("2didn't find", node, "in sym table")
                    print(node.type)
        super().visitExpr(node)

    def visitStmnt(self, node: ast.Statement):
        super().visitStmnt(node)

    def visitVarDecl(self, node: ast.VariableDeclaration):
        # check duplicate variable
        if not self.isDuplicate(node):
            if self.cur_method is not None:
                self.sym_table[self.cur_class][self.cur_method][node.ident] = [node.type, 0, 0]
            else:
                self.sym_table[self.cur_class][node.ident] = [node.type, 0, 0]
        super().visitVarDecl(node)

    def visitMemberDecl(self, node: ast.ClassAndMemberDeclaration):
        if node.member_type == ast.MemberTypes.CLASS:
            self.cur_class = node
            self.sym_table[self.cur_class] = {}
        if node.member_type == ast.MemberTypes.METHOD \
                or node.member_type == ast.MemberTypes.CONSTRUCTOR:
            self.cur_method = node
            self.sym_table[self.cur_class][self.cur_method] = {}
        if node.member_type == ast.MemberTypes.DATAMEMBER:
            self.sym_table[self.cur_class][node.ident] = [node.ret_type, 0, 0]
        if node.ident == 'main':
            self.cur_class = node
            self.cur_method = None
            self.sym_table[self.cur_class] = {}
        # if node.ident == "compunit":
        #     self.sym_table[node]
        super().visitMemberDecl(node)

    def visitCase(self, node: ast.Case):
        super().visitCase(node)

    def isDuplicate(self, node):
        if self.cur_method is not None:
            if node.ident in self.sym_table[self.cur_class][self.cur_method]:
                print("duplicate decl", node)
                return True
        else:
            if node.ident in self.sym_table[self.cur_class]:
                print("duplicate decl", node)
                return True
        return False

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