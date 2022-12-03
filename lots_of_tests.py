import astclasses as ast
import semanticvisitors as v
import starting_lexer_parser as lp

def main():
    list_of_files = [
        "kxi_test/unit/lexical/json.fail.kxi",
        "kxi_test/unit/lexical/no_token.fail.kxi",
        "kxi_test/unit/parsing/class_name.fail.kxi",
        "kxi_test/unit/parsing/detached_else.fail.kxi",
        "kxi_test/unit/parsing/dup_cases.fail.kxi",
        "kxi_test/unit/parsing/empty.fail.kxi",
        "kxi_test/unit/parsing/keyword_assn.fail.kxi",
        "kxi_test/unit/parsing/keyword_decl.fail.kxi",
        "kxi_test/unit/parsing/keyword_decl.pass.kxi",
        "kxi_test/unit/parsing/operator_precedence.pass.kxi",
        "kxi_test/unit/parsing/pythondict.fail.kxi",
        "kxi_test/unit/semantics/weird.pass.kxi",
        "kxi_test/unit/semantics/constructors/constructor_naming.fail.kxi",
        "kxi_test/unit/semantics/constructors/multiple_constructors.fail.kxi",
        "kxi_test/unit/semantics/constructors/return.fail.kxi",
        "kxi_test/unit/semantics/constructors/return_nested.fail.kxi",
        "kxi_test/unit/semantics/constructors/return_really_nested.fail.kxi",
        "kxi_test/unit/semantics/double_decl/class_and_var.pass.kxi",
        "kxi_test/unit/semantics/double_decl/class_as_var.pass.kxi",
        "kxi_test/unit/semantics/double_decl/class_constructor_parameters.fail.kxi",
        "kxi_test/unit/semantics/double_decl/class_constructor_parameters.pass.kxi",
        "kxi_test/unit/semantics/double_decl/class_constructor_param_body.fail.kxi",
        "kxi_test/unit/semantics/double_decl/class_function_params.fail.kxi",
        "kxi_test/unit/semantics/double_decl/class_function_params_body.fail.kxi",
        "kxi_test/unit/semantics/double_decl/dup_class.fail.kxi",
        "kxi_test/unit/semantics/double_decl/dup_member.fail.kxi",
        "kxi_test/unit/semantics/double_decl/dup_member_funcs.fail.kxi",
        "kxi_test/unit/semantics/double_decl/dup_member_mix.fail.kxi",
        "kxi_test/unit/semantics/double_decl/main_block.fail.kxi",
        "kxi_test/unit/semantics/double_decl/main_block.pass.kxi",
        "kxi_test/unit/semantics/func/call_on_prim.fail.kxi",
        "kxi_test/unit/semantics/func_args/constructor.pass.kxi",
        "kxi_test/unit/semantics/func_args/constructor_count.fail.kxi",
        "kxi_test/unit/semantics/func_args/constructor_type.fail.kxi",
        "kxi_test/unit/semantics/func_args/func_arg_count.fail.kxi",
        "kxi_test/unit/semantics/func_args/func_arg_type.fail.kxi",
        "kxi_test/unit/semantics/func_args/func_call.pass.kxi",
        "kxi_test/unit/semantics/func_args/main.fail.kxi",
        "kxi_test/unit/semantics/func_args/main2.fail.kxi",
        "kxi_test/unit/semantics/func_args/no_constructor.fail.kxi",
        "kxi_test/unit/semantics/func_args/no_constructor.pass.kxi",
        "kxi_test/unit/semantics/invalid_break/break.fail.kxi",
        "kxi_test/unit/semantics/invalid_break/break.pass.kxi",
        "kxi_test/unit/semantics/invalid_index/normal_array.pass.kxi",
        "kxi_test/unit/semantics/invalid_index/not_an_array.fail.kxi",
        "kxi_test/unit/semantics/invalid_index/this_stmt_index.fail.kxi",
        "kxi_test/unit/semantics/invalid_this/this_as_func.fail.kxi",
        "kxi_test/unit/semantics/lvalues/cin.invalid.fail.kxi",
        "kxi_test/unit/semantics/lvalues/cin.parse.fail.kxi",
        "kxi_test/unit/semantics/lvalues/cin.pass.kxi",
        "kxi_test/unit/semantics/lvalues/func_lvalue_assn.fail.kxi",
        "kxi_test/unit/semantics/lvalues/func_lvalue_assn_chain.fail.kxi",
        "kxi_test/unit/semantics/lvalues/func_lvalue_assn_chain.pass.kxi",
        "kxi_test/unit/semantics/lvalues/func_lvalue_assn_nested.fail.kxi",
        "kxi_test/unit/semantics/lvalues/new_lvalue_assn.fail.kxi",
        "kxi_test/unit/semantics/lvalues/new_lvalue_assn_nested.fail.kxi",
        "kxi_test/unit/semantics/lvalues/unusableLVals.fail.kxi",
        "kxi_test/unit/semantics/lvalues/basic_lvalue.pass.kxi",
        "kxi_test/unit/semantics/modifiers/private_func.fail.kxi",
        "kxi_test/unit/semantics/modifiers/private_func_inside.pass.kxi",
        "kxi_test/unit/semantics/modifiers/private_member.fail.kxi",
        "kxi_test/unit/semantics/modifiers/private_member.pass.kxi",
        "kxi_test/unit/semantics/modifiers/public_member.pass.kxi",
        # ...,
        # "kxi_test/unit/semantics/undecl_identifier/func_invoke_main_block.fail.kxi",
        # "kxi_test/unit/semantics/undecl_identifier/func_invoke_main_block.pass.kxi",
        # "kxi_test/unit/semantics/undecl_identifier/main_block.2.pass.kxi",
        # "kxi_test/unit/semantics/undecl_identifier/main_block.fail.kxi",
        # "kxi_test/unit/semantics/undecl_identifier/main_block.pass.kxi",
        # "kxi_test/unit/semantics/undecl_identifier/undecl_function.fail.kxi",
        # "kxi_test/unit/semantics/undecl_identifier/undecl_function_no_class.fail.kxi",
        # "kxi_test/unit/semantics/undecl_identifier/undeclared.fail.kxi",

    ]

    """
    $files = Get-ChildItem -Recurse 
    foreach ($file in $files){
        $file.FullName
    }
    
    with a little bit of fancy text editing...
    
    "kxi_test/unit/andrew/Lexical/lexical_basicwithstring_fail.kxi",
    "kxi_test/unit/andrew/Lexical/lexical_basic_pass.kxi",
    "kxi_test/unit/andrew/Lexical/lexical_textfile_fail.kxi",
    "kxi_test/unit/andrew/Other/assignkeyword.fail.kxi",
    "kxi_test/unit/andrew/Other/classchain.pass.kxi",
    "kxi_test/unit/andrew/Other/doubly_fail.kxi",
    "kxi_test/unit/andrew/Other/doubly_pass.kxi",
    "kxi_test/unit/andrew/Other/lexer_fail.kxi",
    "kxi_test/unit/andrew/Other/lexer_pass.kxi",
    "kxi_test/unit/andrew/Other/other_complex-class-methods_pass.kxi",
    "kxi_test/unit/andrew/Other/other_complex-class_pass.kxi",
    "kxi_test/unit/andrew/Other/other_massive-dotop_pass.kxi",
    "kxi_test/unit/andrew/Other/other_simple-class-if-else_pass.kxi",
    "kxi_test/unit/andrew/Other/other_simple-class_pass.kxi",
    "kxi_test/unit/andrew/Other/other_switch-case-if-else_pass.kxi",
    "kxi_test/unit/andrew/Other/parser_fail.kxi",
    "kxi_test/unit/andrew/Other/parser_pass.kxi",
    "kxi_test/unit/andrew/Other/syntax_fail.kxi",
    "kxi_test/unit/andrew/Other/syntax_pass.kxi",
    "kxi_test/unit/andrew/Other/type_fail.kxi",
    "kxi_test/unit/andrew/Other/type_pass.kxi",
    "kxi_test/unit/andrew/Other/undeclared.txt",
    "kxi_test/unit/andrew/Other/undeclared_fail.kxi",
    "kxi_test/unit/andrew/Other/undeclared_pass.kxi",
    "kxi_test/unit/andrew/Other/unusable_fail.kxi",
    "kxi_test/unit/andrew/Other/unusable_pass.kxi",
    "kxi_test/unit/andrew/Semantic/DoublyDeclared/doubly_decl-before-scope-decl-in-scope_fail.kxi",
    "kxi_test/unit/andrew/Semantic/DoublyDeclared/doubly_decl-class-and-decl-int_fail.kxi",
    "kxi_test/unit/andrew/Semantic/DoublyDeclared/doubly_decl-in-scope-after-decl-out-scope_pass.kxi",
    "kxi_test/unit/andrew/Semantic/DoublyDeclared/doubly_decl-method-and-decl-datamem_fail.kxi",
    "kxi_test/unit/andrew/Semantic/DoublyDeclared/doubly_decl-method-and-decl-int-main_pass.kxi",
    "kxi_test/unit/andrew/Semantic/TypeError/type_class-constr-param_fail.kxi",
    "kxi_test/unit/andrew/Semantic/TypeError/type_class-constr-param_pass.kxi",
    "kxi_test/unit/andrew/Semantic/TypeError/type_dotop-datamem-arg_fail.kxi",
    "kxi_test/unit/andrew/Semantic/TypeError/type_dotop-datamem_pass.kxi",
    "kxi_test/unit/andrew/Semantic/TypeError/type_dotop-method-arg-array_pass.kxi",
    "kxi_test/unit/andrew/Semantic/TypeError/type_dotop-method-array_fail.kxi",
    "kxi_test/unit/andrew/Semantic/TypeError/type_dotop-method_pass.kxi",
    "kxi_test/unit/andrew/Semantic/Undeclared/undeclared_declare-datamem-no-this_fail.kxi",
    "kxi_test/unit/andrew/Semantic/Undeclared/undeclared_declare-datamem-use-main_pass.kxi",
    "kxi_test/unit/andrew/Semantic/Undeclared/undeclared_declare-datamem-use-no-dec-main_fail.kxi",
    "kxi_test/unit/andrew/Semantic/Undeclared/undeclared_declare-datamem-use-this_pass.kxi",
    "kxi_test/unit/andrew/Semantic/Undeclared/undeclared_declare-in-used-out-after_fail.kxi",
    "kxi_test/unit/andrew/Semantic/Undeclared/undeclared_declare-out-used-in_pass.kxi",
    "kxi_test/unit/andrew/Semantic/Unusable/FileNames.txt",
    "kxi_test/unit/andrew/Semantic/Unusable/unusable_correct-func_pass.kxi",
    "kxi_test/unit/andrew/Semantic/Unusable/unusable_function-assignment_fail.kxi",
    "kxi_test/unit/andrew/Semantic/Unusable/unusable_new_fail.kxi",
    "kxi_test/unit/andrew/Syntax/syntax_basic_pass.kxi",
    "kxi_test/unit/andrew/Syntax/syntax_complex_pass.kxi",
    "kxi_test/unit/andrew/Syntax/syntax_missing-kxi_fail.kxi",
    "kxi_test/unit/lexical/json.fail.kxi",
    "kxi_test/unit/lexical/no_token.fail.kxi",
    "kxi_test/unit/parsing/class_name.fail.kxi",
    "kxi_test/unit/parsing/detached_else.fail.kxi",
    "kxi_test/unit/parsing/dup_cases.fail.kxi",
    "kxi_test/unit/parsing/empty.fail.kxi",
    "kxi_test/unit/parsing/keyword_assn.fail.kxi",
    "kxi_test/unit/parsing/keyword_decl.fail.kxi",
    "kxi_test/unit/parsing/keyword_decl.pass.kxi",
    "kxi_test/unit/parsing/operator_precedence.pass.kxi",
    "kxi_test/unit/parsing/pythondict.fail.kxi",
    
    
    
    
    
    "kxi_test/unit/semantics/types/array_idx.fail.kxi",
    "kxi_test/unit/semantics/types/array_idx.pass.kxi",
    "kxi_test/unit/semantics/types/array_init.fail.kxi",
    "kxi_test/unit/semantics/types/assn.fail.kxi",
    "kxi_test/unit/semantics/types/assn_array.fail.kxi",
    "kxi_test/unit/semantics/types/assn_array.pass.kxi",
    "kxi_test/unit/semantics/types/assn_array_member.fail.kxi",
    "kxi_test/unit/semantics/types/assn_array_member.pass.kxi",
    "kxi_test/unit/semantics/types/binary_bool.fail.kxi",
    "kxi_test/unit/semantics/types/binary_bool.pass.kxi",
    "kxi_test/unit/semantics/types/binary_math.fail.kxi",
    "kxi_test/unit/semantics/types/binary_math.pass.kxi",
    "kxi_test/unit/semantics/types/bool_if_cond.fail.kxi",
    "kxi_test/unit/semantics/types/bool_if_cond.pass.kxi",
    "kxi_test/unit/semantics/types/call_array_member.fail.kxi",
    "kxi_test/unit/semantics/types/func_assn.fail.kxi",
    "kxi_test/unit/semantics/types/func_return.fail.kxi",
    "kxi_test/unit/semantics/types/func_return.pass.kxi",
    "kxi_test/unit/semantics/types/func_return_array.pass.kxi",
    "kxi_test/unit/semantics/types/func_return_nested.fail.kxi",
    "kxi_test/unit/semantics/types/func_return_nested.pass.kxi",
    "kxi_test/unit/semantics/types/int_assn_char.fail.kxi",
    "kxi_test/unit/semantics/types/main_return.fail.kxi",
    "kxi_test/unit/semantics/types/main_return.pass.kxi",
    "kxi_test/unit/semantics/types/maths.fail.kxi",
    "kxi_test/unit/semantics/types/math_returns.fail.kxi",
    "kxi_test/unit/semantics/types/math_returns.pass.kxi",
    "kxi_test/unit/semantics/types/null_assn.pass.kxi",
    "kxi_test/unit/semantics/types/shadowing_class.pass.kxi",
    "kxi_test/unit/semantics/types/this_assn.fail.kxi",
    "kxi_test/unit/semantics/types/too_many_indices.fail.kxi",
    "kxi_test/unit/semantics/types/unary_math.fail.kxi",
    "kxi_test/unit/semantics/types/unary_math.pass.kxi",
    "kxi_test/unit/semantics/types/unary_math2.fail.kxi",
    "kxi_test/unit/semantics/types/var_decl.fail.kxi",
    "kxi_test/unit/semantics/types/void_declaration.fail.kxi",
    "kxi_test/unit/semantics/undecl_identifier/func_invoke_main_block.fail.kxi",
    "kxi_test/unit/semantics/undecl_identifier/func_invoke_main_block.pass.kxi",
    "kxi_test/unit/semantics/undecl_identifier/main_block.2.pass.kxi",
    "kxi_test/unit/semantics/undecl_identifier/main_block.fail.kxi",
    "kxi_test/unit/semantics/undecl_identifier/main_block.pass.kxi",
    "kxi_test/unit/semantics/undecl_identifier/undeclared.fail.kxi",
    "kxi_test/unit/semantics/undecl_identifier/undecl_function.fail.kxi",
    "kxi_test/unit/semantics/undecl_identifier/undecl_function_no_class.fail.kxi",
    "kxi_test/unit/semantics/undecl_type/func_param.fail.kxi",
    "kxi_test/unit/semantics/undecl_type/new.pass.kxi",
    "kxi_test/unit/semantics/undecl_type/return_type.fail.kxi",
    "kxi_test/unit/semantics/unsupported/multi_dim_arrays.fail.kxi",
    "kxi_test/unit/transform/func_call_rewrite.kxi",
    """

    for fname in list_of_files:
        lexer = lp.BigLexer()
        parser = lp.BigParser()

        file = open(fname, 'r')
        # print(f"{fname} starting:")
        try:
            compunit = parser.parse(lexer.tokenize(file.read()))
            tablevisitor = v.SymbolTableVisitor()
            compunit.accept(tablevisitor)
            if tablevisitor.isErrorState:
                # print(tablevisitor.error_messages)
                raise Exception()
            assignmentvisitor = v.AssignmentVisitor(tablevisitor.sym_table)
            compunit.accept(assignmentvisitor)
            if assignmentvisitor.isErrorState:
                # print(assignmentvisitor.error_messages)
                raise Exception()
            breakvisitor = v.BreakVisitor()
            compunit.accept(breakvisitor)
            if breakvisitor.isErrorState:
                # print(breakvisitor.error_messages)
                raise Exception()
            cinvisitor = v.CinVisitor(tablevisitor.sym_table)
            compunit.accept(cinvisitor)
            if cinvisitor.isErrorState:
                # print(cinvisitor.error_messages)
                raise Exception()

            if "fail" in fname:
                print(f"fail file {fname} actually passed :/")
        except Exception as e:
            if "pass" in fname:
                print(f"pass file {fname} actually failed :/", e)


if __name__ == "__main__":
    main()