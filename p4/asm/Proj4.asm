ARR         .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT
            .INT

i           .INT #0
input       .INT

            JMP main

fib         MOV R15, FP         ; block for getting the operands
            ADI R15, #-8
            LDR R4, R15         ; op 1, int x

            ; if x == 0 return 0
            MOV R3, R4
            CMPI R3, #0
            BNZ R3, FIB2

            ; RETURN 0
            LDR R2, FP          ; load ret addr
            MOVI R1, #0
            STR R1, FP          ; store ret val where ret addr was
            JMR R2

            ; elif x == 1 return 1
FIB2        MOV R3, R4
            CMPI R3, #1
            BNZ R3, FIB3

            ; RETURN 1
            LDR R2, FP          ; load ret addr
            MOVI R1, #1
            STR R1, FP          ; store ret val where ret addr was
            JMR R2

            ; else return fib(x - 1) + fib(x - 2)
FIB3        ADI SP, #-4          ; should be extra space for fib(x-1) value to keep in this frame

; ################ CALLING FIB x - 1 ###########
            MOV R1, SP          ;save current SP into R1 so we can assign it to FP
            MOV R2, SP          ;save sp
            ADI R2, #-16
            CMP R2, SL
            BLT R2, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R1          ;set FP == Former/Original SP

            ; param 1, x - 1
            MOV R3, R4          ; op 1 is in R4 from the stack
            ADI R3, #-1
            STR R3, SP          ;STORE param-1's value on Stack
            ADI SP, #-4         ;point to next int on stack

            MOV R1, SP          ;save sp - check for stack overflow
            CMP R1, SL
            BLT R1, STACKOVERFLOW
            MOV R1, PC          ;save current PC (which points at next instruction when executing)
            ADI R1, #36
            STR R1, FP
            JMP fib

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R1, FP          ;SP <= FP
            ADI R1, #-4         ;get the PFP

            LDR R3, FP          ;get ret val to put in frame

            LDR FP, R1          ;FP = PFP
            MOV R2, SP          ;check for stackunderflow
            CMP R2, SB
            BGT R2, STACKUNDERFLOW

            MOV R14, FP         ; put the ret of fib(x-1) on stack
            ADI R14, #-12
            STR R3, R14

; ################ CALLING FIB x - 2 ###########
            MOV R15, FP        ; param 1, x - 2
            ADI R15, #-8
            LDR R3, R15

            MOV R1, SP          ;save current SP into R1 so we can assign it to FP
            MOV R2, SP          ;save sp
            ADI R2, #-16
            CMP R2, SL
            BLT R2, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R1          ;set FP == Former/Original SP

            ADI R3, #-2         ;R3 set above this func call to be original x
            STR R3, SP          ;STORE param-1's value on Stack
            ADI SP, #-4         ;point to next int on stack

            MOV R1, SP          ;save sp - check for stack overflow
            CMP R1, SL
            BLT R1, STACKOVERFLOW
            MOV R1, PC          ;save current PC (which points at next instruction when executing)
            ADI R1, #36
            STR R1, FP
            JMP fib

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R1, FP          ;SP <= FP
            ADI R1, #-4         ;get the PFP

            LDR R6, FP          ;get ret val

            LDR FP, R1          ;FP = PFP
            MOV R2, SP          ;check for stackunderflow
            CMP R2, SB
            BGT R2, STACKUNDERFLOW

            MOV R14, FP         ; put the ret of fib(x-1) on stack
            ADI R14, #-12
            LDR R7, R14         ; R14 should still be pointing to the temp val
            ADD R6, R7          ; should be ok to stomp R6

            LDR R2, FP          ; load ret addr
            MOV R1, R6
            STR R1, FP          ; store ret val where ret addr was

            JMR R2


main        MOV R1, R1
FOR01       LDR R4, i               ; for i; i < 30; i+=2
            CMPI R4, #30
            BRZ R4, ENDFOR01

            TRP #2                  ; get input
            MOV R4, R3              ; don't stomp it
            STR R3, input           ; actually gonna store it for later
            CMPI R4, #-1            ; if it's -1 then move on
            BRZ R4, ENDFOR01

; ################ CALLING FIB ###########
            MOV R1, SP          ;save current SP into R1 so we can assign it to FP
            MOV R2, SP          ;save sp
            ADI R2, #-16
            CMP R2, SL
            BLT R2, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R1          ;set FP == Former/Original SP
            ; param 1, input (in R3)
            STR R3, SP          ;STORE param-1's value on Stack
            ADI SP, #-4         ;point to next int on stack

            MOV R1, SP          ;save sp - check for stack overflow
            CMP R1, SL
            BLT R1, STACKOVERFLOW
            MOV R1, PC          ;save current PC (which points at next instruction when executing
            ADI R1, #36
            STR R1, FP
            JMP fib

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R1, FP          ;SP <= FP
            ADI R1, #-4         ;get the PFP

            ; add x and fib(x) to the ARR
            LDR R7, input       ; get the saved input
            LDR R3, FP          ;get ret val
            LDR R4, i
            MULI R4, #4         ; to go by ints 4 byte
            LDA R5, ARR
            ADD R5, R4
            STR R7, R5          ; put input in ARR
            ADI R5, #4          ; go to next ARR spot
            STR R3, R5          ; put ret val in ARR
            MOV R6, R3          ; and in R6 for later print

            MOVI R3, 'F'        ; printing
            TRP #3
            MOVI R3, 'i'
            TRP #3
            MOVI R3, 'b'
            TRP #3
            MOVI R3, 'o'
            TRP #3
            MOVI R3, 'n'
            TRP #3
            MOVI R3, 'a'
            TRP #3
            MOVI R3, 'c'
            TRP #3
            MOVI R3, 'c'
            TRP #3
            MOVI R3, 'i'
            TRP #3
            MOVI R3, #32
            TRP #3
            MOVI R3, 'o'
            TRP #3
            MOVI R3, 'f'
            TRP #3
            MOVI R3, #32
            TRP #3
            LDR R4, input
            MOV R3, R4
            TRP #1
            MOVI R3, #32
            TRP #3
            MOVI R3, 'i'
            TRP #3
            MOVI R3, 's'
            TRP #3
            MOVI R3, #32
            TRP #3
            MOV R3, R6
            TRP #1
            MOVI R3, #10
            TRP #3

            LDR FP, R1          ;FP = PFP
            MOV R2, SP          ;check for stackunderflow
            CMP R2, SB
            BGT R2, STACKUNDERFLOW


            LDR R4, i           ; increment i and do the loop again
            ADI R4, #2          ; incrementing i by two for keeping track of the ARR
            STR R4, i
            JMP FOR01

ENDFOR01    MOV R1, R1

            MOVI R5, #0         ; not in for loop because I want these to be different every loop
            LDR R6, i           ; this i is how many items there are in ARR
            MOV R7, R6
            DIVI R7, #2
FOR02       LDA R4, ARR         ; getting constant registers ready to use in the loop

            MULI R5, #4
            ADD R4, R5          ; print the thing in the list
            DIVI R5, #4
            LDR R3, R4
            TRP #1
            MOVI R3, ','
            TRP #3
            MOVI R3, #32
            TRP #3

            MOV R8, R5          ; copy i to compare
            CMP R8, R7          ; loop is over if we get to the sorta middle
            BRZ R8, ENDFOR02

            MOV R8, R5          ; to increment i, not super simple
            CMP R8, R7
            BLT R8, FOR02LESS

            ADI R6, #-1         ; decrement size
            SUB R5, R6          ; > MIDDLE so sub from i
            JMP FOR02           ; don't do the next thing

FOR02LESS   ADI R6, #-1         ; dec size still
            ADD R5, R6          ; < MIDDLE so add to i
            JMP FOR02


ENDFOR02    TRP #0

STACKOVERFLOW   TRP #0
STACKUNDERFLOW  TRP #0

; numbers used in loops and ifs
; FOR02
