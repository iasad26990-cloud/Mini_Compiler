import ply.lex as lex
# Keywords
keywords = {
    'int':'INT', 'float':'FLOAT', 'char':'CHAR',
    'if':'IF', 'else':'ELSE', 'for':'FOR', 'while':'WHILE',
    'return':'RETURN', 'break':'BREAK', 'continue':'CONTINUE'
}
# Token list
tokens = [
    'IDENTIFIER', 'INTEGER_LITERAL', 'FLOAT_LITERAL',
    'CHAR_LITERAL', 'STRING_LITERAL', 'OPERATOR', 'SYMBOL'
] + list(keywords.values())
# Ignored characters
t_ignore = ' \t'
# Operators and symbols
t_OPERATOR = r'\+\+|--|\+=|-=|\*=|/=|==|!=|<=|>=|&&|\|\||[+\-*/%!=<>]'
t_SYMBOL = r'[\(\)\{\}\[\],;]'
# Token definitions
def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')  # Check for keywords
    return t
def t_FLOAT_LITERAL(t):
    r'\d*\.\d+'
    return t
def t_INTEGER_LITERAL(t):
    r'\d+'
    return t
def t_CHAR_LITERAL(t):
    r"'[^']'"
    return t
def t_STRING_LITERAL(t):
    r'"([^"\n]|(\\"))*"'
    return t
# Comments
def t_COMMENT_SINGLELINE(t):
    r'//.*'   # Ignore single-line comments
    pass
def t_COMMENT_MULTILINE(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')  # Ignore multi-line comments
    pass 
# Unterminated string literal detection
def t_UNTERMINATED_STRING(t):
    r'"[^"\n]*$'
    print(f"Lexical Error (line {t.lineno}): Unterminated string literal")
    t.lexer.skip(len(t.value))
# Unclosed multi-line comment detection
def t_UNCLOSED_COMMENT(t):
    r'/\*[\s\S]*$'
    print(f"Lexical Error (line {t.lineno}): Unclosed multi-line comment")
    t.lexer.skip(len(t.value))
# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
# Error handling
def t_error(t):
    print(f"Lexical Error (line {t.lineno}): Illegal character '{t.value[0]}'")
    t.lexer.skip(1)
# Helper function for column to calculate token position in the code
def find_column(lexpos, code):
    last_cr = code.rfind('\n', 0, lexpos)
    if last_cr < 0:
        last_cr = -1
    return lexpos - last_cr
# Build lexer
lexer = lex.lex()
#For Recognizing Pattern
import re
# Define tokenize function to compile
def tokenize(code):
    """
    Tokenize the input code.
    Returns:
        tokens_list: list of (type, value, line, column)
        lexical_errors: list of lexical error messages
        clean_code: input code with comments removed
    """
    # Remove comments to generate clean source code
    clean_code = re.sub(r"//.*", "", code)                   # single-line comments
    clean_code = re.sub(r"/\*[\s\S]*?\*/", "", clean_code)  # multi-line comments
    lexer.input(clean_code)
    tokens_list = []
    lexical_errors = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        col = find_column(tok.lexpos, clean_code)
        tokens_list.append((tok.type, tok.value, tok.lineno, col))
    # Redefine t_error temporarily to collect errors instead of printing
    def t_error_collect(t):
        lexical_errors.append(
            f"Lexical Error (line {t.lineno}, col {find_column(t.lexpos, clean_code)}): Illegal character '{t.value[0]}'"
        )
        t.lexer.skip(1)
    lexer.errorfunc = t_error_collect  # override default error function
    return tokens_list, lexical_errors, clean_code
#example for testing
if __name__ == "__main__":
    code = """
    int counter = 0;
    float pi = 3.14;
    // This is a comment
    """
    for t in tokenize(code):
        print(t)
# dictionary for token pattern
token_patterns = {
    'IDENTIFIER': r'[A-Za-z_][A-Za-z0-9_]*',
    'INTEGER_LITERAL': r'\d+',
    'FLOAT_LITERAL': r'\d*\.\d+',
    'CHAR_LITERAL': r"'[^']'",
    'STRING_LITERAL': r'"([^"\n]|(\\"))*"',
    'OPERATOR': r'\+\+|--|\+=|-=|\*=|/=|==|!=|<=|>=|&&|\|\||[+\-*/%!=<>]',
    'SYMBOL': r'[\(\)\{\}\[\],;]',
}