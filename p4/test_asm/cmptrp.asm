;EQUALTO     .BYT '='
;
;            LDB R3, EQUALTO
;            TRP #3


;ZERO        .BYT '0'
;C_ZERO      .BYT '0'
;
;            LDB R3, ZERO
;            LDB R4, C_ZERO
;            CMP R3, R4
;            TRP #1


;c           .BYT '\n'
;
;PLUS        .BYT '\n'
;
;
;            LDB R4, c
;            LDB R5, PLUS
;            CMP R4, R5          ; if these are equal it's a 0
;
;            MOV R3, R4
;            TRP #1



;a       .BYT 'a'
;
;        MOVI R3, #65
;        TRP #3
;        MOVI R3, #10
;        TRP #3
;        MOVI R3, 'A'
;        TRP #3



;        TRP #4
;        TRP #3

;        TRP #2
;        TRP #1
        TRP #0