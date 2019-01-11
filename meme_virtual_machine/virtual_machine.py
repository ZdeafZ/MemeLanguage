import meme_codegen.instructions as instructions


class VirtualMachine:
    def __init__(self, code):
        self.code_base = 300
        self.memory = [] + [0]*4096
        counter = 0
        for instruction in code:
            self.memory[self.code_base + counter] = instruction
            counter += 1
        self.ip = self.code_base
        self.sp = 2000
        self.fp = self.sp
        self.running = True

    def execute(self):
        while self.running:
            self.execute_one()

    def execute_call(self, args):
        self.sp -= args
        target = self.memory[self.sp - 3] + self.code_base
        self.memory[self.sp - 3] = self.ip
        self.memory[self.sp - 2] = self.fp
        self.memory[self.sp - 1] = self.sp - 3
        self.ip = target
        self.fp = self.sp

    def execute_ret(self, value):
        old_ip = self.memory[self.fp - 3]
        old_fp = self.memory[self.fp - 2]
        old_sp = self.memory[self.fp - 1]

        self.ip = old_ip
        self.fp = old_fp
        self.sp = old_sp

        self.push(value)

    def execute_one(self):
        opcode = self.read_immediate()
        print(opcode)
        print("ip: {}".format(self.ip-1))
        print("fp: {}".format(self.fp))
        print("sp: {}".format(self.sp))
        if opcode == 0x10:
            b = self.pop()
            a = self.pop()
            self.push(a + b)

        elif opcode == 0x11:
            b = self.pop()
            a = self.pop()
            self.push(a - b)

        elif opcode == 0x12:
            b = self.pop()
            a = self.pop()
            self.push(a * b)

        elif opcode == 0x13:
            b = self.pop()
            a = self.pop()
            self.push(a / b)

        elif opcode == 0x14:
            b = self.pop()
            a = self.pop()
            if a > b:
                self.push(1)
            else:
                self.push(0)

        elif opcode == 0x15:
            b = self.pop()
            a = self.pop()
            if a >= b:
                self.push(1)
            else:
                self.push(0)

        elif opcode == 0x16:
            b = self.pop()
            a = self.pop()
            if a < b:
                self.push(1)
            else:
                self.push(0)

        elif opcode == 0x17:
            b = self.pop()
            a = self.pop()
            if a <= b:
                self.push(1)
            else:
                self.push(0)

        elif opcode == 0x16:
            b = self.pop()
            a = self.pop()
            if a < b:
                self.push(1)
            else:
                self.push(0)

        elif opcode == 0x17:
            b = self.pop()
            a = self.pop()
            if a <= b:
                self.push(1)
            else:
                self.push(0)

        elif opcode == 0x18:
            b = self.pop()
            a = self.pop()
            if a == b:
                self.push(1)
            else:
                self.push(0)

        elif opcode == 0x19:
            b = self.pop()
            a = self.pop()
            if a != b:
                self.push(1)
            else:
                self.push(0)

        elif opcode == 0x20:
            b = self.pop()
            a = self.pop()
            if a and b:
                self.push(1)
            else:
                self.push(0)

        elif opcode == 0x21:
            b = self.pop()
            a = self.pop()
            if a or b:
                self.push(1)
            else:
                self.push(0)

        elif opcode == 0x40:
            idx = self.read_immediate()
            self.push(self.memory[self.fp + idx])

        elif opcode == 0x41:
            idx = self.read_immediate()
            self.memory[self.fp + idx] = self.pop()

        elif opcode == 0x42:
            self.pop()

        elif opcode == 0x43:
            value = self.read_immediate()
            self.push(value)

        elif opcode == 0x30:
            self.execute_call(self.read_immediate())

        elif opcode == 0x31:
            self.execute_ret(0)

        elif opcode == 0x32:
            self.execute_ret(self.pop())

        elif opcode == 0x33:
            target = self.read_immediate_target()
            self.ip = target

        elif opcode == 0x34:
            target = self.read_immediate_target()
            if self.pop() == 0:
                self.ip = target

        elif opcode == 0x35:
            num = self.read_immediate()
            self.sp += num

        elif opcode == 0x36:
            self.running = False

    def pop(self):
        self.sp -= 1
        return self.memory[self.sp]

    def push(self, value):
        self.memory[self.sp] = value
        self.sp += 1

    def read_immediate(self):
        value = self.memory[self.ip]
        self.ip += 1
        return value

    def read_immediate_target(self):
        return self.read_immediate() + self.code_base
