import starting_lexer_parser as lp
import semanticvisitors as v
import sys
import codegenvisitors as cv


def main(args):
    lexer = lp.BigLexer()
    parser = lp.BigParser()

    kxi = open(args[0], 'r')
    compunit = parser.parse(lexer.tokenize(kxi.read()))
    printvisitor = v.PrintAST()
    # try:
    compunit.accept(printvisitor)
    # except:
    #     print(f"Got {sys.exc_info()[0]} from going through the nodes")
    printvisitor.makeTree()

    tablevisitor = v.SymbolTableVisitor()
    compunit.accept(tablevisitor)
    print("table errors", tablevisitor.error_messages)
    assignmentvisitor = v.AssignmentVisitor(tablevisitor.sym_table)
    compunit.accept(assignmentvisitor)
    print("assignment errors", assignmentvisitor.error_messages)
    breakvisitor = v.BreakVisitor()
    compunit.accept(breakvisitor)
    print("break error", breakvisitor.error_messages)
    cinvisitor = v.CinVisitor(tablevisitor.sym_table)
    compunit.accept(cinvisitor)
    print("cin error", cinvisitor.error_messages)
    pretypes = v.ExpressionTypeVisitor(tablevisitor.sym_table)
    compunit.accept(pretypes)
    print("pre_types error", pretypes.error_messages)
    typesvisitor = v.TypesVisitor(tablevisitor.sym_table)
    compunit.accept(typesvisitor)
    print("types error", typesvisitor.error_messages)


if __name__ == '__main__':
    main(sys.argv[1:])
