import json
import mmap
import shutil
import sys


from model.OpCode import OpCodes
from model.Register import Register, getReg

class VirtualMachine:
    # gotta do some sort of checking if it's a .bin or .asm? maybe that's in main
    # by project 3 we  should get a stack and put activiaton records on there
    # and by project 4 (optional?) preemptive multitasking (concurrent not parallel)
    # good idea to check where code segment starts and ends and enforce pc there
    # maybe have registers and stacks be own entity?
    # first operand, if not register, it probably register?
    # second register could be empty, immediate, or label after maybe being register

    def __init__(self, file_name):
        self.file_name = file_name
        self.sym_file_name = self.file_name[:-4] + "_sym.json"
        self.run_log_file_name = self.file_name[:-4] + "_run.log"
        self.running = False
        # print(f"in VM running {file_name}")
        self.bigswitch()

    def getOpName(self, opNum):
        for op in OpCodes:
            if opNum == op.value:
                return op.name


    def bigswitch(self):
        with open(self.sym_file_name) as sym_file:
            sym_dict = json.load(sym_file)
        shutil.copyfile(self.file_name, self.file_name[:-4] + "_fake.bin")
        # TODO For now I'm using a _fake.bin file for adding stack to and changing up
        bin_file = open(self.file_name[:-4] + "_fake.bin", 'a+b')
        mmap_bin_file = mmap.mmap(bin_file.fileno(), 0, access=mmap.ACCESS_WRITE)  # idk if it ok to say 0 length
        log_file = open(self.run_log_file_name, 'w')
        self.running = True
        # make a stack
        self.makeStack(mmap_bin_file, sym_dict)
        # mmap_bin_file.seek(Register.reg_dict["PC"])
        Register.reg_dict["PC"] = int.from_bytes(mmap_bin_file.read(4), 'little', signed=True)
        mmap_bin_file.seek(Register.reg_dict["PC"])

        while self.running:
            Register.reg_dict["PC"] += 12
            instruction = []
            for x in range(3):
                instruction.append(int.from_bytes(mmap_bin_file.read(4), 'little', signed=True))
            reg1 = "R" + str(instruction[1])  # finally put this here, idk if good idea but probably
            reg2 = "R" + str(instruction[2])  # only use if opcode expecting register
            # similar to above for the stack registers
            # TODO I've got a bad feeling about this
            stack_regs = {16 : "PC", 17 : "SL", 18 : "SB", 19 : "SP", 20 : "FP"}
            if instruction[1] in stack_regs.keys():
                reg1 = stack_regs[instruction[1]]
            if instruction[2] in stack_regs.keys():
                reg2 = stack_regs[instruction[2]]

            # this log file gets massive when doing stuff like recursion, so I commented it out
            # log_file.write(f"{Register.reg_dict}\nInstruction {instruction}:\t {self.getOpName(instruction[0])}\t{reg1}\t{reg2}\n")

            if instruction[0] == 1:  # JMP
                if instruction[1] < sym_dict["code_segment_start"] or instruction[1] > sym_dict["code_segment_end"]:
                    print(f"Warning: PC set to addr outside code seg -> {instruction[1]}")
                Register.reg_dict["PC"] = instruction[1]
                mmap_bin_file.seek(Register.reg_dict["PC"])

            elif instruction[0] == 2:  #JMR
                # FIXME this is supposed to be that there's an address (offset) in reg that I go straight to?
                if Register.reg_dict[reg1] < sym_dict["code_segment_start"] or Register.reg_dict[reg1] > sym_dict["code_segment_end"]:
                    print(f"Warning: PC set to addr outside code seg -> {Register.reg_dict[reg1]}")
                Register.reg_dict["PC"] = Register.reg_dict[reg1]
                mmap_bin_file.seek(Register.reg_dict["PC"])

            elif instruction[0] == 3:  # BNZ
                if Register.reg_dict[reg1] != 0:
                    if instruction[2] < sym_dict["code_segment_start"] or instruction[2] > sym_dict["code_segment_end"]:
                        print(f"Warning: PC set to addr outside code seg -> {instruction[2]}")
                    Register.reg_dict["PC"] = instruction[2]
                    mmap_bin_file.seek(Register.reg_dict["PC"])

            elif instruction[0] == 4:  # BGT
                if Register.reg_dict[reg1] > 0:
                    if instruction[2] < sym_dict["code_segment_start"] or instruction[2] > sym_dict["code_segment_end"]:
                        print(f"Warning: PC set to addr outside code seg -> {instruction[2]}")
                    Register.reg_dict["PC"] = instruction[2]
                    mmap_bin_file.seek(Register.reg_dict["PC"])

            elif instruction[0] == 5:  # BLT
                if Register.reg_dict[reg1] < 0:
                    if instruction[2] < sym_dict["code_segment_start"] or instruction[2] > sym_dict["code_segment_end"]:
                        print(f"Warning: PC set to addr outside code seg -> {instruction[2]}")
                    Register.reg_dict["PC"] = instruction[2]
                    mmap_bin_file.seek(Register.reg_dict["PC"])

            elif instruction[0] == 6:  # BRZ
                if Register.reg_dict[reg1] == 0:
                    if instruction[2] < sym_dict["code_segment_start"] or instruction[2] > sym_dict["code_segment_end"]:
                        print(f"Warning: PC set to addr outside code seg -> {instruction[2]}")
                    Register.reg_dict["PC"] = instruction[2]
                    mmap_bin_file.seek(Register.reg_dict["PC"])

            elif instruction[0] == 7:  # MOV
                # MOV   R1, R2 ;means put contents of R2 in R1
                Register.reg_dict[reg1] = Register.reg_dict[reg2]

            elif instruction[0] == 8:  # LDA
                if instruction[2] > sym_dict["code_segment_start"]:
                    print("Error: LDA with address outside data segment")
                    return
                Register.reg_dict[reg1] = instruction[2]

            elif instruction[0] == 9:  # STR
                # FIXME is this supposed to be writing to the bin file?
                mmap_bin_file.seek(instruction[2])
                mmap_bin_file.write(int(Register.reg_dict[reg1]).to_bytes(4, "little", signed=True))
                mmap_bin_file.seek(Register.reg_dict["PC"])
                # TODO I'm kinda idk about if this works so I'm keeping an eye on it...

            elif instruction[0] == 10:  # LDR
                # LDR   R1, label ;means put int in label in R1
                mmap_bin_file.seek(instruction[2])
                Register.reg_dict[reg1] = int.from_bytes(mmap_bin_file.read(4), 'little', signed=True)
                mmap_bin_file.seek(Register.reg_dict["PC"])

            elif instruction[0] == 11:  # STB
                mmap_bin_file.seek(instruction[2])
                mmap_bin_file.write(bytes(Register.reg_dict[reg1], "ascii"))
                mmap_bin_file.seek(Register.reg_dict["PC"])

            elif instruction[0] == 12:  # LDB
                # LDB   R1, label ;means put byte in label in R1
                mmap_bin_file.seek(instruction[2])
                Register.reg_dict[reg1] = mmap_bin_file.read(1).decode("ascii")
                mmap_bin_file.seek(Register.reg_dict["PC"])  # so I can seek back to the (next) instruction

            elif instruction[0] == 13:  # ADD
                # ADD   R1, R2 ;means add contents of the registers and put result in R1
                Register.reg_dict[reg1] = Register.reg_dict[reg1] + Register.reg_dict[reg2]

            elif instruction[0] == 14:  # ADI
                # ADI   R1, #3 ;means add the 3 to R1 (and store in R1)
                Register.reg_dict[reg1] = Register.reg_dict[reg1] + instruction[2]

            elif instruction[0] == 15:  # SUB
                # SUB   R1, R2 ;means R1 - R2? result go R1 (always do)
                Register.reg_dict[reg1] = Register.reg_dict[reg1] - Register.reg_dict[reg2]

            elif instruction[0] == 16:  # MUL
                Register.reg_dict[reg1] = Register.reg_dict[reg1] * Register.reg_dict[reg2]

            elif instruction[0] == 17:  # DIV
                Register.reg_dict[reg1] = Register.reg_dict[reg1] // Register.reg_dict[reg2]
                # TODO, maybe I should keep the remainder somewhere?

            elif instruction[0] == 18:  # AND
                if Register.reg_dict[reg1] and Register.reg_dict[reg2]:
                    Register.reg_dict[reg1] = 1
                else:
                    Register.reg_dict[reg1] = 0

            elif instruction[0] == 19:  # OR
                if Register.reg_dict[reg1] or Register.reg_dict[reg2]:
                    Register.reg_dict[reg1] = 1
                else:
                    Register.reg_dict[reg1] = 0

            elif instruction[0] == 20:  # CMP
                # print(Register.reg_dict[reg1], Register.reg_dict[reg2])
                if Register.reg_dict[reg1] == Register.reg_dict[reg2]:
                    Register.reg_dict[reg1] = 0
                elif Register.reg_dict[reg1] > Register.reg_dict[reg2]:
                    Register.reg_dict[reg1] = 1
                else:
                    Register.reg_dict[reg1] = -1

            elif instruction[0] == 21:  # TRP
                if instruction[1] == 0:
                    self.running = False
                elif instruction[1] == 1:
                    # for printing ints
                    print(Register.reg_dict["R3"], end="")
                elif instruction[1] == 2:  # get int from console

                    stuff = input()
                    num = ""
                    for x in stuff:
                        if x.isdecimal() or x == '-':
                            num += x
                        else:
                            break
                    if not num:
                        print("Warning: no value detected")
                    Register.reg_dict["R3"] = int(num)
                elif instruction[1] == 3:  # TODO maybe TRP #1 and TRP #3 shouldn't be same
                    # for printing bytes
                    if isinstance(Register.reg_dict["R3"], str):
                        print(Register.reg_dict["R3"], end="")
                        continue
                    try:  # converting the thing in register into a byte
                        temp = int(Register.reg_dict["R3"]).to_bytes(1, 'little', signed=True)
                        char = str(temp.decode('ascii'))
                        print(char, end='')
                    except:
                        print(Register.reg_dict["R3"], end="")
                elif instruction[1] == 4:  # get char from console
                    Register.reg_dict["R3"] = sys.stdin.read(1)
                elif instruction[1] == 99:
                    print(Register.reg_dict)

            elif instruction[0] == 22:  # STR_I
                mmap_bin_file.seek(Register.reg_dict[reg2])
                mmap_bin_file.write(Register.reg_dict[reg1].to_bytes(4, "little", signed=True))
                mmap_bin_file.seek(Register.reg_dict["PC"])
                # print("putting", Register.reg_dict[reg1], "into offset", Register.reg_dict[reg2])


            elif instruction[0] == 23:  # LDR_I
                # if reg1 in stack_regs:
                #
                mmap_bin_file.seek(Register.reg_dict[reg2])
                Register.reg_dict[reg1] = int.from_bytes(mmap_bin_file.read(4), 'little', signed=True)
                mmap_bin_file.seek(Register.reg_dict["PC"])

            elif instruction[0] == 24:  # STB_I
                mmap_bin_file.seek(Register.reg_dict[reg2])
                mmap_bin_file.write(bytes(str(Register.reg_dict[reg1]), "ascii"))
                mmap_bin_file.seek(Register.reg_dict["PC"])

            elif instruction[0] == 25:  # LDB_I
                mmap_bin_file.seek(Register.reg_dict[reg2])
                Register.reg_dict[reg1] = mmap_bin_file.read(1).decode("ascii")
                mmap_bin_file.seek(Register.reg_dict["PC"])

            elif instruction[0] == 26:  # RUN
                pass

            elif instruction[0] == 27:  # BLK
                pass

            elif instruction[0] == 28:  # END
                pass

            elif instruction[0] == 29:  # LCK
                pass

            elif instruction[0] == 30:  # ULK
                pass

            elif instruction[0] == 31:  # MOVI
                # TODO this currently probably only works for ints?
                Register.reg_dict[reg1] = instruction[2]

            elif instruction[0] == 32:  # CMPI
                if Register.reg_dict[reg1] == instruction[2]:
                    Register.reg_dict[reg1] = 0
                elif Register.reg_dict[reg1] > instruction[2]:
                    Register.reg_dict[reg1] = 1
                else:
                    Register.reg_dict[reg1] = -1

            elif instruction[0] == 33:  # MULI
                Register.reg_dict[reg1] *= instruction[2]

            elif instruction[0] == 34:  # DIVI
                Register.reg_dict[reg1] //= instruction[2]

            else:  # uhh, oops?
                print("Warning: Unknown Op Code happened probably")

        # if I don't close and flush then it won't write it to the bin right? do I want it written to bin?
        # mmap_bin_file.flush()
        # mmap_bin_file.close()
        # bin_file.close()

        log_file.close()

    def makeStack(self, mmap_bin_file, sym_dict):
        old_bin_size = mmap_bin_file.size()
        mmap_bin_file.resize(mmap_bin_file.size() + 1024)
        # mmap_bin_file.seek(mmap_bin_file.size())
        # zero = 0
        # for _ in range(1024):
        #     mmap_bin_file.write(zero.to_bytes(1, "little", signed=True))


        # self.bytecode_with_stack = [0b0 for _ in range(1024)]
        # mmap_bin_file.seek(0)
        # for _ in range(mmap_bin_file.size()):
        #     self.bytecode_with_stack.insert(0, mmap_bin_file.read(1))
        # fixedArr = np.array(bytecode_with_stack)

        # TODO maybe I should make this not dependent on symbol table? I think I could with mmap.size()
        Register.reg_dict["SL"] = old_bin_size
        Register.reg_dict["SB"] = mmap_bin_file.size()  # new bin size
        Register.reg_dict["SP"] = Register.reg_dict["SB"] - 4
        Register.reg_dict["FP"] = 0

    # def trap99(): # an idea for this function
    #     for register in Register:
    #         print(f"{register} = {self.registers[register.value]}\n")
    #     # and maybe print the whole data segment and stack when that is a thing



