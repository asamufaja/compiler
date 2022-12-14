import starting_lexer_parser as lp
import semanticvisitors as v
import sys
import codegenvisitors as cv
import astclasses as ast


def main(args):
    lexer = lp.BigLexer()
    parser = lp.BigParser()

    kxi = open(args[0], 'r')
    compunit: ast.ClassAndMemberDeclaration = parser.parse(lexer.tokenize(kxi.read()))

    printvisitor = v.PrintAST()
    # compunit.accept(printvisitor)
    # printvisitor.makeTree()

    pretablevisitor = v.PreSymbolTableVisitor({})
    compunit.accept(pretablevisitor)
    print("pre-table errors", pretablevisitor.error_messages)
    tablevisitor = v.SymbolTableVisitor(pretablevisitor.sym_table)
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
    addthis = cv.AddThisVisitor(tablevisitor.sym_table)
    compunit.accept(addthis)
    varinits = cv.VarInitToEquals()
    compunit.accept(varinits)

    # compunit.accept(printvisitor)
    # printvisitor.makeTree()

    vars = cv.VarsAndMembers(tablevisitor.sym_table)
    compunit.accept(vars)
    codegen = cv.CodeGen(vars.asmfile, tablevisitor.sym_table)
    compunit.accept(codegen)

    # print(tablevisitor.sym_table)
    # for key, val in codegen.sym_table.items():
    #     print(key)
    #     if isinstance(val, dict):
    #         for key1, val1 in val.items():
    #             print(key1)
    #             if isinstance(val1, dict):
    #                 for key2, val2 in val1.items():
    #                     print(key2)
    #                     print('  ', val2)
    #             else:
    #                 print('  ', val1)
    #     else:
    #         print('  ', val)


if __name__ == '__main__':
    main(sys.argv[1:])
