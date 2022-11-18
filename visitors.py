import abc
import astclasses as ast


class Visitor:
    def visitExpr(self, node):
        if node.left is not None:
            node.left.accept(self)
        if node.right is not None and not isinstance(node.right, str):  # if it's IDENTIFIER it won't have accept()
            node.right.accept(self)
        if node.index is not None:
            for index in node.index:
                index.accept(self)
        if node.args is not None:
            for arg in node.args:
                arg.accept(self)

    def visitStmnt(self, node):
        if node.statement_type == ast.StatementTypes.BRACES:
            for stmnt in node.substatement:
                stmnt.accept(self)
        if node.statement_type == ast.StatementTypes.EXPRESSION:
            node.expr.accept(self)
        if node.statement_type == ast.StatementTypes.IF:
            node.expr.accept(self)
            for stmnt in node.substatement:
                stmnt.accept(self)
            if node.else_statement is not None:
                for stmnt in node.else_statement:
                    stmnt.accept(self)
        if node.statement_type == ast.StatementTypes.WHILE:
            node.expr.accept(self)
            if node.substatement is not None:
                node.substatement.accept(self)
        if node.statement_type == ast.StatementTypes.RETURN \
                or node.statement_type == ast.StatementTypes.COUT \
                or node.statement_type == ast.StatementTypes.CIN:
            if node.expr is not None:
                node.expr.accept(self)
        # if node.statement_type == ast.StatementTypes.COUT:
        #     pass
        # if node.statement_type == ast.StatementTypes.CIN:
        #     pass
        if node.statement_type == ast.StatementTypes.SWITCH:
            node.expr.accept(self)
            for casenode in node.case_list:
                casenode.accept(self)
            for stmnt in node.default_stmnts:
                stmnt.accept(self)
        # if node.statement_type == ast.StatementTypes.BREAK:
        #     pass
        # if node.statement_type == ast.StatementTypes.VAR_DECL:
        #     pass  # I don't currently make a Statement node that contains a VariableDeclaration

    def visitVarDecl(self, node):
        if node.init is not None:
            node.init.accept(self)

    def visitMemberDecl(self, node):
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
            # it is list of statements, the body of the main()
            for stmnt in node.child:
                stmnt.accept(self)
    
    def visitCase(self, node):
        if node.statements is not None:
            for stmnt in node.statements:
                stmnt.accept(self)


class PrintAST(Visitor):
    def __init__(self):
        self.indentLevel = 0
        self.tab = "  "
    
    def visitExpr(self, node):
        print(f"{self.tab*self.indentLevel}{node.op_type}, type:{node.type}, valaue:{node.value}")
        super().visitExpr(node)

    def visitStmnt(self, node):
        print(f"{self.tab*self.indentLevel}{node.statement_type}")
        self.indentLevel += 1
        super().visitStmnt(node)
        self.indentLevel -= 1

    def visitVarDecl(self, node):
        print(f"{self.tab*self.indentLevel}{node.type}, {node.ident}")
        super().visitVarDecl(node)

    def visitMemberDecl(self, node):
        print(f"{self.tab*self.indentLevel}{node.modifier}, {node.ret_type}, {node.ident}")
        if node.ret_type == ast.TypeTypes.CLASS \
            or node.body is not None:
            self.indentLevel += 1
        super().visitMemberDecl(node)
        if node.ret_type == ast.TypeTypes.CLASS \
            or node.body is not None:
            self.indentLevel -= 1


class SymbolTableVisitor(Visitor):
    def __init__(self):
        self.sym_table = dict()
        self.cur_class = None
        self.cur_method = None
        '''
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
        '''

    def visitExpr(self, node):
        pass

    def visitStmnt(self, node):
        pass

    def visitVarDecl(self, node):
        pass

    def visitMemberDecl(self, node):
        pass
