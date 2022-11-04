from enum import Enum

'''Registers
    I'm still experimenting with it a bit'''


class Register:
    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4
    R5 = 5
    R6 = 6
    R7 = 7
    R8 = 8
    R9 = 9
    R10 = 10
    R11 = 11
    R12 = 12
    R13 = 13
    R14 = 14
    R15 = 15
    PC = 16
    SL = 17
    SB = 18
    SP = 19
    FP = 20
    reg_dict = {"R0": 0,
                "R1": 1,
                "R2": 2,
                "R3": 3,
                "R4": 4,
                "R5": 5,
                "R6": 6,
                "R7": 7,
                "R8": 8,
                "R9": 9,
                "R10": 10,
                "R11": 11,
                "R12": 12,
                "R13": 13,
                "R14": 14,
                "R15": 15,
                "PC" : 16,
                "SL" : 17,
                "SB" : 18,
                "SP" : 19,
                "FP" : 20}


def isReg(thing):
    for r in Register.reg_dict.keys():
        if thing == r:
            return True
    return False

def getReg(thing):  # idk if this is really necessary but it's what I thought of
    if thing == "R1":
        return Register.R1
    elif thing == "R2":
        return Register.R2
    elif thing == "R3":
        return Register.R3
    elif thing == "R4":
        return Register.R4
    elif thing == "R5":
        return Register.R5
    elif thing == "R6":
        return Register.R6
    elif thing == "R7":
        return Register.R7
    elif thing == "R8":
        return Register.R8
    elif thing == "R9":
        return Register.R9
    elif thing == "R10":
        return Register.R10
    elif thing == "R11":
        return Register.R11
    elif thing == "R12":
        return Register.R12
    elif thing == "R13":
        return Register.R13
    elif thing == "R14":
        return Register.R14
    elif thing == "R15":
        return Register.R15
    elif thing == "PC":
        return Register.PC
    elif thing == "SP":
        return Register.SP
    elif thing == "FP":
        return Register.FP
    elif thing == "SL":
        return Register.SL
    elif thing == "SB":
        return Register.SB
