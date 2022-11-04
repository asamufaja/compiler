C_ZERO  .BYT '1'

        LDB R3, C_ZERO
        STB R3, SP
        LDR R3, SP
        TRP #3
        ;LDB R4, C_ZERO
        ;CMP R3, R4
        ;TRP #1

;newln   .BYT '\n'
;one     .INT #1
;
;        MOVI R3, 'a'
;        TRP #3
;        MOVI R3, #4
;        TRP #1

;        LDR R3, one     ; this gets stuff out of the stack just fine?
;        STR R3, SP
;        ADI SP, #-4
;        ADI SP, #4
;        LDR R4, SP
;        MOVI R3, #4
;
;        MOV R3, R4
;        TRP #1

        TRP #0