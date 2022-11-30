import starting_lexer_parser as lp
import visitors as v
import astclasses as ast
import sys


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

    # print(tablevisitor.sym_table)
    # for key, val in tablevisitor.sym_table.items():
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
'''
{
    <astclasses.ClassAndMemberDeclaration object at 0x0000020366FABEB0>: {
        <astclasses.ClassAndMemberDeclaration object at 0x0000020366FABFA0>: [<TypeTypes.INT: 'int'>, 0, 0], 
        <astclasses.ClassAndMemberDeclaration object at 0x0000020366FABF70>: [<TypeTypes.INT: 'int'>, 0, 0]
    }, 
    <astclasses.ClassAndMemberDeclaration object at 0x00000203670A95B0>: {
        <astclasses.ClassAndMemberDeclaration object at 0x00000203670A9040>: [<TypeTypes.CLASS: 'class'>, 0, 0], 
        <astclasses.ClassAndMemberDeclaration object at 0x00000203670A91C0>: [<TypeTypes.CLASS: 'class'>, 0, 0], 
        <astclasses.ClassAndMemberDeclaration object at 0x00000203670A90A0>: [<TypeTypes.INT: 'int'>, 0, 0], 
        <astclasses.ClassAndMemberDeclaration object at 0x00000203670A9160>: {}, 
        <astclasses.ClassAndMemberDeclaration object at 0x00000203670A93D0>: {
            <astclasses.VariableDeclaration object at 0x00000203670A92E0>: [<TypeTypes.INT: 'int'>, 0, 0], 
            <astclasses.VariableDeclaration object at 0x00000203670A94C0>: [<TypeTypes.CHAR: 'char'>, 0, 0], 
            <astclasses.VariableDeclaration object at 0x00000203670A9190>: [<TypeTypes.BOOL: 'bool'>, 0, 0], 
            <astclasses.VariableDeclaration object at 0x00000203670A9640>: [<TypeTypes.INT: 'int'>, 0, 0]
        }
    }, 
    <astclasses.ClassAndMemberDeclaration object at 0x00000203670A9AF0>: {
        <astclasses.VariableDeclaration object at 0x00000203670A9820>: [<TypeTypes.CLASS: 'class'>, 0, 0], 
        <astclasses.VariableDeclaration object at 0x00000203670A9C40>: [<TypeTypes.INT: 'int'>, 0, 0]
    }
}
'''


if __name__ == '__main__':
    main(sys.argv[1:])
