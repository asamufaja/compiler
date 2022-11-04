SIZE        .INT #10
ARR         .INT #10
            .INT #2
            .INT #3
            .INT #4
            .INT #15
            .INT #-6
            .INT #7
            .INT #8
            .INT #9
            .INT #10
i           .INT #0
sum         .INT #0
; temp        .INT
result      .INT
is          .BYT 'i'
            .BYT 's'
even        .BYT 'e'
            .BYT 'v'
            .BYT 'e'
            .BYT 'n'
odd         .BYT 'o'
            .BYT 'd'
            .BYT 'd'
newln       .BYT '\n'
space       .BYT '\s'
; comma       .BYT ','
SUM         .BYT 'S'
            .BYT 'u'
            .BYT 'm'
four        .INT #4
two         .INT #2

DAGS        .BYT 'D'
            .BYT 'A'
            .BYT 'G'
            .BYT 'S'
GADS        .INT #-99
rel         .BYT
C_LESS      .BYT '<'
C_GREATER   .BYT '>'
MINUS       .BYT '-'
C_EQUAL     .BYT '='

            JMP MAIN
MAIN        LDR R1, i
            LDR R2, SIZE
            LDR R15, four       ; I should implement a MUL immediate
            LDR R9, sum
            LDR R14, two

WHILE01     MOV R4, R2          ; SIZE to R4 to be compared with i
            CMP R4, R1          ; if i == SIZE
            BRZ R4, WHILE01END  ; gonna leave the loop

            LDA R8, ARR         ; the array
            MOV R6, R1          ; put i in R6
            MUL R6, R15         ; to MUL with #4 to make the offset
            ADD R8, R6          ; to access ARR[i]
            LDR R7, R8          ; getting the value from the pointer ARR[i] (R8) putting in R7
            ADD R9, R7          ; adding that value to sum (R9)
            STR R9, sum         ; storing sum so I can idk

            MOV R4, R7          ; ARR[i] % 2. ARR[i]'s value is at R7 so now it's in R4 too
            DIV R4, R14         ; divide by two
            MUL R4, R14         ; multiply by two
            CMP R4, R7          ; compare from what it was
            BNZ R4, oddbranch   ; if they're not equal, it's odd

            STR R4, result      ; it's even if we're here, put zero in result, it's ARR[i] % 2
            MOV R3, R7          ; print the number
            TRP #1
            LDB R3, space
            TRP #3
            LDA R4, is          ; printing is even
            LDB R3, R4
            TRP #3
            ADI R4, #1          ; just a byte, add 1. (I often forget and add 1 for ints)
            LDB R3, R4
            TRP #3
            LDB R3, space
            TRP #3
            LDA R4, even
            LDB R3, R4
            TRP #3
            ADI R4, #1
            LDB R3, R4
            TRP #3
            ADI R4, #1
            LDB R3, R4
            TRP #3
            ADI R4, #1
            LDB R3, R4
            TRP #3              ; done printing is even
            LDB R3, newln
            TRP #3
            JMP continue        ; skip odd

oddbranch   ADI R4, #2          ; it was -1, now it's one
            STR R4, result      ; putting the 1 in result, it's ARR[i] % 2
            MOV R3, R7
            TRP #1
            LDB R3, space
            TRP #3
            LDA R4, is          ; printing is odd
            LDB R3, R4
            TRP #3
            ADI R4, #1
            LDB R3, R4
            TRP #3
            LDB R3, space
            TRP #3
            LDA R4, odd
            LDB R3, R4
            TRP #3
            ADI R4, #1
            LDB R3, R4
            TRP #3
            ADI R4, #1
            LDB R3, R4
            TRP #3              ; done printing is odd
            LDB R3, newln
            TRP #3

continue    ADI R1, #1          ; increment i
            JMP WHILE01

WHILE01END  LDA R4, SUM         ; printing Sum is 62
            LDB R3, R4
            TRP #3
            ADI R4, #1
            LDB R3, R4
            TRP #3
            ADI R4, #1
            LDB R3, R4
            TRP #3
            LDB R3, space
            TRP #3
            LDA R4, is
            LDB R3, R4
            TRP #3
            ADI R4, #1
            LDB R3, R4
            TRP #3
            LDB R3, space
            TRP #3
            LDR R3, sum
            TRP #1
            LDB R3, newln
            TRP #3
            TRP #3

; PART TWO
            LDR R3, DAGS        ; access DAGS as integer
            STR R3, GADS        ; put in GADS
            LDA R4, GADS        ; address of the D
            ;LDB R3, R4
            ;TRP #3             ; it's a D
            LDA R5, GADS        ; almost the G
            ADI R5, #2          ; address of the G
            LDB R6, R4          ; the D
            LDB R7, R5          ; the G
            STB R6, R5          ; Should be putting a D in the G
            STB R7, R4          ; and a G in the D
            ;LDB R3, R4
            ;TRP #3             ; it's a G

            LDR R1, four
            ADI R1, #-4         ; now it's 0, it will be my new i

WHILE02     MOV R4, R15         ; R15 has the 4
            CMP R4, R1          ; if i is up to 4 now
            BRZ R4, WHILE02END  ; loop ends if i==4

            LDA R5, DAGS        ; PARTS I ADDED FOR RESUBMIT WITH P3 START HERE
            LDA R6, GADS
            ADD R5, R1          ; DAGS[i]
            ADD R6, R1          ; GADS[i]
            ; IF01
            LDB R7, R5          ; DAGS and GADS [i] dereferenced
            LDB R8, R6
            MOV R9, R7
            CMP R9, R8
            BGT R9, GREATERTHAN
            BRZ R9, EQUALTO
            ; if no branch it will just stay here and be LESSTHAN
            LDB R3, C_LESS
            STB R3, rel
            JMP ENDIF01

GREATERTHAN LDB R3, C_GREATER
            STB R3, rel
            JMP ENDIF01

EQUALTO     LDB R3, C_EQUAL
            STB R3, rel
            JMP ENDIF01

ENDIF01     MOV R3, R7          ; print dags[i] ><= gads[i]
            TRP #3
            LDB R3, rel
            TRP #3
            MOV R3, R8
            TRP #3
            LDB R3, MINUS
            TRP #3
            TRP #3


            ADI R1, #1          ; increment i
            JMP WHILE02         ; go back to the while

WHILE02END  LDB R3, newln
            TRP #3
            TRP #3

            LDR R3, DAGS        ; DAGS as int
            TRP #1
            MOV R2, R3          ; save DAGS for later
            LDB R3, space
            TRP #3
            LDB R3, MINUS
            TRP #3
            LDB R3, space
            TRP #3

            LDR R4, GADS        ; GADS as int
            MOV R3, R4
            TRP #1
            LDB R3, space
            TRP #3
            LDB R3, C_EQUAL
            TRP #3

            LDB R3, space
            TRP #3

            MOV R3, R2          ; bring DAGS back
            SUB R3, R4
            TRP #1
            LDB R3, newln
            TRP #3


            TRP #0

;sum should be 62 pretty sure