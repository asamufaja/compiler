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
    compunit.accept(printvisitor)


if __name__ == '__main__':
    main(sys.argv[1:])