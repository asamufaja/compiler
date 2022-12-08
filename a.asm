swes .INT 
x .INT 
i .INT 
.INT 3
MOV R15, SP
STR R15, swes
MOVI R15, #1
STR R15, SP
ADI SP, #-4
MOV R15, SP
STR R15, x
LDR R15, swes
MOVI R14, #5
ADD R15, R14	;doing ADD with swes, 5
STR R15, SP
ADI SP, #-4
MOV R14, SP
STR R14, i
MOVI R14, #0	;put local var i on stack
STR R14, SP
ADI SP, #-4
STR R14, SP
ADI SP, #-4
STR R14, SP
ADI SP, #-4
LDR R3, x
TRP #1
TRP #0
