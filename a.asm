endl_sus_strs .INT 
deez_sus_do .INT 
tmp1_sus_fib .INT 
tmp2_sus_fib .INT 
e_uhh_welp .INT 
bus .INT
bus_sus_sus .INT
JMP main
strs_sus MOV R0, R0
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, endl_sus_strs
ADI SP, #-4
MOVI R14, #10
LDR R13, endl_sus_strs
ADD R13, FP
STR R14, R13
LDR R3, endl_sus_strs
ADD R3, FP
LDR R3, R3
TRP #3

        LDR R15, FP          ; load ret addr
        JMR R15
do_sus MOV R0, R0
