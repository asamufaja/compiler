import astclasses as ast
import visitors as v
import starting_lexer_parser as lp

def main():
    list_of_files = [
        "kxi_test/unit/lexical/json.fail.kxi",
        "kxi_test/unit/lexical/no_token.fail.kxi",
        "kxi_test/unit/parsing/class_name.fail.kxi",
        "kxi_test/unit/parsing/detached_else.fail.kxi",
        "kxi_test/unit/parsing/dup_cases.fail.kxi",
        "kxi_test/unit/parsing/empty.fail.kxi",
        "kxi_test/unit/parsing/keyword_assn.fail.kxi",  # not a parser error for me
        "kxi_test/unit/parsing/keyword_decl.fail.kxi",
        "kxi_test/unit/parsing/keyword_decl.pass.kxi",
        "kxi_test/unit/parsing/operator_precedence.pass.kxi",
        "kxi_test/unit/parsing/pythondict.fail.kxi",
        "kxi_test/unit/parsing/weird_array.pass.kxi",
    ]

    for fname in list_of_files:
        lexer = lp.BigLexer()
        parser = lp.BigParser()

        file = open(fname, 'r')
        # print(f"{fname} starting:")
        try:
            compunit = parser.parse(lexer.tokenize(file.read()))
            tablevisitor = v.SymbolTableVisitor()
            compunit.accept(tablevisitor)
            if "fail" in fname:
                print(f"fail file {fname} actually passed :/")
        except Exception as e:
            if "pass" in fname:
                print(f"pass file {fname} actually failed :/")
                print(e)


if __name__ == "__main__":
    main()