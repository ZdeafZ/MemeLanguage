from meme_codegen.instructions import instructions_by_name,instructions_by_opcode


class Label:
    def __init__(self, value = None):
        self.offsets = []
        self.value = value


class CodeWriter:

    def __init__(self):
        self.code = []

    def dump(self):
        print("Binary form:")
        print(self.code)
        print("\n")
        print("Textual form:")
        offset = 0
        while offset in range(0,len(self.code)):
            opcode = self.code[offset]
            instr_descr = instructions_by_opcode[opcode]
            ops = self.code[offset + 1: offset + 1 + instr_descr.op_count]
            print("{:<5} {:10} {}".format(offset,instr_descr.name,ops))
            offset += 1 + instr_descr.op_count

    def write(self,instr,*ops):
        instr_descr = instructions_by_name[instr]

        if instr_descr.op_count != len(ops):
            print("bullshit operand count")
        self.code.append(instr_descr.opcode)
        for op in ops:
            if not isinstance(op,Label):
                self.code.append(op)
            elif op.value is None:
                op.offsets.append(len(self.code))
                self.code.append(123123)
            else:
                self.code.append(op.value)

    def new_label(self):
        return Label()

    def new_label_placed(self):
        return len(self.code)

    def place_label(self, label):
        label.value = len(self.code)
        for offset in label.offsets:
            self.code[offset] = label.value
