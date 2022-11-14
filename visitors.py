import abc


class Visitor:
    @abc.abstractmethod
    def visit(self):
        None


class PrintAST(Visitor):



class SymbolTableVisitor(Visitor):
    def visit(self):
        None