# register_allocator.py

class RegisterAllocator:
    def __init__(self, ir_file="optimized_ir.txt", reg_file="reg_ir.txt"):
        self.ir_file = ir_file
        self.reg_file = reg_file
        self.ir_lines = []
        self.register_map = {}
        self.register_count = 0
        self.reg_ir = []

    def new_register(self):
        self.register_count += 1
        return f"R{self.register_count}"

    def read_ir(self):
        with open(self.ir_file, "r") as f:
            self.ir_lines = [line.strip() for line in f if line.strip()]

    def allocate(self):
        self.read_ir()

        for line in self.ir_lines:
            if "=" not in line:
                self.reg_ir.append(line)
                continue

            lhs, rhs = map(str.strip, line.split("="))

            # Assign register to lhs if not exists
            if lhs not in self.register_map:
                self.register_map[lhs] = self.new_register()

            lhs_reg = self.register_map[lhs]

            # Case: constant
            if rhs.isdigit():
                self.reg_ir.append(f"{lhs_reg} = {rhs}")
                continue

            # Case: variable
            if rhs.isidentifier():
                if rhs not in self.register_map:
                    self.register_map[rhs] = self.new_register()
                rhs_reg = self.register_map[rhs]
                self.reg_ir.append(f"{lhs_reg} = {rhs_reg}")
                continue

            # Case: binary operation
            parts = rhs.split()
            if len(parts) == 3:
                a, op, b = parts

                if a.isidentifier():
                    if a not in self.register_map:
                        self.register_map[a] = self.new_register()
                    a = self.register_map[a]

                if b.isidentifier():
                    if b not in self.register_map:
                        self.register_map[b] = self.new_register()
                    b = self.register_map[b]

                self.reg_ir.append(f"{lhs_reg} = {a} {op} {b}")

    def write_register_ir(self):
        with open(self.reg_file, "w") as f:
            for line in self.reg_ir:
                f.write(line + "\n")

        print(f"Register-based IR written to {self.reg_file}")
