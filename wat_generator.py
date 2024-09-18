import my_parser
import ply.yacc as yacc
from ply import lex
from pprint import pprint
import AST_catcher


class MyLanguageCompiler:
    def __init__(self):
        self.wat_code = []

    def compile_to_wat(self, source_code):
        # Parse source code into an abstract syntax tree (AST)
        ast = self.parse_source_code(source_code)

        # Translate AST to WAT
        self.translate_ast_to_wat(ast)
        pass

    def parse_source_code(self, source_code):
        parser = my_parser.parser
        ast = parser.parse(source_code)

        return ast



    def translate_ast_to_wat(self, ast):
        catcher=AST_catcher.NodeAnalyzer()
        catcher.analyze(ast)

        self.wat_code = catcher.wat_code
        
            

    def output_wat(self, filename):
        # Convert the list of WAT code lines to a single string with newline characters
        wat_code_str = '\n'.join(self.wat_code)
        
        # Write the WAT code string to the file
        with open(filename, "w") as f:
            f.write(wat_code_str)



if __name__ == "__main__":
    # Create compiler instance
    compiler = MyLanguageCompiler()

    # Compile source code to WAT
    source_code = open("test_cases/test_ceasar.zeva", "r").read()
    compiler.compile_to_wat(source_code)

    # Output WAT code to file
    compiler.output_wat("output.wat")
