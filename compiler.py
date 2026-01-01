from collections import Counter
from lexer import tokenize, token_patterns
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator
from optimizer import CodeOptimizer
from register_allocator import RegisterAllocator


# File paths
input_file = "test.mini"
tokens_file = "tokens.txt"
symbol_table_file = "symbol_table.txt"
reg_file = "reg.txt"
semantic_file = "semantic_analysis.txt"
ir_file = "ir.txt"
python_file = "output.py"
lexical_errors_file = "lexical_errors.txt"
clean_source_file = "clean_source.mini"
token_stats_file = "token_stats.txt"

# Read input source code
with open(input_file, 'r') as f:
    code = f.read()

# Tokenize code (Task 5)
tokens_list, lexical_errors, clean_code = tokenize(code)

# Save cleaned source (without comments)
with open(clean_source_file, "w") as f:
    f.write(clean_code)

# Save lexical errors
with open(lexical_errors_file, "w") as f:
    if lexical_errors:
        f.write("Lexical Errors:\n")
        for err in lexical_errors:
            f.write(err + "\n")
    else:
        f.write("No lexical errors detected.\n")

# Write token stream & build symbol table
symbol_table = {}
with open(tokens_file, 'w') as tf:
    for tok_type, tok_value, tok_line, tok_col in tokens_list:
        tf.write(f"<{tok_line}, {tok_col}> <{tok_type}, {tok_value}>\n")
        # Update symbol table for identifiers/literals
        if tok_type in ['IDENTIFIER','INTEGER_LITERAL','FLOAT_LITERAL','CHAR_LITERAL','STRING_LITERAL']:
            if tok_value not in symbol_table:
                category = 'variable' if tok_type == 'IDENTIFIER' else 'literal'
                symbol_table[tok_value] = {
                    'type': tok_type.lower().replace('_literal',''),
                    'category': category,
                    'value': tok_value if category == 'literal' else '—',
                    'line': tok_line,
                    'column': tok_col
                }

# --- ✅ TOKEN STATISTICS SECTION ---
# Count tokens by type
counts = Counter(tok_type for tok_type, _, _, _ in tokens_list)

# Prepare table formatting
header_token = "Token Type"
header_count = "Count"
line_width = 30  # adjust for neatness
# write token stats to file
with open(token_stats_file, "w") as f:
    f.write("+" + "-" * (line_width - 1) + "+\n")
    f.write(f"| {header_token.ljust(20)} | {header_count.rjust(5)} |\n")
    f.write("+" + "-" * (line_width - 1) + "+\n")
    for token_type, count in counts.items():
        f.write(f"| {token_type.ljust(20)} | {str(count).rjust(5)} |\n")
    f.write("+" + "-" * (line_width - 1) + "+\n")

# --- SEMANTIC ANALYSIS ---
analyzer = SemanticAnalyzer()
semantic_errors = []

for i, (tok_type, tok_value, tok_line, tok_col) in enumerate(tokens_list):
    # Variable declaration (int, float, char)
    if tok_type in ['INT', 'FLOAT', 'CHAR']:
        current_type = tok_type.lower()
        if i + 1 < len(tokens_list):
            next_tok_type, next_tok_value, next_tok_line, next_tok_col = tokens_list[i + 1]
            if next_tok_type == 'IDENTIFIER':
                try:
                    analyzer.declare(next_tok_value, current_type, next_tok_line)
                except Exception as e:
                    semantic_errors.append(f"Line {next_tok_line}: {e}")
        continue

    # Variable assignment
    if tok_type == 'OPERATOR' and tok_value == '=':
        if i - 1 >= 0 and i + 1 < len(tokens_list):
            var_tok_type, var_name, var_line, var_col = tokens_list[i - 1]
            val_tok_type, val_tok_value, val_line, val_col = tokens_list[i + 1]
            # Determine value type
            if val_tok_type == 'INTEGER_LITERAL':
                val_type = 'int'
            elif val_tok_type == 'FLOAT_LITERAL':
                val_type = 'float'
            elif val_tok_type == 'CHAR_LITERAL':
                val_type = 'char'
            elif val_tok_type == 'STRING_LITERAL':
                val_type = 'string'
            else:
                val_type = None
            try:
                analyzer.assign(var_name, value=val_tok_value, vtype=val_type, lineno=var_line)
            except Exception as e:
                semantic_errors.append(f"Line {var_line}: {e}")

# Save semantic errors
with open(semantic_file, 'w') as sf:
    if semantic_errors:
        sf.write("Semantic Errors:\n")
        for err in semantic_errors:
            sf.write(err + "\n")
    else:
        sf.write("No semantic errors detected.\n")

# Write symbol table
analyzer.write_symbol_table(symbol_table_file)

# Write regex patterns with examples (aligned columns)
examples = {
    "IDENTIFIER": "counter, _var2",
    "INTEGER_LITERAL": "123",
    "FLOAT_LITERAL": "3.14",
    "CHAR_LITERAL": "'a', 'Z'",
    "STRING_LITERAL": '"hello", "world"',
    "OPERATOR": "++, --, =, +, -",
    "SYMBOL": ";, (, {, }",
    "KEYWORD": "int, float, char, if, else"
}

token_col_width = max(len(tok) for tok in token_patterns) + 2
pattern_col_width = max(len(pat) for pat in token_patterns.values()) + 2
example_col_width = max(len(ex) for ex in examples.values()) + 2

with open(reg_file, 'w') as rf:
    rf.write(f"{'Token Type'.ljust(token_col_width)}{'Regex / Pattern'.ljust(pattern_col_width)}{'Example'}\n")
    for tok_type, pattern in token_patterns.items():
        example = examples.get(tok_type, "")
        rf.write(f"{tok_type.ljust(token_col_width)}{pattern.ljust(pattern_col_width)}{example}\n")

# --- IR & CODE GENERATION ---
codegen = CodeGenerator()

for i, (tok_type, tok_value, tok_line, tok_col) in enumerate(tokens_list):
    # Handle assignment statements: IDENTIFIER = LITERAL/IDENTIFIER
    if tok_type == 'OPERATOR' and tok_value == '=':
        lhs_type, lhs, _, _ = tokens_list[i - 1]
        rhs_type, rhs, _, _ = tokens_list[i + 1]

        # Generate IR
        codegen.generate_assignment(lhs, rhs)





# Done
print("Lexical, semantic analysis, and code generation completed!")
print(f"Tokens saved to {tokens_file}")
print(f"Symbol table saved to {symbol_table_file}")
print(f"Semantic analysis saved to {semantic_file}")
print(f"Lexical errors saved to {lexical_errors_file}")
print(f"Clean source saved to {clean_source_file}")
print(f"Regular expressions saved to {reg_file}")
print(f"Token statistics saved to {token_stats_file}")
print(f"IR code saved to {ir_file} and Python code saved to {python_file}")
# Write IR and Python output
codegen.write_output()

# --- CODE OPTIMIZATION ---
optimizer = CodeOptimizer(
    ir_file="ir.txt",
    optimized_file="optimized_ir.txt"
)

optimizer.optimize()
optimizer.write_optimized_ir()

# --- REGISTER ALLOCATION ---
allocator = RegisterAllocator(
    ir_file="optimized_ir.txt",
    reg_file="reg_ir.txt"
)

allocator.allocate()
allocator.write_register_ir()
