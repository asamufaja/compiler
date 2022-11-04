from enum import Enum


class OpCodes(Enum):
    JMP = 1
    JMR = 2
    BNZ = 3
    BGT = 4  # baguette
    BLT = 5  # blt is tasty
    BRZ = 6  # subaru brz
    MOV = 7
    LDA = 8
    STR = 9
    LDR = 10
    STB = 11
    LDB = 12
    ADD = 13
    ADI = 14
    SUB = 15
    MUL = 16
    DIV = 17
    AND = 18
    OR = 19
    CMP = 20
    TRP = 21
    STR_I = 22
    LDR_I = 23
    STB_I = 24
    LDB_I = 25
    RUN = 26
    BLK = 27
    END = 28
    LCK = 29  # luck
    ULK = 30
    MOVI = 31
    CMPI = 32
    MULI = 33
    DIVI = 34