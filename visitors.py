import abc
import astclasses as ast


class Visitor:
    def visitExpr(self, node):
        if node.left != None:
            node.left.accept(self)
        if node.right != None:
            node.right.accept(self)
        if node.index != None:
            for index in node.index:
                index.accept(self)
        if node.args != None:
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
            if node.else_statement != None:
                for stmnt in node.else_statement:
                    stmnt.accept(self)
        if node.statement_type == ast.StatementTypes.WHILE:
            node.expr.accept(self)
            if node.substatement != None:
                node.substatement.accept(self)
        if node.statement_type == ast.StatementTypes.RETURN
            or node.statement_type == ast.StatementTypes.COUT
            or node.statement_type == ast.StatementTypes.CIN:
            if node.expr != None:
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
        pass

    def visitMemberDecl(self, node):
        pass
    
    def visitCase(self, node):
        pass


class PrintAST(Visitor):
    def __init__(self):
        self.indentLevel = 0
        self.tab = "  "

    def visit(self, node):
        pass
    
    def visitExpr(self, node):
        pass

    def visitStmnt(self, node):
        if node.statement_type == ast.StatementTypes.IF:
            node.expr.accept(self)
            for stmnt in node.substatement:
                node.accept(stmnt)
            if node.else_statement != None:
                for stmnt in node.else_statement:
                    node.accept(stmnt)

    def visitVarDecl(self, node):
        pass

    def visitMemberDecl(self, node):
        pass


class SymbolTableVisitor(Visitor):
    def visit(self, node):
        pass
    
    def visitExpr(self, node):
        pass

    def visitStmnt(self, node):
        pass

    def visitVarDecl(self, node):
        pass

    def visitMemberDecl(self, node):
        pass
