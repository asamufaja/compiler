import starting_lexer_parser as lp
import semanticvisitors as v
import codegenvisitors as cv
import sys
import pydot


def dashC(kxi, lexer, parser):
    compunit = dashS(kxi, lexer, parser)
    if not compunit:
        print("cannot compile due to error in semantics")
        return
    setupdir = cv.SetupDirectives()
    compunit.accept(setupdir)
    exprgen = cv.ExpressionGen(setupdir.asmfile)
    compunit.accept(exprgen)
    setupdir.asmfile.close()


def dashS(kxi, lexer, parser):
    compunit = dashP(kxi, lexer, parser)
    pretablevisitor = v.PreSymbolTableVisitor({})
    compunit.accept(pretablevisitor)
    if pretablevisitor.isErrorState:
        raise Exception()
    tablevisitor = v.SymbolTableVisitor()
    compunit.accept(tablevisitor)
    if tablevisitor.isErrorState:
        print("error at table visitor", tablevisitor.error_messages)
        return
    assignmentvisitor = v.AssignmentVisitor(tablevisitor.sym_table)
    compunit.accept(assignmentvisitor)
    if assignmentvisitor.isErrorState:
        print("error at assignment checking", assignmentvisitor.error_messages)
        return
    breakvisitor = v.BreakVisitor()
    compunit.accept(breakvisitor)
    if assignmentvisitor.isErrorState:
        print("error at break visitor", breakvisitor.error_messages)
        return
    cinvisitor = v.CinVisitor(tablevisitor.sym_table)
    compunit.accept(cinvisitor)
    if cinvisitor.isErrorState:
        print("error at other visitor", cinvisitor.error_messages)
        return
    pretypes = v.ExpressionTypeVisitor(tablevisitor.sym_table)
    compunit.accept(pretypes)
    if pretypes.isErrorState:
        print("pre_types error", pretypes.error_messages)
        return
    typesvisitor = v.TypesVisitor(tablevisitor.sym_table)
    compunit.accept(typesvisitor)
    if typesvisitor.isErrorState:
        print("types error", typesvisitor.error_messages)
        return
    return compunit


def dashP(kxi, lexer, parser):
    compunit = parser.parse(dashL(kxi, lexer))
    printvisitor = v.PrintAST()
    compunit.accept(printvisitor)
    printvisitor.makeTree()
    return compunit


def dashL(kxi, lexer):
    tokens = lexer.tokenize(kxi.read())
    return tokens

def main(args):
    lexer = lp.BigLexer()
    parser = lp.BigParser()

    kxi = [x for x in args if x.endswith(".kxi")]
    if kxi:
        kxi = open(kxi[0], 'r')
    else:
        print("didn't detect a file")
    if "-c" in args:
        dashC(kxi, lexer, parser)
    if "-s" in args:
        dashS(kxi, lexer, parser)
    if "-p" in args:
        dashP(kxi, lexer, parser)
    if "-l" in args:
        tokens = dashL(kxi, lexer)
        for t in [t for t in tokens]:  # t's everywhere
            print(t)


if __name__ == '__main__':
    main(sys.argv[1:])
