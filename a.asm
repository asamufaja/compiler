tmp1_sus_fib .INT 
tmp2_sus_fib .INT 
bus .INT 
swes .INT 
JMP main
fib_sus MOV R0, R0
MOV R15, SP
STR R15, tmp1_sus_fib
ADI SP, #-4
MOV R15, SP
STR R15, tmp2_sus_fib
ADI SP, #-4
IF0start MOV R0, R0
MOV R15, FP
ADI R15, #-8
LDR R15, R15
MOVI R14, #0
CMP R15, R14
BRZ R15, equal0
MOVI R15, #0
JMP equal0end
equal0 MOVI R15, #1
equal0end MOV R0, R0
BRZ R15, IF0false
IF0true MOV R0 R0
LDR R14, FP          ; load ret addr
MOVI R3, #0

            MOV R13, R3          ; get ret val
            STR R13, FP          ; store ret val where ret addr was
JMR R14
JMP IF0end
IF0false MOV R0 R0
IF0end MOV R0, R0
IF1start MOV R0, R0
MOV R15, FP
ADI R15, #-8
LDR R15, R15
MOVI R14, #1
CMP R15, R14
BRZ R15, equal2
MOVI R15, #0
JMP equal2end
equal2 MOVI R15, #1
equal2end MOV R0, R0
BRZ R15, IF1false
IF1true MOV R0 R0
LDR R14, FP          ; load ret addr
MOVI R3, #1

            MOV R13, R3          ; get ret val
            STR R13, FP          ; store ret val where ret addr was
JMR R14
JMP IF1end
IF1false MOV R0 R0
IF1end MOV R0, R0
LDR R15, FP          ; load ret addr

; before frame make
            ADI SP, #-4          ; should be extra space for ret value to keep in this frame
;ADI SP, #-4          ; should be extra space for ret value to keep in this frame
MOV R13, SP	;trying to put old params on stack to recurse
ADI R13, #-8
MOV R3, FP
ADI R3, #-8
LDR R3, R3
STR R3, R13

            
            MOV R13, SP          ;save current SP into R13 so we can assign it to FP
            MOV R12, SP          ;save sp
            ADI R12, #20  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R12, SL
            BLT R12, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R13          ;set FP == Former/Original SP
            ; params

MOV R14, FP
ADI R14, #-8
LDR R14, R14
MOVI R13, #1
SUB R14, R13	;doing SUB with expr:identifier value:x at:A6BA77670, expr:num_literal value:1 at:A6BA77B50
MOV R3, R14
STR R3, SP
ADI SP, #-4

            MOV R13, SP          ;save sp - check for stack overflow
            CMP R13, SL
            BLT R13, STACKOVERFLOW
            MOV R13, PC          ;save current PC (which points at next instruction when executing
            ADI R13, #36
            STR R13, FP
            JMP fib_sus

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R13, FP          ;SP <= FP
            ADI R13, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R11, FP      ;and one for oher uses just in case
        
            LDR FP, R13          ;FP = PFP
            MOV R12, SP          ;check for stackunderflow
            CMP R12, SB
            BGT R12, STACKUNDERFLOW
            
            ; before frame make
            ;ADI SP, #-4          ; should be extra space for ret value to keep in this frame

            ; after frame make
            ;MOV R11, FP         ; put the ret of fib(x-1) on stack
            ;ADI R11, #-12   ;-12 because FP is ret addr, FP-4 is PFP, FP-8 is the int x param
            ;STR R3, R11

            ; after frame make
            MOV R14, FP         ; put the ret of fib(x-1) on stack
            ADI R14, #-12   ;-12 because FP is ret addr, FP-4 is PFP, FP-8 is the int x param
            STR R3, R14
;ADI SP, #-4          ; should be extra space for ret value to keep in this frame
MOV R13, SP	;trying to put old params on stack to recurse
ADI R13, #-8
MOV R3, FP
ADI R3, #-8
LDR R3, R3
STR R3, R13

            
            MOV R13, SP          ;save current SP into R13 so we can assign it to FP
            MOV R14, SP          ;save sp
            ADI R14, #20  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R14, SL
            BLT R14, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R13          ;set FP == Former/Original SP
            ; params

MOV R12, FP
ADI R12, #-8
LDR R12, R12
MOVI R13, #2
SUB R12, R13	;doing SUB with expr:identifier value:x at:A6BA77B20, expr:num_literal value:2 at:A6BA77D00
MOV R3, R12
STR R3, SP
ADI SP, #-4

            MOV R13, SP          ;save sp - check for stack overflow
            CMP R13, SL
            BLT R13, STACKOVERFLOW
            MOV R13, PC          ;save current PC (which points at next instruction when executing
            ADI R13, #36
            STR R13, FP
            JMP fib_sus

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R13, FP          ;SP <= FP
            ADI R13, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R10, FP      ;and one for oher uses just in case
        
            LDR FP, R13          ;FP = PFP
            MOV R14, SP          ;check for stackunderflow
            CMP R14, SB
            BGT R14, STACKUNDERFLOW
            
            ; before frame make
            ;ADI SP, #-4          ; should be extra space for ret value to keep in this frame

            ; after frame make
            ;MOV R10, FP         ; put the ret of fib(x-1) on stack
            ;ADI R10, #-12   ;-12 because FP is ret addr, FP-4 is PFP, FP-8 is the int x param
            ;STR R3, R10

MOV R14, FP
            ADI R14, #-12  ; the offset I put on earlier
            LDR R14, R14
MOV R13, R10
ADD R14, R13	;doing ADD with expr:() value:None at:A6BA77B80, expr:() value:None at:A6BA77D30
MOV R3, R14
LDR R15, FP

            MOV R13, R3          ; get ret val
            STR R13, FP          ; store ret val where ret addr was
JMR R15
main MOV R0, R0
MOV R15, SP
STR R15, bus
ADI SP, #-4
MOV R15, SP
STR R15, swes
ADI SP, #-4
;ADI SP, #-4          ; should be extra space for ret value to keep in this frame

            
            MOV R11, SP          ;save current SP into R11 so we can assign it to FP
            MOV R14, SP          ;save sp
            ADI R14, #20  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R14, SL
            BLT R14, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R11          ;set FP == Former/Original SP
            ; params

MOVI R3, #10
STR R3, SP
ADI SP, #-4

            MOV R11, SP          ;save sp - check for stack overflow
            CMP R11, SL
            BLT R11, STACKOVERFLOW
            MOV R11, PC          ;save current PC (which points at next instruction when executing
            ADI R11, #36
            STR R11, FP
            JMP fib_sus

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R11, FP          ;SP <= FP
            ADI R11, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R12, FP      ;and one for oher uses just in case
        
            LDR FP, R11          ;FP = PFP
            MOV R14, SP          ;check for stackunderflow
            CMP R14, SB
            BGT R14, STACKUNDERFLOW
            
            ; before frame make
            ;ADI SP, #-4          ; should be extra space for ret value to keep in this frame

            ; after frame make
            ;MOV R12, FP         ; put the ret of fib(x-1) on stack
            ;ADI R12, #-12   ;-12 because FP is ret addr, FP-4 is PFP, FP-8 is the int x param
            ;STR R3, R12
LDR R14, swes
STR R12, R14
LDR R3, swes
LDR R3, R3
TRP #1
TRP #0
STACKOVERFLOW TRP #99
TRP #0
STACKUNDERFLOW TRP #99
TRP #0
