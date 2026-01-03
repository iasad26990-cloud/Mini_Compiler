# optimizer.py

class CodeOptimizer:
    def __init__(self, ir_file="ir.txt", optimized_file="optimized_ir.txt"):
        self.ir_file = ir_file
        self.optimized_file = optimized_file
        self.ir_lines = []
        self.optimized_lines = []
        self.constants = {}

    def read_ir(self):
        with open(self.ir_file, "r") as f:
            self.ir_lines = [line.strip() for line in f if line.strip()]

    def optimize(self):
        self.read_ir()

        for line in self.ir_lines:
            if "=" in line and not line.startswith("RETURN"):
                lhs, rhs = map(str.strip, line.split("="))

                # Constant assignment
                if rhs.isdigit():
                    self.constants[lhs] = rhs
                    self.optimized_lines.append(f"{lhs} = {rhs}")
                    continue

                # Constant folding: a = 2 + 3
                parts = rhs.split()
                if len(parts) == 3 and parts[0].isdigit() and parts[2].isdigit():
                    value = eval(rhs)
                    self.constants[lhs] = str(value)
                    self.optimized_lines.append(f"{lhs} = {value}")
                    continue

                # Constant propagation
                if rhs in self.constants:
                    self.optimized_lines.append(f"{lhs} = {self.constants[rhs]}")
                    self.constants[lhs] = self.constants[rhs]
                    continue

                self.optimized_lines.append(line)

            else:
                self.optimized_lines.append(line)

        self.remove_dead_temporaries()

    # 🔥 FIXED DEAD CODE ELIMINATION
    def remove_dead_temporaries(self):
        used = set()

        for line in self.optimized_lines:
            if "=" in line:
                _, rhs = line.split("=")
                for tok in rhs.split():
                    if tok.startswith("t"):
                        used.add(tok)

        final = []
        for line in self.optimized_lines:
            if "=" in line:
                lhs = line.split("=")[0].strip()
                if lhs.startswith("t") and lhs not in used:
                    continue  # remove dead temporary
            final.append(line)

        self.optimized_lines = final

    def write_optimized_ir(self):
        with open(self.optimized_file, "w") as f:
            for line in self.optimized_lines:
                f.write(line + "\n")

        print(f"Optimized IR written to {self.optimized_file}")
