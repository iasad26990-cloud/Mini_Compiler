# semantic_analyzer.py
class SemanticAnalyzer:
    def __init__(self):
        """
        Initialize an empty symbol table.
        Each entry stores:
            - type: variable type (int, float, char, etc.)
            - value: assigned value (optional)
            - declared_at: line number where declared
        """
        self.symbols = {}
    def declare(self, name, vtype, lineno):
        """
        Declare a variable with name, type, and line number.
        Raises an error if variable is already declared.
        """
        if name in self.symbols:
            raise Exception(f"Semantic Error (line {lineno}): Variable '{name}' already declared.")
        self.symbols[name] = {
            'type': vtype,
            'value': None,
            'declared_at': lineno
        }
    def assign(self, name, value=None, vtype=None, lineno=None):
        """
        Assign a value to a variable.
        Raises an error if variable not declared or type mismatch.
        """
        if name not in self.symbols:
            raise Exception(f"Semantic Error (line {lineno}): Variable '{name}' not declared.")
        if vtype and self.symbols[name]['type'] != vtype:
            raise Exception(f"Semantic Error (line {lineno}): Type mismatch for variable '{name}'. "
                            f"Expected '{self.symbols[name]['type']}', got '{vtype}'.")
        if value is not None:
            self.symbols[name]['value'] = value
    def lookup(self, name, lineno=None):
        """
        Return variable info if declared, else raise error.
        """
        if name not in self.symbols:
            raise Exception(f"Semantic Error (line {lineno}): Variable '{name}' not declared.")
        return self.symbols[name]
    def write_symbol_table(self, filename="symbol_table.txt"):
        """
        Write the symbol table to a file in a readable format.
        """
        with open(filename, "w") as f:
            f.write("Name\tType\tValue\tDeclaredAt\n")
            for name, info in self.symbols.items():
                f.write(f"{name}\t{info['type']}\t{info.get('value', '-')}\t{info.get('declared_at', '-')}\n")
# Optional test to demonstrate functionality
if __name__ == "__main__":
    analyzer = SemanticAnalyzer()
    try:
        analyzer.declare("x", "int", 1)       # Declare variable x of type int at line 1
        analyzer.declare("y", "float", 2)     # Declare variable y of type float at line 2
        analyzer.assign("x", 10, "int", 3)    # Assign value 10 to x at line 3
        analyzer.assign("y", 3.14, "float", 4) # Assign value 3.14 to y at line 4
        analyzer.lookup("x")                  # Check info of variable x
        analyzer.write_symbol_table()         # Save the symbol table to a file
        print("Semantic analysis completed successfully!")
    except Exception as e:
        print(e)