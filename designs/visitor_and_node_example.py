from abc import abstractmethod


class visitor:
    def visit(self, node):
        print(node.letter)
        if node.next != None:
            node.next.accept(self)


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


def main():
    h = letterNode("h")
    i = letterNode("i")
    h.next = i
    myvisitor = visitor()
    h.accept(myvisitor)



if __name__ == '__main__':
    main()