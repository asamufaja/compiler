import starting_lexer_parser as lp
import semanticvisitors as v
import codegenvisitors as cv
import sys


def dashC(kxi, lexer, parser):
    compunit, sym_table = dashS(kxi, lexer, parser)
    if not compunit:
        print("cannot compile due to error in semantics")
        return
    mathassndesugar = cv.MathAssignDesugar()
    compunit.accept(mathassndesugar)
    notequals = cv.NotEqualsVisitor()
    compunit.accept(notequals)
    lessorgreater = cv.LessOrGreater()
    compunit.accept(lessorgreater)
    whiletoif = cv.WhileToIf()
    compunit.accept(whiletoif)
    # switchtoif = cv.SwitchToIf()
    # compunit.accept(switchtoif)
    iftruefalse = cv.IfTrueFalse()
    compunit.accept(iftruefalse)
    addthis = cv.AddThisVisitor(sym_table)
    compunit.accept(addthis)
    varinits = cv.VarInitToEquals()
    compunit.accept(varinits)

    vars = cv.VarsAndMembers(sym_table)
    compunit.accept(vars)
    codegen = cv.CodeGen(vars.asmfile, sym_table)
    compunit.accept(codegen)


def dashS(kxi, lexer, parser):
    compunit = dashP(kxi, lexer, parser)
    pretablevisitor = v.PreSymbolTableVisitor({})
    compunit.accept(pretablevisitor)
    # TODO maybe should leave this here
    addthis = cv.AddThisVisitor(pretablevisitor.sym_table)
    compunit.accept(addthis)

    if pretablevisitor.isErrorState:
        raise Exception()
    tablevisitor = v.SymbolTableVisitor(pretablevisitor.sym_table)
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
    return compunit, tablevisitor.sym_table


def dashP(kxi, lexer, parser):
    compunit = parser.parse(dashL(kxi, lexer))
    printvisitor = v.PrintAST()
    compunit.accept(printvisitor)
    # printvisitor.makeTree()
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
