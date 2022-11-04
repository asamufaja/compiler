SIZE        .INT #7
cnt         .INT
tenth       .INT
c           .BYT
            .BYT
            .BYT
            .BYT
            .BYT
            .BYT
            .BYT
data        .INT
flag        .INT
opdv        .INT
newln       .BYT '\n'
PLUS        .BYT '+'
MINUS       .BYT '-'
AT          .BYT '@'
C_ZERO      .BYT '0'
C_ONE       .BYT '1'
C_TWO       .BYT '2'
C_THREE     .BYT '3'
C_FOUR      .BYT '4'
C_FIVE      .BYT '5'
C_SIX       .BYT '6'
C_SEVEN     .BYT '7'
C_EIGHT     .BYT '8'
C_NINE      .BYT '9'

            JMP main

opd         MOV R15, FP         ; block for getting the operands
            ADI R15, #-8
            LDB R4, R15         ; op 1, char s
            ADI R15, #-4
            LDR R5, R15         ; op 2, int k
            ADI R15, #-4
            LDB R6, R15         ; op 3, char j
            ADI R15, #-4

            MOVI R7, #0
            LDR R7, R15         ; temp var t

            ; IF05
            MOV R8, R6          ; copy j
            LDB R9, C_ZERO
            CMP R8, R9
            BNZ R8, ELIF05_01

            MOVI R7, #0
            JMP ENDIF05

ELIF05_01   MOV R8, R6
            LDB R9, C_ONE
            CMP R8, R9
            BNZ R8, ELIF05_02

            MOVI R7, #1
            JMP ENDIF05

ELIF05_02   MOV R8, R6
            LDB R9, C_TWO
            CMP R8, R9
            BNZ R8, ELIF05_03

            MOVI R7, #2
            JMP ENDIF05

ELIF05_03   MOV R8, R6
            LDB R9, C_THREE
            CMP R8, R9
            BNZ R8, ELIF05_04

            MOVI R7, #3
            JMP ENDIF05

ELIF05_04   MOV R8, R6
            LDB R9, C_FOUR
            CMP R8, R9
            BNZ R8, ELIF05_05

            MOVI R7, #4
            JMP ENDIF05

ELIF05_05   MOV R8, R6
            LDB R9, C_FIVE
            CMP R8, R9
            BNZ R8, ELIF05_06

            MOVI R7, #5
            JMP ENDIF05

ELIF05_06   MOV R8, R6
            LDB R9, C_SIX
            CMP R8, R9
            BNZ R8, ELIF05_07

            MOVI R7, #6
            JMP ENDIF05

ELIF05_07   MOV R8, R6
            LDB R9, C_SEVEN
            CMP R8, R9
            BNZ R8, ELIF05_08

            MOVI R7, #7
            JMP ENDIF05

ELIF05_08   MOV R8, R6
            LDB R9, C_EIGHT
            CMP R8, R9
            BNZ R8, ELIF05_09

            MOVI R7, #8
            JMP ENDIF05

ELIF05_09   MOV R8, R6
            LDB R9, C_NINE
            CMP R8, R9
            BNZ R8, ELSE05

            MOVI R7, #9
            JMP ENDIF05

ELSE05      MOV R3, R6          ; put j in R3 to print
            TRP #3
            MOVI R3, 'i'
            TRP #3
            MOVI R3, 's'
            TRP #3
            MOVI R3, #32
            TRP #3
            MOVI R3, 'n'
            TRP #3
            MOVI R3, 'o'
            TRP #3
            MOVI R3, 't'
            TRP #3
            MOVI R3, #32
            TRP #3
            MOVI R3, 'a'
            TRP #3
            MOVI R3, #32
            TRP #3
            MOVI R3, 'n'
            TRP #3
            MOVI R3, 'u'
            TRP #3
            MOVI R3, 'm'
            TRP #3
            MOVI R3, 'b'
            TRP #3
            MOVI R3, 'e'
            TRP #3
            MOVI R3, 'r'
            TRP #3
            MOVI R3, #10
            TRP #3

            MOVI R3, #1
            STR R3, flag

ENDIF05     LDR R3, flag        ; IF06, if flag == 0
            CMPI R3, #0
            BNZ R3, ENDIF06

            LDB R3, PLUS        ; IF07, if s == '+'
            CMP R3, R4          ; s in R4
            BNZ R3, ELSE07

            MUL R7, R5          ; t (R7) *= k (R5)
            JMP ENDIF07

ELSE07      MULI R5, #-1        ; t *= -k
            MUL R7, R5

ENDIF07     LDR R3, opdv        ; opdv += t
            ADD R3, R7
            STR R3, opdv

ENDIF06     LDR R2, FP          ; load ret addr
            STR R1, FP          ; store ret val where ret addr was
            JMR R2


flush       MOV R15, FP

            LDR R4, data        ; data = 0
            MOVI R4, #0
            STR R4, data

            LDA R4, c           ; c[0] = getchar() -> R3 after a TRP #4
            TRP #4
            STB R3, R4

WHILE01     LDB R4, c           ; getting c[0]
            LDB R6, newln       ; getting '\n' to compare
            MOV R5, R4          ; copy R4
            CMP R5, R6
            BRZ R5, ENDWHILE01  ; leave loop if c[0] is \n

            TRP #4
            STB R3, c

            JMP WHILE01

ENDWHILE01  LDR R2, FP          ; load ret addr
            STR R1, FP          ; store ret val where ret addr was
            JMR R2


getdata     MOV R15, FP
            LDR R4, cnt         ; get count and SIZE
            LDR R5, SIZE
            MOV R6, R4          ; copy count
            CMP R6, R5
            BLT R6, IF01        ; if cnt < SIZE

            MOVI R3, 'N'        ; ELSE01
            TRP #3
            MOVI R3, 'u'
            TRP #3
            MOVI R3, 'm'
            TRP #3
            MOVI R3, 'b'
            TRP #3
            MOVI R3, 'e'
            TRP #3
            MOVI R3, 'r'
            TRP #3
            MOVI R3, #32
            TRP #3
            MOVI R3, 'T'
            TRP #3
            MOVI R3, 'o'
            TRP #3
            MOVI R3, 'o'
            TRP #3
            MOVI R3, #32
            TRP #3
            MOVI R3, 'B'
            TRP #3
            MOVI R3, 'i'
            TRP #3
            MOVI R3, 'g'
            TRP #3
            MOVI R3, #10
            TRP #3

; ################# CALL FLUSH #################
            MOV R1, SP          ;save current SP into R1 so we can assign it to FP
            MOV R2, SP          ;save sp
            ADI R2, #-16
            CMP R2, SL
            BLT R2, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R1          ;set FP == Former/Original SP

            MOV R1, SP          ;save sp - check for stack overflow
            CMP R1, SL
            BLT R1, STACKOVERFLOW
            MOV R1, PC          ;save current PC (which points at next instruction when executing
            ADI R1, #36
            STR R1, FP
            JMP flush

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R1, FP          ;SP <= FP
            ADI R1, #-4         ;get the PFP
            LDR FP, R1          ;FP = PFP
            MOV R2, SP          ;check for stackunderflow
            CMP R2, SB
            BGT R2, STACKUNDERFLOW

            JMP ENDIF01

IF01        LDA R5, c           ; get c
            ADD R5, R4          ; R4 is still count, doing c[cnt]
            TRP #4
            STB R3, R5          ; store the thing from TRP #4 (in R3) into c[cnt]
            ADI R4, #1          ; increment count
            STR R4, cnt

ENDIF01     LDR R2, FP          ; load ret addr
            STR R1, FP          ; store ret val where ret addr was
            JMR R2


reset       MOV R15, FP         ; block for getting the operands
            ADI R15, #-8
            LDR R4, R15         ; op 1
            ADI R15, #-4
            LDR R5, R15         ; op 2
            ADI R15, #-4
            LDR R6, R15         ; op 3
            ADI R15, #-4
            LDR R7, R15         ; op 4

            ADI R15, #-4        ; local var k
            MOVI R8, #0
            STR R8, R15

            LDR R10, SIZE       ; stop condition for the for
            MOVI R1, #0         ; the zero for storing in c

FOR01       MOV R9, R8          ; R9 is stomp register
            CMP R9, R10         ; loop until R8 (k) >= R10 (SIZE)
            BRZ R9, ENDFOR01    ; R9 should be zero if k == SIZE

            LDA R9, c
            ADD R9, R8          ; do c[k]
            STB R1, R9          ; R1 previously set as 0

            ADI R8, #1          ; increment k
            JMP FOR01

ENDFOR01    STR R4, data        ; continue with the function
            STR R5, opdv        ; assigning the globals with the passed params
            STR R6, cnt
            STR R7, flag

            LDR R2, FP          ; load ret addr
            STR R1, FP          ; store ret val where ret addr was
            JMR R2

; ############## CALL RESET #################### (FIRST THING IN MAIN)
main        MOV R1, SP          ;save current SP into R1 so we can assign it to FP
            MOV R2, SP          ;save sp
            ADI R2, #-16
            CMP R2, SL
            BLT R2, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R1          ;set FP == Former/Original SP
            MOVI R1, #1         ;R1 == 1  (first param)
            STR R1, SP          ;STORE param-1's value on Stack
            ADI SP, #-4         ;point to next int on stack
            MOVI R1, #0         ;R1 == 0 (second param)
            STR R1, SP          ;STORE param-2's value on Stack
            ADI SP, #-4         ;point to next int on stack
            STR R1, SP          ;third param
            ADI SP, #-4
            STR R1, SP          ;fourth
            ADI SP,  #-4

            MOV R1, SP          ;save sp - check for stack overflow
            CMP R1, SL
            BLT R1, STACKOVERFLOW
            MOV R1, PC          ;save current PC (which points at next instruction when executing
            ADI R1, #36
            STR R1, FP
            JMP reset

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R1, FP          ;SP <= FP
            ADI R1, #-4         ;get the PFP
            LDR FP, R1          ;FP = PFP
            MOV R2, SP          ;check for stackunderflow
            CMP R2, SB
            BGT R2, STACKUNDERFLOW

; ##################### CALL GETDATA #############
            MOV R1, SP          ;save current SP into R1 so we can assign it to FP
            MOV R2, SP          ;save sp
            ADI R2, #-16
            CMP R2, SL
            BLT R2, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R1          ;set FP == Former/Original SP
            ; no params

            MOV R1, SP          ;save sp - check for stack overflow
            CMP R1, SL
            BLT R1, STACKOVERFLOW
            MOV R1, PC          ;save current PC (which points at next instruction when executing
            ADI R1, #36
            STR R1, FP
            JMP getdata

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R1, FP          ;SP <= FP
            ADI R1, #-4         ;get the PFP
            LDR FP, R1          ;FP = PFP
            MOV R2, SP          ;check for stackunderflow
            CMP R2, SB
            BGT R2, STACKUNDERFLOW

            ; START LARGE WHILE
WHILE02     LDB R4, c
            LDB R5, AT        ; @
            CMP R4, R5
            BRZ R4, ENDWHILE02

            LDB R4, c           ; IF02
            LDB R5, PLUS        ; +
            CMP R4, R5          ; if these are equal it's a 0
            LDB R6, c
            LDB R5, MINUS        ; -
            CMP R5, R6          ; if these are equal it's a 0
            ; OR R4, R5 if I do OR if they're both 0 (actually impossible?) it's 0, else it's 1 or -1, not helpful
            AND R4, R5          ; if I do AND then I get a 0 if one or both same (fulfill condition) non 0 otherwise
            BNZ R4, ELSE02

; ############## CALL GETDATA  ##############
            MOV R1, SP          ;save current SP into R1 so we can assign it to FP
            MOV R2, SP          ;save sp
            ADI R2, #-16
            CMP R2, SL
            BLT R2, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R1          ;set FP == Former/Original SP
            ;yeah no params

            MOV R1, SP          ;save sp - check for stack overflow
            CMP R1, SL
            BLT R1, STACKOVERFLOW
            MOV R1, PC          ;save current PC (which points at next instruction when executing
            ADI R1, #36
            STR R1, FP
            JMP getdata

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R1, FP          ;SP <= FP
            ADI R1, #-4         ;get the PFP
            LDR FP, R1          ;FP = PFP
            MOV R2, SP          ;check for stackunderflow
            CMP R2, SB
            BGT R2, STACKUNDERFLOW

            JMP ENDIF02         ; don't go to the else block

ELSE02      LDA R4, c
            ADI R4, #1          ; c[1] ptr
            LDB R5, c
            STB R5, R4          ; c[1] = c[0]

            LDA R4, c
            LDB R5, PLUS
            STB R5, R4          ; c[0] = '+'

            LDR R4, cnt
            ADI R4, #1
            STR R4, cnt         ; cnt++

ENDIF02     MOV R1, R1
WHILE03     LDR R4, data        ; while data != 0
            MOVI R5, #0
            CMP R5, R4
            BRZ R5, ENDWHILE03

            LDA R4, c           ; IF03
            LDR R5, cnt
            ADI R5, #-1
            ADD R4, R5          ; c[cnt - 1]
            LDB R6, R4
            LDB R7, newln
            CMP R6, R7          ; if c[cnt - 1] == '\n'
            BNZ R6, ELSE03      ; if not go on (to call getdata())

            MOVI R4, #0
            STR R4, data        ; data = 0
            MOVI R4, #1
            STR R4, tenth       ; tenth = 0
            LDR R4, cnt
            ADI R4, #-2         ; cnt - 2
            STR R4, cnt         ; cnt = cnt - 2

WHILE04     LDR R4, flag        ; while flag == 0
            CMPI R4, #1         ; so we should only branch if this is zero
            LDR R5, cnt         ; and cnt != 0
            CMPI R5, #0         ; and only branch if this is zero
            AND R4, R5          ;
            BRZ R4, ENDWHILE04  ; and that means end the loop


; ################# CALL OPD  ##################
            MOV R1, SP          ;save current SP into R1 so we can assign it to FP
            MOV R2, SP          ;save sp
            ADI R2, #-16
            CMP R2, SL
            BLT R2, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R1          ;set FP == Former/Original SP
            LDB R1, c           ; first param c[0]
            STB R1, SP          ;STORE param-1's value on Stack
            ADI SP, #-4         ;point to next int on stack
            LDR R1, tenth       ; second param, tenth
            STR R1, SP
            ADI SP, #-4
            LDA R1, c
            LDR R2, cnt
            ADD R1, R2
            LDB R2, R1          ; getting c[cnt]
            STB R2, SP          ;third param
            ADI SP, #-4

            MOV R1, SP          ;save sp - check for stack overflow
            CMP R1, SL
            BLT R1, STACKOVERFLOW
            MOV R1, PC          ;save current PC (which points at next instruction when executing
            ADI R1, #36
            STR R1, FP
            JMP opd

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R1, FP          ;SP <= FP
            ADI R1, #-4         ;get the PFP
            LDR FP, R1          ;FP = PFP
            MOV R2, SP          ;check for stackunderflow
            CMP R2, SB
            BGT R2, STACKUNDERFLOW

            LDR R4, cnt
            ADI R4, #-1
            STR R4, cnt         ; cnt--
            LDR R4, tenth
            MULI R4, #10
            STR R4, tenth       ; tenth *= 10

            JMP WHILE04

ENDWHILE04  LDR R4, flag
            CMPI R4, #0         ; if flag == 0
            BNZ R4, ENDIF04

            MOVI R3, 'O'        ; printing "Operand is {opdv}\n"
            TRP #3
            MOVI R3, 'p'
            TRP #3
            MOVI R3, 'e'
            TRP #3
            MOVI R3, 'r'
            TRP #3
            MOVI R3, 'a'
            TRP #3
            MOVI R3, 'n'
            TRP #3
            MOVI R3, 'd'
            TRP #3
            MOVI R3, #32
            TRP #3
            MOVI R3, 'i'
            TRP #3
            MOVI R3, 's'
            TRP #3
            MOVI R3, #32
            TRP #3
            LDR R3, opdv
            TRP #1
            MOVI R3, #10
            TRP #3

ENDIF04     JMP ENDIF03         ; end of large if
; ############ CALL GETDATA ##############
ELSE03      MOV R1, SP          ;save current SP into R1 so we can assign it to FP
            MOV R2, SP          ;save sp
            ADI R2, #-16
            CMP R2, SL
            BLT R2, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R1          ;set FP == Former/Original SP
            ;yeah no params

            MOV R1, SP          ;save sp - check for stack overflow
            CMP R1, SL
            BLT R1, STACKOVERFLOW
            MOV R1, PC          ;save current PC (which points at next instruction when executing
            ADI R1, #36
            STR R1, FP
            JMP getdata

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R1, FP          ;SP <= FP
            ADI R1, #-4         ;get the PFP
            LDR FP, R1          ;FP = PFP
            MOV R2, SP          ;check for stackunderflow
            CMP R2, SB
            BGT R2, STACKUNDERFLOW
            ; BIG IF BLOCK OVER

ENDIF03     JMP WHILE03

ENDWHILE03  MOV R1, R1          ; END MEDIUM SIZED WHILE
; ############### CALL RESET(1,0,0,0) ############
            MOV R1, SP          ;save current SP into R1 so we can assign it to FP
            MOV R2, SP          ;save sp
            ADI R2, #-16
            CMP R2, SL
            BLT R2, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R1          ;set FP == Former/Original SP
            MOVI R1, #1         ;R1 == 1  (first param)
            STR R1, SP          ;STORE param-1's value on Stack
            ADI SP, #-4         ;point to next int on stack
            MOVI R1, #0         ;R1 == 0 (second param)
            STR R1, SP          ;STORE param-2's value on Stack
            ADI SP, #-4         ;point to next int on stack
            STR R1, SP          ;third param
            ADI SP, #-4
            STR R1, SP          ;fourth
            ADI SP,  #-4        ; second, third, fourth all are just 0

            MOV R1, SP          ;save sp - check for stack overflow
            CMP R1, SL
            BLT R1, STACKOVERFLOW
            MOV R1, PC          ;save current PC (which points at next instruction when executing
            ADI R1, #36
            STR R1, FP
            JMP reset

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R1, FP          ;SP <= FP
            ADI R1, #-4         ;get the PFP
            LDR FP, R1          ;FP = PFP
            MOV R2, SP          ;check for stackunderflow
            CMP R2, SB
            BGT R2, STACKUNDERFLOW

; ############## CALL GETDATA ##############
            MOV R1, SP          ;save current SP into R1 so we can assign it to FP
            MOV R2, SP          ;save sp
            ADI R2, #-16
            CMP R2, SL
            BLT R2, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            MOV FP, R1          ;set FP == Former/Original SP
            ;yeah no params

            MOV R1, SP          ;save sp - check for stack overflow
            CMP R1, SL
            BLT R1, STACKOVERFLOW
            MOV R1, PC          ;save current PC (which points at next instruction when executing
            ADI R1, #36
            STR R1, FP
            JMP getdata

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R1, FP          ;SP <= FP
            ADI R1, #-4         ;get the PFP
            LDR FP, R1          ;FP = PFP
            MOV R2, SP          ;check for stackunderflow
            CMP R2, SB
            BGT R2, STACKUNDERFLOW

            JMP WHILE02

ENDWHILE02  TRP #0          ; END LARGE WHILE ALSO END OF MAIN()


STACKOVERFLOW   TRP #0
STACKUNDERFLOW  TRP #0

; lables used up to:
; FOR01 IF07 WHILE04