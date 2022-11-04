import json
import mmap
from model.OpCode import OpCodes
from model.Register import Register, getReg, isReg
from vm.VirtualMachine import VirtualMachine


class Assembler:
    def __init__(self, file_name):
        self.line_number = 0
        self.file_name = file_name
        # print(f"in assembler parsing {file_name}")
        self.sym_file_name = file_name[:-4] + "_sym.json"
        self.raw_assembly = []
        self.bin_file_name = file_name[:-4] + ".bin"
        self.offset = 4
        self.firstPass()

    def firstPass(self):
        line_number = 0
        sym_dict = {}
        code_started = False
        # directives = [".byt", ".BYT", ".int", ".INT"]
        with open(self.file_name) as file:
            for line in file:
                tokens = line.split()
                token_list = []
                for token in tokens:
                    if token.startswith(';'):
                    # if ';' in token:  # TODO this could be better to allow \; use maybe
                        break
                    # do some sort of stripping whitespace and stuff?
                    token_list.append(token)
                self.line_number += 1
                if len(token_list) != 0:
                    self.raw_assembly.append(token_list)
                # print(token_list)

                if (not code_started) and (len(token_list) >= 2):
                    # for directive in directives:
                    if self.isOpcode(token_list[0]) or self.isOpcode(token_list[1]):
                        # FIXME probably start of code segment
                        sym_dict["code_segment_start"] = self.offset
                        code_started = True

                # setting label offsets and calculating file size
                # print(token_list, self.offset)
                if len(token_list) == 0:
                    continue
                if len(token_list) == 1:
                    if not self.isOpcode(token_list[0]) and not self.isDirective(token_list[0]):
                        print("Error: Got a label that is all alone")
                        return
                if self.isOpcode(token_list[0]):
                    self.offset += 12
                    continue
                elif self.isDirective(token_list[0]):
                    # print(token_list, self.offset)
                    if token_list[0] == ".byt" or token_list[0] == ".BYT":
                        # print(token_list, self.offset)
                        self.offset += 1
                    else:  # it's a .INT
                        self.offset += 4
                    continue
                else:  # ADDING LABELS
                    # print(token_list, self.offset)
                    if token_list[0] in sym_dict:
                        print(f"Warning: duplicate label {token_list[0]}, line {self.line_number}, {token_list}")
                        raise ValueError
                    sym_dict[token_list[0]] = self.offset
                    if token_list[1] == ".BYT" or token_list[1] == ".byt":
                        self.offset += 1
                    elif token_list[1] == ".INT" or token_list[1] == ".int":
                        self.offset += 4
                    elif self.isOpcode(token_list[1]):
                        self.offset += 12
            # the offset of the next open spot
            sym_dict["code_segment_end"] = self.offset
            with open(self.sym_file_name, 'w') as sym_file:
                json.dump(sym_dict, sym_file)
            # I guess I'll second pass now
            self.secondPass()

    def isOpcode(self, thing):
        for ops in OpCodes:
            if thing == ops.name:
                return True
        return False

    def isDirective(self, thing):
        directives = [".byt", ".BYT", ".int", ".INT"]
        return thing in directives

    def secondPass(self):
        zero = 0
        with open(self.sym_file_name) as sym_file:
            sym_dict = json.load(sym_file)
            # print(sym_dict)
        with open(self.bin_file_name, 'w+b') as bin_file:
            mmap_bin_file = mmap.mmap(bin_file.fileno(), length=self.offset, access=mmap.ACCESS_WRITE)
            Register.reg_dict["PC"] = sym_dict["code_segment_start"]
            mmap_bin_file.write(Register.reg_dict["PC"].to_bytes(4, 'little', signed=True))
            # print(self.raw_assembly)


            for key in sym_dict.keys():  # checking for unused labels
                keycount = 0
                if key == "code_segment_start" or key == "code_segment_end":
                    continue
                for line in self.raw_assembly:
                    if key in line:
                        keycount += 1
                if keycount < 2:
                    print(f"Warning: unused label {key}")

            neatOpcodes = ["STR", "LDR", "STB", "LDB"]
            for token_list in self.raw_assembly:
                if self.isOpcode(token_list[0]):        # TODO make this writeinstruction maybe
                    opval = 0                           # TODO make this getopval?
                    if token_list[0] in neatOpcodes:
                        if token_list[2] in Register.reg_dict.keys() or token_list[2].startswith("("):
                            token_list[0] += "_I"
                    for op in OpCodes:
                        if token_list[0] == op.name:
                            opval = op.value
                            break                       # end TODO
                    mmap_bin_file.write(opval.to_bytes(4, "little", signed=True))
                    op1, *op2 = token_list[1:3]
                    # operands
                    for operand in op1, op2:
                        if len(operand) == 0:
                            mmap_bin_file.write(zero.to_bytes(4, 'little', signed=True))
                            continue
                        elif isinstance(operand, list):
                            operand = operand[0]
                        if operand.startswith('#'):
                            # shouldn't be any commas after an immediate operand...
                            mmap_bin_file.write((int(operand[1:])).to_bytes(4, 'little', signed=True))
                        elif operand.startswith("'"):
                            # it should be a MOVI with a byte
                            mmap_bin_file.write(bytes(operand[1], 'ascii'))
                            mmap_bin_file.write(zero.to_bytes(3, 'little', signed=True))  # pad the extra 3 bytes?
                        elif operand.startswith("("):
                            # FIXME needs testing if this works
                            operand = operand[1:-1]  # strip the () around the register
                            reg = getReg(operand)
                            mmap_bin_file.write(reg.to_bytes(4, 'little', signed=True))
                        # elif operand.startswith('R') or operand.startswith("S") or operand.startswith("F"):
                        elif isReg(operand) or isReg(operand[:-1]):
                            if operand.endswith(','):
                                reg = getReg(operand[:-1])  # omit the comma
                            else:
                                reg = getReg(operand)
                            mmap_bin_file.write(reg.to_bytes(4, 'little', signed=True))
                        elif len(operand) != 0:  # it's a label
                            # get its offset
                            if operand in sym_dict.keys():
                                off = sym_dict[operand]
                                mmap_bin_file.write(off.to_bytes(4, 'little', signed=True))
                            else:
                                print(f"Got a label that wasn't defined: {operand}")
                                return 1
                        else:  # it's empty?
                            mmap_bin_file.write(zero.to_bytes(4, 'little', signed=True))
                elif self.isDirective(token_list[0]):  # a directive without a label
                    if token_list[0] == ".byt" or token_list[0] == ".BYT":
                        if len(token_list) == 2:  # there's a value
                            if token_list[1].startswith("'"):
                                character = token_list[1][1:-1]
                                if character == "\\" + "n":  # FIXME there's gotta be a better way
                                    character = "\n"
                                if character == "\s":
                                    character = " "
                                mmap_bin_file.write(bytes(character, "ascii"))
                            else:
                                mmap_bin_file.write(bytes(token_list[1], "ascii"))
                        else:  # no value
                            mmap_bin_file.write(zero.to_bytes(1, 'little', signed=True))  # write one zero byte
                    elif token_list[0] == ".int" or token_list[0] == ".INT":
                        if len(token_list) == 2:  # there's value
                            if token_list[1].startswith("#"):
                                mmap_bin_file.write(int(token_list[1][1:]).to_bytes(4, "little", signed=True))
                            else:
                                mmap_bin_file.write(int(token_list[1]).to_bytes(4, "little", signed=True))
                        else:  # no value
                            mmap_bin_file.write(zero.to_bytes(4, "little", signed=True))  # four zero bytes
                else:  # a label probably
                    if self.isDirective(token_list[1]):  # directive after label
                        if len(token_list) == 3:  # there's a value
                            if token_list[1] == ".int" or token_list[1] == ".INT":
                                if token_list[2].startswith("#"):
                                    mmap_bin_file.write(int(token_list[2][1:]).to_bytes(4, "little", signed=True))
                                else:
                                    mmap_bin_file.write(int(token_list[2]).to_bytes(4, "little", signed=True))
                            # TODO this could use more testing
                            elif token_list[1] == ".byt" or token_list[1] == ".BYT":
                                if token_list[2].startswith("'"):  # '' around the byte
                                    # print(token_list)
                                    character = token_list[2][1:-1]
                                    # print(f"character='{character}'")
                                    if character == "\\" + "n":  # FIXME there's gotta be a better way? lol
                                        character = "\n"
                                    if character == "\s":
                                        character = " "
                                    mmap_bin_file.write(bytes(character, "ascii"))
                                else:  # no ''
                                    mmap_bin_file.write(bytes(token_list[2], "ascii"))
                            # TODO support different byte types like hex and dec
                        else:  # no value after directive, set a default value
                            if token_list[1] == ".int" or token_list[1] == ".INT":
                                mmap_bin_file.write(zero.to_bytes(4, "little", signed=True))
                            else:
                                mmap_bin_file.write(zero.to_bytes(1, "little", signed=True))
                    elif self.isOpcode(token_list[1]):  # opcode after label
                        # TODO slightly duplicated writeinstruction
                        opval = 0                   # TODO make this getopval
                        if token_list[1] in neatOpcodes:
                            if token_list[3] in Register.reg_dict.keys() or token_list[3].startswith("("):
                                token_list[1] += "_I"
                        for op in OpCodes:
                            if token_list[1] == op.name:
                                opval = op.value
                                break               # TODO
                        mmap_bin_file.write(opval.to_bytes(4, "little", signed=True))
                        op1, *op2 = token_list[2:4]
                        # operands
                        for operand in op1, op2:
                            if len(operand) == 0:
                                mmap_bin_file.write(zero.to_bytes(4, 'little', signed=True))
                                continue
                            elif isinstance(operand, list):
                                operand = operand[0]
                            if operand.startswith('#'):
                                mmap_bin_file.write((int(operand[1:])).to_bytes(4, 'little', signed=True))
                            elif operand.startswith("'"):
                                # it should be a MOVI with a byte
                                mmap_bin_file.write(bytes(operand[1], 'ascii'))
                                mmap_bin_file.write(zero.to_bytes(3, 'little', signed=True))
                            elif operand.startswith("("):
                                operand = operand[1:-1]
                                reg = getReg(operand)
                                mmap_bin_file.write(reg.to_bytes(4, 'little', signed=True))
                            # elif operand.startswith('R') or operand.startswith("S") or operand.startswith("F"):
                            elif isReg(operand) or isReg(operand[:-1]):
                                if operand.endswith(","):
                                    reg = getReg(operand[:-1])  # omit the comma
                                else:
                                    reg = getReg(operand)
                                mmap_bin_file.write(reg.to_bytes(4, 'little', signed=True))
                            elif len(operand) != 0:  # it's a label
                                # get it's offset
                                if operand in sym_dict.keys():
                                    off = sym_dict[operand]
                                    mmap_bin_file.write(off.to_bytes(4, 'little', signed=True))
                                else:  # missing label
                                    print(f"Got a label that wasn't defined: {operand}")
                                    return 1
                            else:  # it's empty?
                                mmap_bin_file.write(zero.to_bytes(4, 'little', signed=True))
            mmap_bin_file.flush()
            mmap_bin_file.close()


        # VirtualMachine(self.bin_file_name)
