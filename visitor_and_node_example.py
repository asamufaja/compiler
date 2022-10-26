from abc import abstractmethod


class visitor:
    def visit(self, node):
        print(node.letter)


class node:
    @abstractmethod
    def accept(self, visitor):
        pass


class letterNode(node):
    letter:str
    next:node
    def __init__(self, letter):
        self.letter = letter
        self.next = None
    def accept(self, visitor):
        visitor.visit(self)
        if self.next != None:
            self.next.accept(visitor)


def main():
    h = letterNode("h")
    i = letterNode("i")
    h.next = i
    myvisitor = visitor()
    h.accept(myvisitor)



if __name__ == '__main__':
    main()