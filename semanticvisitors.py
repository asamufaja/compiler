import abc


class Visitor:
    @abc.abstractmethod
    def visit(self):
        None


class SymbolTableVisitor(Visitor):
    def visit(self):
        None