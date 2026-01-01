from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator
class Parser:
    def __init__(self, tokens):
        # Initialize parser with a list of tokens
        # tokens: list of tuples like (line_number, token_type, token_value)
        self.tokens = tokens
        self.pos = 0  # current index in the token list
        self.current_token = self.tokens[self.pos] if self.tokens else None  # current token being processed
        self.semantic = SemanticAnalyzer()  # create semantic analyzer (for declarations, type checks)
        self.cg = CodeGenerator()           # create code generator (for output code generation)
    def advance(self):
        # Move to the next token
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]  # update current token
        else:
            self.current_token = None  # reached end of token list
    def match(self, expected_value=None, expected_type=None):
        # Check if current token matches expected value or type
        if not self.current_token:
            raise Exception("Unexpected end of file")
        _, token_type, token_value = self.current_token
        # If both value and type are given, and none matches → error
        if (expected_value and token_value != expected_value) and (expected_type and token_type != expected_type):
            raise Exception(f"Syntax Error: Expected {expected_value or expected_type}, got {token_value}")
        # If matched, move to next token
        self.advance()
    def parse(self):
        # Entry point for parsing
        # Parses the program and triggers semantic + code generation
        self.program()
        self.semantic.write_symbol_table()  # save variable info
        self.cg.write_output()              # save generated code
        print("✅ Compilation successful.")
    def program(self):
        # Grammar: program → int main() { statement_list }
        # Parse the main function structure
        self.match(expected_value="int", expected_type="KEYWORD")
        self.match(expected_type="IDENTIFIER")        # typically 'main'
        self.match(expected_value="(", expected_type="DELIMITER")
        self.match(expected_value=")", expected_type="DELIMITER")
        self.match(expected_value="{", expected_type="DELIMITER")
        self.statement_list()                         # parse all statements inside main
        self.match(expected_value="}", expected_type="DELIMITER")
    def statement_list(self):
        # Grammar: statement_list → { statement }
        # Parse multiple statements until a closing brace '}' appears
        while self.current_token and self.current_token[2] != "}":
            self.statement()
    def statement(self):
        # Decide which statement rule to use based on current token
        _, ttype, value = self.current_token

        if ttype == "KEYWORD" and value in ("int", "float"):
            self.declaration()     # variable declaration
        elif ttype == "IDENTIFIER":
            self.assignment()      # variable assignment
        elif ttype == "KEYWORD" and value == "if":
            self.if_stmt()         # if-statement
        elif ttype == "KEYWORD" and value == "return":
            self.return_stmt()     # return-statement
        else:
            raise Exception(f"Syntax Error: Unexpected token {value}")
    def declaration(self):
        # Grammar: declaration → (int|float) IDENTIFIER [= value] ;
        # Declare variable and optionally assign value
        _, _, vtype = self.current_token
        self.match(expected_type="KEYWORD")           # match type keyword (int/float)
        _, _, name = self.current_token
        self.match(expected_type="IDENTIFIER")        # match variable name
        self.semantic.declare(name, vtype)            # add to symbol table
        # Optional assignment during declaration
        if self.current_token and self.current_token[2] == "=":
            self.match(expected_value="=")
            _, _, rhs = self.current_token
            self.match()                              # consume value token
            self.cg.generate_assignment(name, rhs)    # generate assignment code
        self.match(expected_value=";", expected_type="DELIMITER")  # statement must end with semicolon
    def assignment(self):
        # Grammar: assignment → IDENTIFIER = value ;
        # Assign value to an already declared variable
        _, _, name = self.current_token
        self.semantic.assign(name)                    # check if variable declared
        self.match(expected_type="IDENTIFIER")        # match variable name
        self.match(expected_value="=")                # match '='
        _, _, rhs = self.current_token                # get right-hand-side value
        self.match()                                  # consume RHS token
        self.cg.generate_assignment(name, rhs)        # generate assignment code
        self.match(expected_value=";", expected_type="DELIMITER")  # statement must end with semicolon
    def if_stmt(self):
        # Grammar: if_stmt → if ( condition ) { statement_list }
        # Parse an if statement
        self.match(expected_value="if")
        self.match(expected_value="(")
        _, _, cond = self.current_token               # get condition expression
        self.match()                                  # consume condition token
        self.match(expected_value=")")
        self.match(expected_value="{")
        self.cg.generate_if(cond, [])                 # generate code for if-block
        self.statement_list()                         # parse inner statements
        self.match(expected_value="}")                # match closing brace
    def return_stmt(self):
        # Grammar: return_stmt → return value ;
        # Parse a return statement
        self.match(expected_value="return")
        _, _, val = self.current_token                # get return value
        self.match()                                  # consume return value
        self.cg.generate_return(val)                  # generate return code
        self.match(expected_value=";", expected_type="DELIMITER")  # must end with semicolon