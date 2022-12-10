coo .INT 
bus .INT 
JMP main
MOVI R15, 'a'
LDR R14, coo
STR R15, R14
main MOV R0, R0
MOVI R14, #1
MOVI R15, #1
ADD R14, R15	;doing ADD with 1, 1
