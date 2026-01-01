# ir_generator.py
# A small IR generator for a simple compiler frontend.
# Produces three things:
#  - a list of IR instructions (self.ir_code)
#  - a simple Python-equivalent list (self.python_code) for testing
#  - writes ir.txt and output.py when write_output() is called

class IRGenerator:
    def __init__(self):
        # Counter for temporary variables (t1, t2, ...)
        self.temp_count = 0
        # Counter for labels (L1, L2, ...)
        self.label_count = 0
        # List of IR instructions (strings)
        self.ir_code = []
        # Optional Python "friendly" code list for quick execution/testing
        self.python_code = []
    
    # -----------------------
    # Utility generators
    # -----------------------
    def new_temp(self):
        # Return a new temporary variable name
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    def new_label(self):
        # Return a new unique label name
        self.label_count += 1
        return f"L{self.label_count}"
    
    # -----------------------
    # Emit functions
    # -----------------------
    def emit(self, instr):
        # Append a raw IR instruction (string) to the IR list
        self.ir_code.append(instr)
    
    def emit_python(self, line):
        # Append a Python-equivalent line
        self.python_code.append(line)
    
    # -----------------------
    # High-level IR helpers
    # -----------------------
    def generate_assignment(self, lhs, rhs):
        # Generate IR for simple assignment: lhs = rhs
        # rhs can be literal, variable, or temporary name
        self.emit(f"{lhs} = {rhs}")
        # Also add to python code for testing
        self.emit_python(f"{lhs} = {rhs}")
    
    def generate_binary(self, op, arg1, arg2):
        # Generate IR for a binary operation (arg1 op arg2)
        # Returns the temporary holding the result
        temp = self.new_temp()
        # Example IR: t1 = a + b
        self.emit(f"{temp} = {arg1} {op} {arg2}")
        # Python equivalent
        self.emit_python(f"{temp} = {arg1} {op} {arg2}")
        return temp
    
    def generate_unary(self, op, arg):
        # Generate IR for unary operation like -x or !x
        temp = self.new_temp()
        self.emit(f"{temp} = {op}{arg}")
        self.emit_python(f"{temp} = {op}{arg}")
        return temp
    
    def generate_label(self, label):
        # Emit a label in IR. Labels are written as "LABEL:" lines.
        self.emit(f"{label}:")
        # In python, we simulate labels with comments (no-op)
        self.emit_python(f"# label {label}")
    
    def generate_goto(self, label):
        # Unconditional jump
        self.emit(f"GOTO {label}")
        # Python cannot GOTO, so we add a comment placeholder
        self.emit_python(f"# GOTO {label}  (not directly supported in python)")
    
    def generate_conditional_jump(self, cond, true_label, false_label=None):
        """
        cond: a condition string (e.g., "x < 5" or "t1")
        true_label: label to jump to when condition true
        false_label: optional label for false branch (if provided emit explicit goto)
        """
        # IR style: IF cond GOTO L1
        self.emit(f"IF {cond} GOTO {true_label}")
        if false_label:
            # If we want an explicit false jump, we can emit it after the true branch label handling.
            # But commonly you'd do: IF cond GOTO Ltrue; GOTO Lfalse
            self.emit(f"GOTO {false_label}")
            # Python fallback (comments)
            self.emit_python(f"# IF {cond} GOTO {true_label} ELSE GOTO {false_label}")
        else:
            self.emit_python(f"# IF {cond} GOTO {true_label}")
    
    def generate_if(self, cond, true_body_lines, false_body_lines=None):
        """
        High-level helper to generate IR for an if-else:
            if cond:
                true_body_lines
            else:
                false_body_lines (optional)
        true_body_lines and false_body_lines are lists of IR strings or python lines.
        """
        L_true = self.new_label()
        L_end = self.new_label() if false_body_lines else L_true + "_end"
        
        # IF cond GOTO L_true
        if false_body_lines:
            L_false = self.new_label()
            self.generate_conditional_jump(cond, L_true, L_false)
        else:
            # If no explicit false label, we only jump to true and continue (typical structure differs)
            self.generate_conditional_jump(cond, L_true)
        
        # False branch (if present)
        if false_body_lines:
            # Emit false label and its body
            self.generate_label(L_false)
            for instr in false_body_lines:
                # Accept either IR-formatted string or (lhs, rhs) tuples; here we accept raw strings
                self.emit(instr)
                self.emit_python(f"# {instr}")
            # After false body, jump to end
            self.generate_goto(L_end)
        
        # True label and body
        self.generate_label(L_true)
        for instr in true_body_lines:
            self.emit(instr)
            self.emit_python(f"# {instr}")
        
        # End label if we used one
        if false_body_lines:
            self.generate_label(L_end)
    
    def generate_return(self, value=None):
        # Generate IR for return
        if value is not None and value != "":
            self.emit(f"RETURN {value}")
            self.emit_python(f"return {value}")
        else:
            self.emit("RETURN")
            self.emit_python("return")
    
    # -----------------------
    # Output helpers
    # -----------------------
    def write_ir_file(self, filename="ir.txt"):
        # Write the IR lines to a file
        with open(filename, "w") as f:
            for line in self.ir_code:
                f.write(line + "\n")
    
    def write_python_file(self, filename="output.py", top_lines=None):
        # Write the simple python_equivalent code to a file, wrapped in a main()
        with open(filename, "w") as f:
            if top_lines:
                for l in top_lines:
                    f.write(l + "\n")
            f.write("def main():\n")
            if self.python_code:
                for line in self.python_code:
                    # Indent python code lines (they may be comments or simple assignments)
                    f.write("    " + line + "\n")
            else:
                f.write("    pass\n")
            f.write("\nif __name__ == '__main__':\n")
            f.write("    main()\n")
    
    def write_output(self, ir_filename="ir.txt", py_filename="output.py"):
        # Convenience: write both files
        self.write_ir_file(ir_filename)
        self.write_python_file(py_filename)
        print(f"IR written to {ir_filename}, Python-equivalent written to {py_filename}")

# -----------------------
# Example usage (run as script)
# -----------------------
if __name__ == "__main__":
    ir = IRGenerator()
    
    # Example: Translate simple statements to IR
    # Simulate: a = 10
    ir.generate_assignment("a", "10")
    
    # Simulate: b = 20
    ir.generate_assignment("b", "20")
    
    # Simulate: t1 = a + b
    t = ir.generate_binary("+", "a", "b")  # returns t1
    
    # Simulate: x = t1 * 2
    t2 = ir.generate_binary("*", t, "2")
    ir.generate_assignment("x", t2)
    
    # Simulate: if x < 100 then y = 1 else y = 0
    cond = "x < 100"
    true_body = ["y = 1"]
    false_body = ["y = 0"]
    # Use high-level helper (this accepts raw IR instruction strings for bodies)
    ir.generate_if(cond, true_body, false_body)
    
    # return x
    ir.generate_return("x")
    
    # Write outputs
    ir.write_output()
    
    # Print IR to console for quick verification
    print("\n--- IR ---")
    print("\n".join(ir.ir_code))
    print("\n--- Python-equivalent (preview) ---")
    print("\n".join(ir.python_code))
