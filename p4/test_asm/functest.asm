;code prof. Mortensen/class made during class a few days
;I use to see if I can get 42 with my assem/vm

;VM
;determine what size the bytecode is
;add 1024 bytes
;allocate that size (bytecode + call stack) of array of raw bytes
;read the bytecode into the first bytes (0-n)
;initialize callstack(s) to be x00s
;Rx => 0; PC mem[0:4]
;set up SP (Sb - 4), SL (end of CS), SB (end of stack), FP (0)

;ASM
        JMP MAIN
;
; Put your utility functions here
;
MAIN    MOV R1, SP          ;save current SP into R1 so we can assign it to FP
        MOV R2, SP          ;save sp
        ADI R2, #-16
        CMP R2, SL
        BLT R2, STACKOVERFLOW

        ADI SP, #-4         ;reserve space for ret addr on stack
        STR FP, SP          ;store FP => 0, into PFP
        ADI SP, #-4         ;point to next int on stack
        MOV FP, R1          ;set FP == Former/Original SP
        MOVI R1, #7         ;R1 == 7  (first param)
        STR R1, SP          ;STORE param-1's value on Stack
        ADI SP, #-4         ;point to next int on stack
        MOVI R1, #6         ;R1 == 6 (second param)
        STR R1, SP          ;STORE param-2's value on Stack
        ADI SP, #-4         ;point to next int on stack

;check for stack overflow
        MOV R1, SP          ;save sp
        CMP R1, SL
        BLT R1, STACKOVERFLOW
        MOV R1, PC          ;save current PC (which points at next instruction when executing
        ADI R1, #36
        STR R1, FP
        JMP MULT            ;invoke MULT(X,Y)
RETURNHEREORELSE MOV R1, R1
        MOV SP, FP          ;get rid of top (no longer needed) frame
        MOV R1, FP          ;SP <= FP
        ADI R1, #-4         ;get the PFP

        LDR R3, FP          ;load result's value (@FP) into R3
        TRP #1

        LDR FP, R1          ;FP = PFP
        MOV R2, SP          ;check for stackunderflow
        CMP R2, SB
        BGT R2, STACKUNDERFLOW

        TRP #0





;FP <= PFP
;check for stack underflow


;MULT (x, y): return x*y

;cache ret addr in RegX
;copy ret value
;JMR to RegX
MULT    MOV R15, FP
        ADI R15, #-8
        LDR R1, R15
        ADI R15, #-4
        LDR R2, R15
        MUL R1, R2
        ;load ret addr
        LDR R2, FP
        ;store ret val where ret addr was
        STR R1, FP
        JMR R2

STACKOVERFLOW	TRP #0
STACKUNDERFLOW 	TRP #0