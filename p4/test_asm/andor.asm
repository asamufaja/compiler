zero    .INT #0
one     .INT #1
newln   .BYT '\n'




        JMP MAIN
MAIN    LDR R4, one
        LDR R5, zero
        ; TRP #99
        AND R4, R5      ; one and zero
        MOV R3, R4      ; put in R3 to print
        TRP #3

        LDB R3, newln   ; do a new line
        TRP #1

        AND R4, R5      ; zero and zero
        MOV R3, R4
        TRP #3          ; still zero

        LDB R3, newln   ; do a new line
        TRP #1

        LDR R4, one
        LDR R5, one
        AND R4, R5
        MOV R3, R4
        TRP #3

        LDB R3, newln   ; do a new line
        TRP #1

        OR  R4, R5      ; one or one
        MOV R3, R4
        TRP #3          ; 1

        LDB R3, newln   ; do a new line
        TRP #1

        LDR R5, zero
        OR  R4, R5      ; one or zero
        MOV R3, R4
        TRP #3          ; 1
        ; TRP #99

        LDB R3, newln   ; do a new line
        TRP #1

        LDB R4, zero
        OR R4, R5
        MOV R3, R4
        TRP #3
        TRP #99

        TRP #0