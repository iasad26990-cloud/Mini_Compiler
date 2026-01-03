# code_generator.py
class CodeGenerator:
    def __init__(self):
        # Counter for temporary variables (e.g., t1, t2)
        self.temp_count = 0
        # List to store intermediate representation (IR) code
        self.ir_code = []
        # List to store equivalent Python code for testing/execution
        self.python_code = []
    def new_temp(self):
        # Generate a new temporary variable name (like t1, t2, ...)
        self.temp_count += 1
        return f"t{self.temp_count}"
    def emit(self, op, arg1="", arg2="", result=""):
        # Emit one line of intermediate code based on operation type
        if op == "=":
            # Simple assignment
            line = f"{result} = {arg1}"
        elif op == "RETURN":
            # Return statement
            line = f"RETURN {arg1}"
        else:
            # Arithmetic or logical operation
            line = f"{result} = {arg1} {op} {arg2}"
        # Add the generated line to IR code list
        self.ir_code.append(line)
    def emit_python(self, line):
        # Add a Python line to the Python output list
        self.python_code.append(line)
    def generate_assignment(self, lhs, rhs):
        # Generate IR and Python code for an assignment statement
        self.emit("=", rhs, "", lhs)
        self.emit_python(f"{lhs} = {rhs}")
    def generate_expression(self, op, arg1, arg2):
        # Generate IR code for an expression like a + b
        temp = self.new_temp()
        self.emit(op, arg1, arg2, temp)
        return temp  # Return temp variable holding the result
    def generate_if(self, condition, body_lines):
        # Generate IR and Python code for an if-statement
        self.emit_python(f"if {condition}:")
        for line in body_lines:
            # Indent inner lines in Python output
            self.emit_python(f"    {line}")
        # Add placeholder IR jump (for demonstration)
        self.ir_code.append(f"IF {condition} GOTO LABEL_TRUE")
    def generate_return(self, value=None):
        # Generate IR and Python code for return statement
        self.emit("RETURN", value or "", "", "")
        self.emit_python(f"return {value or ''}")
    def write_output(self):
        # Write intermediate representation (IR) to a text file
        with open("ir.txt", "w") as f:
            f.write("\n".join(self.ir_code))
        # Write generated Python equivalent code to a file
        with open("output.py", "w") as f:
            f.write("def main():\n")
            for line in self.python_code:
                f.write(f"    {line}\n")
            f.write("\nmain()\n")
        # Notify user that code generation is done
        print("Generated ir.txt and output.py")