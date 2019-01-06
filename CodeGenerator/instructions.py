class Instruction:
    def __init__(self,name,opcode,op_count):
        self.name = name
        self.opcode = opcode
        self.op_count = op_count


instructions_by_name = {}
instructions_by_opcode = {}


def add_instruction(name,opcode,op_count):
    instruction = Instruction(name,opcode,op_count)
    instructions_by_name[name] = instruction
    instructions_by_opcode[opcode] = instruction


# Operators
add_instruction("ADD", 0x10, 0)
add_instruction("SUB", 0x11, 0)
add_instruction("MULT", 0x12, 0)
add_instruction("DIV", 0x13, 0)
add_instruction("GR", 0x14, 0)
add_instruction("GREQ", 0x15, 0)
add_instruction("LS", 0x16, 0)
add_instruction("LSEQ", 0x17, 0)
add_instruction("EQ", 0x18, 0)
add_instruction("NEQ", 0x19, 0)
add_instruction("AND", 0x20, 0)
add_instruction("OR", 0x21, 0)
# Stack
add_instruction("PEEK", 0x40, 1)
add_instruction("POKE", 0x41, 1)
add_instruction("POP", 0x42, 0)
add_instruction("PUSH", 0x43, 1)
# Control transfer
add_instruction("CALL", 0x30, 1)
add_instruction("RET", 0x31, 0)
add_instruction("RET_V", 0x32, 0)
add_instruction("BR", 0x33,  1)
add_instruction("BZ", 0x34,  1)
add_instruction("CNT", 0x35, 1)
add_instruction("JMP", 0x36, 1)