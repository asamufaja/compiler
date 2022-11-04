A1          .INT    1
A2          .INT    2
A3          .INT    3
A4          .INT    4
A5          .INT    5
A6          .INT    6
B300        .INT    300
B150        .INT    150
B50         .INT    50
B20         .INT    20
B10         .INT    10
B5          .INT    5
C500        .INT    500
C2          .INT    2
C5          .INT    5
C10         .INT    10
B           .BYT    'B'
r           .BYT    'r'
a           .BYT    'a'
n           .BYT    'n'
d           .BYT    'd'
o           .BYT    'o'

S           .BYT    'S'
m           .BYT    'm'
i           .BYT    'i'
t           .BYT    't'
h           .BYT    'h'

space       .BYT    '\s'
comma       .BYT    ','
newln       .BYT    '\n'

            JMP     MAIN

MAIN        LDB R3, S               ; PART ONE
            TRP #3
            LDB R3, m
            TRP #3
            LDB R3, i
            TRP #3
            LDB R3, t
            TRP #3
            LDB R3, h
            TRP #3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            LDB R3, B
            TRP #3
            LDB R3, r
            TRP #3
            LDB R3, a
            TRP #3
            LDB R3, n
            TRP #3
            LDB R3, d
            TRP #3
            LDB R3, o
            TRP #3
            LDB R3, n
            TRP #3
            LDB R3, newln
            TRP #3
            LDB R3, newln
            TRP #3

            LDR R3, B300            ; PART TWO
            LDR R4, B150
            ADD R3, R4
            MOV R2, R3
            TRP #1
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, B50
            ADD R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, B20
            ADD R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, B10
            ADD R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, B5
            ADD R3, R4
            TRP #1
            LDB R3, newln
            TRP #3
            LDB R3, newln
            TRP #3

            LDR R3, A1              ; PART THREE
            LDR R4, A2
            MUL R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, A3
            MUL R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, A4
            MUL R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, A5
            MUL R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, A6
            MUL R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, newln
            TRP #3
            TRP #3

            MOV R3, R2              ; PART FOUR
            LDR R4, B300
            DIV R3, R4              ; so I'm dividing 720 by 300 here? that makes two...
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, B150
            DIV R3, R4              ; all the other divides just get 0. maybe I'm misunderstanding
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, B50
            DIV R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, B20
            DIV R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, B10
            DIV R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, B5
            DIV R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, newln
            TRP #3
            TRP #3

            MOV R3, R2
            LDR R4, C500
            SUB R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, C2
            SUB R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, C5
            SUB R3, R4
            TRP #1
            MOV R2, R3
            LDB R3, comma
            TRP #3
            LDB R3, space
            TRP #3
            MOV R3, R2
            LDR R4, C10
            SUB R3, R4
            TRP #1
            MOV R2, R3


            TRP #0