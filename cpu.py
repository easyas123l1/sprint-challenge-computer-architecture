"""CPU functionality."""

import sys

# binary values
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
CMP = 0b10100111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0  # program counter
        self.running = False
        self.SP = 7  # Stack Pointer
        self.reg[self.SP] = 0xF4
        self.flag = bin(0)
        self.branch_table = {
            LDI: self.LDI,
            PRN: self.PRN,
            HLT: self.HLT,
            MUL: self.MUL,
            CMP: self.CMP
        }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = bin(1)
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = bin(1 << 2)
            else:
                self.flag = bin(1 << 1)

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def LDI(self, op_a, op_b):
        self.reg[op_a] = op_b
        return 3

    def PRN(self, op_a, op_b):
        print(self.reg[op_a])
        return 2

    def MUL(self, op_a, op_b):
        self.alu("MUL", op_a, op_b)
        return 3

    def HLT(self, op_a, op_b):
        self.running = False
        return 0

    def CMP(self, op_a, op_b):
        self.alu("CMP", op_a, op_b)
        return 3

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            # Instruction Register
            IR = self.ram[self.pc]
            # print(IR)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            if IR in self.branch_table:
                count = self.branch_table[IR](op_a, op_b)
                self.pc += count
            else:
                print(f'Unknown instruction: {IR}, at address PC: {self.pc}')
                sys.exit(1)
