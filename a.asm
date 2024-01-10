Functions_~newval .INT
endl_Functions_printFail .INT 
f_Functions_printFail .INT 
l_Functions_printFail .INT 
space_Functions_okayYeahButForRealPassing .INT 
endl_Functions_okayYeahButForRealPassing .INT 
s_Functions_okayYeahButForRealPassing .INT 
u_Functions_okayYeahButForRealPassing .INT 
c_Functions_okayYeahButForRealPassing .INT 
e_Functions_okayYeahButForRealPassing .INT 
f_Functions_okayYeahButForRealPassing .INT 
l_Functions_okayYeahButForRealPassing .INT 
ex_Functions_okayYeahButForRealPassing .INT 
passed_Functions_printPassing .INT 
Fibonacci_~newval .INT
comma_Fibonacci_fibonacciSequence .INT 
space_Fibonacci_fibonacciSequence .INT 
temp_Fibonacci_fibonacciSequence .INT 
objectTests_~newval .INT
objectTest_objectTests_objectReturnTest .INT 
objectToTest_~newval .INT
universal_FP .INT	;I'm putting this here to have a safe place to keep FP sometimes
functions .INT
functions_Functions_Functions .INT
fibonacci .INT
fibonacci_Fibonacci_Fibonacci .INT
currentFib .INT 
pastFib1 .INT 
pastFib2 .INT 
B .INT 
B2 .INT 
i .INT 
B3 .INT 
space .INT 
minus .INT 
endl .INT 
s .INT 
mathWithPrecedence .INT 
u .INT 
passingGrade .INT 
c .INT 
e .INT 
nl .INT 
f .INT 
l .INT 
numberOfFibonacciIterations .INT 
comma .INT 
switchTest .INT 
nestedIfAndFibPass .INT 
j .INT 
switchSuccessOneOption .INT 
switchOptionsTaken .INT 
defaultTaken .INT 
objectSuccess .INT 
objectTest .INT
objectTest_objectTests_objectTests .INT
obTest .INT
obTest_objectToTest_objectToTest .INT
JMP main
printFail_Functions MOV R0, R0
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, endl_Functions_printFail
ADI SP, #-4
MOVI R14, #10
LDR R13, endl_Functions_printFail
ADD R13, FP
STR R14, R13
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, f_Functions_printFail
ADI SP, #-4
MOVI R14, 'f'
LDR R13, f_Functions_printFail
ADD R13, FP
STR R14, R13
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, l_Functions_printFail
ADI SP, #-4
MOVI R14, 'l'
LDR R13, l_Functions_printFail
ADD R13, FP
STR R14, R13
LDR R3, endl_Functions_printFail
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, f_Functions_printFail
ADD R3, FP
LDR R3, R3
TRP #3
MOVI R3, 'a'
TRP #3
MOVI R3, 'i'
TRP #3
LDR R3, l_Functions_printFail
ADD R3, FP
LDR R3, R3
TRP #3
MOVI R3, ':'
TRP #3
MOVI R3, '('
TRP #3
LDR R3, endl_Functions_printFail
ADD R3, FP
LDR R3, R3
TRP #3

        LDR R15, FP          ; load ret addr
        JMR R15


passing_Functions MOV R0, R0
IF0start MOV R0, R0

            
            MOV R14, SP          ;save current SP into R14 so we can assign it to FP
            STR R14, universal_FP
            MOV R13, SP          ;save sp
            ADI R13, #56  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R13, SL
            BLT R13, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params

MOV R3, FP
ADI R3, #-8
LDR R3, R3
STR R3, SP
ADI SP, #-4
MOVI R3, #367
STR R3, SP
ADI SP, #-4
MOV R3, FP
ADI R3, #-12
LDR R3, R3
STR R3, SP
ADI SP, #-4
MOV R3, FP
ADI R3, #-16
LDR R3, R3
STR R3, SP
ADI SP, #-4

            LDR R14, universal_FP
            MOV FP, R14          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV R14, SP          ;save sp - check for stack overflow
            CMP R14, SL
            BLT R14, STACKOVERFLOW
            MOV R14, PC          ;save current PC (which points at next instruction when executing
            ADI R14, #36
            STR R14, FP
            JMP okayYeahButForRealPassing_Functions

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R14, FP          ;SP <= FP
            ADI R14, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R12, FP      ;and one for oher uses just in case
        
            LDR FP, R14          ;FP = PFP
            MOV R13, SP          ;check for stackunderflow
            CMP R13, SB
            BGT R13, STACKUNDERFLOW
MOV R15, R12
MOVI R13, 'p'
CMP R15, R13
BRZ R15, equal0
MOVI R15, #0
JMP equal0end
equal0 MOVI R15, #1
equal0end MOV R0, R0
BRZ R15, IF0false
IF0true MOV R0 R0
LDR R12, FP          ; load ret addr
MOVI R3, #8

            MOV R14, R3          ; get ret val
            STR R14, FP          ; store ret val where ret addr was
JMR R12


JMP IF0end
IF0false MOV R0 R0
LDR R15, FP          ; load ret addr
MOVI R12, #0
MOVI R14, #1
SUB R12, R14	;doing SUB with None, expr:num_literal value:1 at:0D1E3E2E0
MOV R3, R12

            MOV R14, R3          ; get ret val
            STR R14, FP          ; store ret val where ret addr was
JMR R15


IF0end MOV R0, R0
okayYeahButForRealPassing_Functions MOV R0, R0
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, space_Functions_okayYeahButForRealPassing
ADI SP, #-4
MOVI R14, #32
LDR R12, space_Functions_okayYeahButForRealPassing
ADD R12, FP
STR R14, R12
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, endl_Functions_okayYeahButForRealPassing
ADI SP, #-4
MOVI R14, #10
LDR R12, endl_Functions_okayYeahButForRealPassing
ADD R12, FP
STR R14, R12
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, s_Functions_okayYeahButForRealPassing
ADI SP, #-4
MOVI R14, 's'
LDR R12, s_Functions_okayYeahButForRealPassing
ADD R12, FP
STR R14, R12
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, u_Functions_okayYeahButForRealPassing
ADI SP, #-4
MOVI R14, 'u'
LDR R12, u_Functions_okayYeahButForRealPassing
ADD R12, FP
STR R14, R12
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, c_Functions_okayYeahButForRealPassing
ADI SP, #-4
MOVI R14, 'c'
LDR R12, c_Functions_okayYeahButForRealPassing
ADD R12, FP
STR R14, R12
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, e_Functions_okayYeahButForRealPassing
ADI SP, #-4
MOVI R14, 'e'
LDR R12, e_Functions_okayYeahButForRealPassing
ADD R12, FP
STR R14, R12
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, f_Functions_okayYeahButForRealPassing
ADI SP, #-4
MOVI R14, 'f'
LDR R12, f_Functions_okayYeahButForRealPassing
ADD R12, FP
STR R14, R12
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, l_Functions_okayYeahButForRealPassing
ADI SP, #-4
MOVI R14, 'l'
LDR R12, l_Functions_okayYeahButForRealPassing
ADD R12, FP
STR R14, R12
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, ex_Functions_okayYeahButForRealPassing
ADI SP, #-4
MOVI R14, '!'
LDR R12, ex_Functions_okayYeahButForRealPassing
ADD R12, FP
STR R14, R12
IF1start MOV R0, R0
MOV R15, FP
ADI R15, #-12
LDR R15, R15
MOVI R14, #367
CMP R15, R14
BRZ R15, equal2
MOVI R15, #0
JMP equal2end
equal2 MOVI R15, #1
equal2end MOV R0, R0
BRZ R15, IF1false
IF1true MOV R0 R0
MOV R3, FP
ADI R3, #-16
LDR R3, R3
TRP #3
MOV R3, FP
ADI R3, #-20
LDR R3, R3
TRP #3
LDR R3, space_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, s_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, u_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, c_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, c_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, e_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, s_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, s_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, f_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, u_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, l_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, ex_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
MOVI R3, '!'
TRP #3
MOVI R3, '!'
TRP #3
LDR R3, endl_Functions_okayYeahButForRealPassing
ADD R3, FP
LDR R3, R3
TRP #3
LDR R14, FP          ; load ret addr
MOVI R3, 'p'

            MOV R12, R3          ; get ret val
            STR R12, FP          ; store ret val where ret addr was
JMR R14


JMP IF1end
IF1false MOV R0 R0
IF1end MOV R0, R0
LDR R15, FP          ; load ret addr
MOVI R3, 'f'

            MOV R14, R3          ; get ret val
            STR R14, FP          ; store ret val where ret addr was
JMR R15


printPassing_Functions MOV R0, R0
MOV R3, FP
MOV R15, SP
SUB R15, R3
STR R15, passed_Functions_printPassing
ADI SP, #-4

            
            MOV R14, SP          ;save current SP into R14 so we can assign it to FP
            STR R14, universal_FP
            MOV R12, SP          ;save sp
            ADI R12, #16  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R12, SL
            BLT R12, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params

MOV R3, FP
ADI R3, #-8
LDR R3, R3
STR R3, SP
ADI SP, #-4
MOV R3, FP
ADI R3, #-16
LDR R3, R3
STR R3, SP
ADI SP, #-4
MOV R3, FP
ADI R3, #-12
LDR R3, R3
STR R3, SP
ADI SP, #-4

            LDR R14, universal_FP
            MOV FP, R14          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV R14, SP          ;save sp - check for stack overflow
            CMP R14, SL
            BLT R14, STACKOVERFLOW
            MOV R14, PC          ;save current PC (which points at next instruction when executing
            ADI R14, #36
            STR R14, FP
            JMP passing_Functions

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R14, FP          ;SP <= FP
            ADI R14, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R13, FP      ;and one for oher uses just in case
        
            LDR FP, R14          ;FP = PFP
            MOV R12, SP          ;check for stackunderflow
            CMP R12, SB
            BGT R12, STACKUNDERFLOW
LDR R12, passed_Functions_printPassing
ADD R12, FP
STR R13, R12
IF2start MOV R0, R0
LDR R15, passed_Functions_printPassing
ADD R15, FP
LDR R15, R15
MOVI R13, #8
CMP R15, R13
BRZ R15, equal4
MOVI R15, #0
JMP equal4end
equal4 MOVI R15, #1
equal4end MOV R0, R0
NOT R15
BRZ R15, IF2false
IF2true MOV R0 R0

            
            MOV R13, SP          ;save current SP into R13 so we can assign it to FP
            STR R13, universal_FP
            MOV R14, SP          ;save sp
            ADI R14, #20  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R14, SL
            BLT R14, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params

MOV R3, FP
ADI R3, #-8
LDR R3, R3
STR R3, SP
ADI SP, #-4

            LDR R13, universal_FP
            MOV FP, R13          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV R13, SP          ;save sp - check for stack overflow
            CMP R13, SL
            BLT R13, STACKOVERFLOW
            MOV R13, PC          ;save current PC (which points at next instruction when executing
            ADI R13, #36
            STR R13, FP
            JMP printFail_Functions

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R13, FP          ;SP <= FP
            ADI R13, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R12, FP      ;and one for oher uses just in case
        
            LDR FP, R13          ;FP = PFP
            MOV R14, SP          ;check for stackunderflow
            CMP R14, SB
            BGT R14, STACKUNDERFLOW
JMP IF2end
IF2false MOV R0 R0
IF2end MOV R0, R0

        LDR R15, FP          ; load ret addr
        JMR R15


Fibonacci_Fibonacci MOV R0, R0
MOVI R15, #0
MOV R12, FP
ADI R12, #-8	;access self in constructor
LDR R12, R12
ADI R12, #0
STR R15, R12
MOVI R15, #1
MOV R12, FP
ADI R12, #-8	;access self in constructor
LDR R12, R12
ADI R12, #4
STR R15, R12
MOV R15, FP
ADI R15, #-12
LDR R15, R15
MOV R12, FP
ADI R12, #-8	;access self in constructor
LDR R12, R12
ADI R12, #8
STR R15, R12
MOVI R15, #0
MOV R12, FP
ADI R12, #-8	;access self in constructor
LDR R12, R12
ADI R12, #12
STR R15, R12
MOV R15, FP
ADI R15, #-16
LDR R15, R15
MOV R12, FP
ADI R12, #-8	;access self in constructor
LDR R12, R12
ADI R12, #20
STR R15, R12

        LDR R15, FP          ; load ret addr
        JMR R15


step_Fibonacci MOV R0, R0
MOV R15, FP
ADI R15, #-8
LDR R15, R15
ADI R15, #0
LDR R15, R15
MOV R3, R15
TRP #1
MOV R15, FP
ADI R15, #-8
LDR R15, R15
ADI R15, #4
LDR R15, R15
MOV R12, FP
ADI R12, #-12
STR R15, R12
IF3start MOV R0, R0
MOV R15, FP
ADI R15, #-8
LDR R15, R15
ADI R15, #12
LDR R15, R15
MOV R12, R15
MOV R14, FP
ADI R14, #-8
LDR R14, R14
ADI R14, #8
LDR R14, R14
MOV R13, R14
MOVI R11, #1
SUB R13, R11	;doing SUB with expr:. value:None at:0D1ED2550, expr:num_literal value:1 at:0D1E55130
MOV R11, R13
CMP R12, R11
BRZ R12, equal6
MOVI R12, #0
JMP equal6end
equal6 MOVI R12, #1
equal6end MOV R0, R0
NOT R12
BRZ R12, IF3false
IF3true MOV R0 R0
MOVI R3, #32
TRP #3
MOV R14, FP
ADI R14, #-8
LDR R14, R14
ADI R14, #4
LDR R14, R14
MOV R15, FP
ADI R15, #-8
LDR R15, R15
ADI R15, #0
LDR R15, R15
MOV R11, R14
MOV R13, R15
ADD R11, R13	;doing ADD with expr:. value:None at:0D1ED2490, expr:. value:None at:0D1ED2430
MOV R3, R11
TRP #1
MOV R13, FP
ADI R13, #-8
LDR R13, R13
ADI R13, #4
LDR R13, R13
MOV R15, FP
ADI R15, #-8
LDR R15, R15
ADI R15, #0
LDR R15, R15
MOV R14, R13
MOV R10, R15
ADD R14, R10	;doing ADD with expr:. value:None at:0D1ED2370, expr:. value:None at:0D1ED2310
MOV R10, FP
ADI R10, #-8	;access self
LDR R10, R10
ADI R10, #4
STR R14, R10
MOV R11, FP
ADI R11, #-12
LDR R11, R11
MOV R10, FP
ADI R10, #-8	;access self
LDR R10, R10
ADI R10, #0
STR R11, R10
JMP IF3end
IF3false MOV R0 R0
IF3end MOV R0, R0

        LDR R12, FP          ; load ret addr
        JMR R12


fibonacciSequence_Fibonacci MOV R0, R0
MOV R3, FP
MOV R12, SP
SUB R12, R3
STR R12, comma_Fibonacci_fibonacciSequence
ADI SP, #-4
MOVI R11, ','
LDR R10, comma_Fibonacci_fibonacciSequence
ADD R10, FP
STR R11, R10
MOV R3, FP
MOV R12, SP
SUB R12, R3
STR R12, space_Fibonacci_fibonacciSequence
ADI SP, #-4
MOVI R11, #32
LDR R10, space_Fibonacci_fibonacciSequence
ADD R10, FP
STR R11, R10
MOV R3, FP
MOV R12, SP
SUB R12, R3
STR R12, temp_Fibonacci_fibonacciSequence
ADI SP, #-4
IF4start MOV R0, R0
MOV R11, FP
ADI R11, #-8
LDR R11, R11
ADI R11, #12
LDR R11, R11
MOV R12, R11
MOV R10, FP
ADI R10, #-8
LDR R10, R10
ADI R10, #8
LDR R10, R10
MOV R14, R10
MOVI R15, #1
SUB R14, R15	;doing SUB with expr:. value:None at:0D1ED2250, expr:num_literal value:1 at:0D1E555E0
MOV R15, R14
CMP R12, R15
BLT R12, less0
MOVI R12, #0
JMP less0end
less0 MOVI R12, #1
less0end MOV R0, R0
BRZ R12, IF4false
IF4true MOV R0 R0

            
            MOV R10, SP          ;save current SP into R10 so we can assign it to FP
            STR R10, universal_FP
            MOV R11, SP          ;save sp
            ADI R11, #12  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R11, SL
            BLT R11, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params

MOV R3, FP
ADI R3, #-8
LDR R3, R3
STR R3, SP
ADI SP, #-4
LDR R3, temp_Fibonacci_fibonacciSequence
ADD R3, FP
LDR R3, R3
STR R3, SP
ADI SP, #-4

            LDR R10, universal_FP
            MOV FP, R10          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV R10, SP          ;save sp - check for stack overflow
            CMP R10, SL
            BLT R10, STACKOVERFLOW
            MOV R10, PC          ;save current PC (which points at next instruction when executing
            ADI R10, #36
            STR R10, FP
            JMP step_Fibonacci

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R10, FP          ;SP <= FP
            ADI R10, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R15, FP      ;and one for oher uses just in case
        
            LDR FP, R10          ;FP = PFP
            MOV R11, SP          ;check for stackunderflow
            CMP R11, SB
            BGT R11, STACKUNDERFLOW
MOV R11, FP
ADI R11, #-8
LDR R11, R11
ADI R11, #12
LDR R11, R11
MOV R10, R11
MOVI R14, #1
ADD R10, R14	;doing ADD with expr:. value:None at:0D1ED27F0, expr:num_literal value:1 at:0D1E55910
MOV R14, FP
ADI R14, #-8	;access self
LDR R14, R14
ADI R14, #12
STR R10, R14
LDR R3, comma_Fibonacci_fibonacciSequence
ADD R3, FP
LDR R3, R3
TRP #3
LDR R3, space_Fibonacci_fibonacciSequence
ADD R3, FP
LDR R3, R3
TRP #3
LDR R15, FP          ; load ret addr

            
            MOV R14, SP          ;save current SP into R14 so we can assign it to FP
            STR R14, universal_FP
            MOV R10, SP          ;save sp
            ADI R10, #20  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R10, SL
            BLT R10, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params

MOV R3, FP
ADI R3, #-8
LDR R3, R3
STR R3, SP
ADI SP, #-4

            LDR R14, universal_FP
            MOV FP, R14          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV R14, SP          ;save sp - check for stack overflow
            CMP R14, SL
            BLT R14, STACKOVERFLOW
            MOV R14, PC          ;save current PC (which points at next instruction when executing
            ADI R14, #36
            STR R14, FP
            JMP fibonacciSequence_Fibonacci

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R14, FP          ;SP <= FP
            ADI R14, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R11, FP      ;and one for oher uses just in case
        
            LDR FP, R14          ;FP = PFP
            MOV R10, SP          ;check for stackunderflow
            CMP R10, SB
            BGT R10, STACKUNDERFLOW
LDR R15, FP
MOV R3, R3

            MOV R10, R3          ; get ret val
            STR R10, FP          ; store ret val where ret addr was
JMR R15


JMP IF4end
IF4false MOV R0 R0
IF4end MOV R0, R0

            
            MOV R12, SP          ;save current SP into R12 so we can assign it to FP
            STR R12, universal_FP
            MOV R15, SP          ;save sp
            ADI R15, #12  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R15, SL
            BLT R15, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params

MOV R3, FP
ADI R3, #-8
LDR R3, R3
STR R3, SP
ADI SP, #-4
LDR R3, temp_Fibonacci_fibonacciSequence
ADD R3, FP
LDR R3, R3
STR R3, SP
ADI SP, #-4

            LDR R12, universal_FP
            MOV FP, R12          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV R12, SP          ;save sp - check for stack overflow
            CMP R12, SL
            BLT R12, STACKOVERFLOW
            MOV R12, PC          ;save current PC (which points at next instruction when executing
            ADI R12, #36
            STR R12, FP
            JMP step_Fibonacci

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R12, FP          ;SP <= FP
            ADI R12, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R10, FP      ;and one for oher uses just in case
        
            LDR FP, R12          ;FP = PFP
            MOV R15, SP          ;check for stackunderflow
            CMP R15, SB
            BGT R15, STACKUNDERFLOW
IF5start MOV R0, R0
CMP R10, R15
BRZ R10, equal8
MOVI R10, #0
JMP equal8end
equal8 MOVI R10, #1
equal8end MOV R0, R0
BRZ R10, IF5false
IF5true MOV R0 R0
IF6start MOV R0, R0
CMP R15, R12
BRZ R15, equal10
MOVI R15, #0
JMP equal10end
equal10 MOVI R15, #1
equal10end MOV R0, R0
CMP R12, R14
BRZ R12, equal11
MOVI R12, #0
JMP equal11end
equal11 MOVI R12, #1
equal11end MOV R0, R0
MOV R14, R15
MOV R13, R12
AND R14, R13	;ANDing None, None
BRZ R14, IF6false
IF6true MOV R0 R0
IF7start MOV R0, R0
MOV R13, FP
ADI R13, #-8
LDR R13, R13
ADI R13, #20
LDR R13, R13
MOV R15, R13
MOVI R14, 'l'
CMP R15, R14
BRZ R15, equal14
MOVI R15, #0
JMP equal14end
equal14 MOVI R15, #1
equal14end MOV R0, R0
NOT R15
BRZ R15, IF7false
IF7true MOV R0 R0

            
            MOV R13, SP          ;save current SP into R13 so we can assign it to FP
            STR R13, universal_FP
            MOV R14, SP          ;save sp
            ADI R14, #20  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R14, SL
            BLT R14, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params

MOV R3, FP
ADI R3, #-8
LDR R3, R3
ADI R3, #0
LDR R3, R3
;idk lel
STR R3, SP
ADI SP, #-4

            LDR R13, universal_FP
            MOV FP, R13          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV R13, SP          ;save sp - check for stack overflow
            CMP R13, SL
            BLT R13, STACKOVERFLOW
            MOV R13, PC          ;save current PC (which points at next instruction when executing
            ADI R13, #36
            STR R13, FP
            JMP printFail_Functions

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R13, FP          ;SP <= FP
            ADI R13, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R9, FP      ;and one for oher uses just in case
        
            LDR FP, R13          ;FP = PFP
            MOV R14, SP          ;check for stackunderflow
            CMP R14, SB
            BGT R14, STACKUNDERFLOW
JMP IF7end
IF7false MOV R0 R0
LDR R15, FP          ; load ret addr
MOV R14, FP
ADI R14, #-8
LDR R14, R14
ADI R14, #8
LDR R14, R14
MOV R9, R14
MOVI R13, #1
CMP R9, R13
BRZ R9, equal16
MOVI R9, #0
JMP equal16end
equal16 MOVI R9, #1
equal16end MOV R0, R0
MOV R14, FP
ADI R14, #-8
LDR R14, R14
ADI R14, #0
LDR R14, R14
MOV R13, R14
MOVI R8, #0
CMP R13, R8
BRZ R13, equal17
MOVI R13, #0
JMP equal17end
equal17 MOVI R13, #1
equal17end MOV R0, R0
MOV R8, R9
MOV R14, R13
AND R8, R14	;ANDing None, None
MOV R13, FP
ADI R13, #-8
LDR R13, R13
ADI R13, #8
LDR R13, R13
MOV R14, R13
MOVI R9, #10
CMP R14, R9
BRZ R14, equal18
MOVI R14, #0
JMP equal18end
equal18 MOVI R14, #1
equal18end MOV R0, R0
MOV R13, FP
ADI R13, #-8
LDR R13, R13
ADI R13, #0
LDR R13, R13
MOV R9, R13
MOVI R7, #34
CMP R9, R7
BRZ R9, equal19
MOVI R9, #0
JMP equal19end
equal19 MOVI R9, #1
equal19end MOV R0, R0
MOV R7, R14
MOV R13, R9
AND R7, R13	;ANDing None, None
MOV R13, R8
MOV R9, R7
OR R13, R9	;ORing None, None
MOV R7, FP
ADI R7, #-8
LDR R7, R7
ADI R7, #8
LDR R7, R7
MOV R9, R7
MOVI R8, #20
CMP R9, R8
BRZ R9, equal20
MOVI R9, #0
JMP equal20end
equal20 MOVI R9, #1
equal20end MOV R0, R0
MOV R7, FP
ADI R7, #-8
LDR R7, R7
ADI R7, #0
LDR R7, R7
MOV R8, R7
MOVI R14, #4181
CMP R8, R14
BRZ R8, equal21
MOVI R8, #0
JMP equal21end
equal21 MOVI R8, #1
equal21end MOV R0, R0
MOV R14, R9
MOV R7, R8
AND R14, R7	;ANDing None, None
MOV R7, R13
MOV R8, R14
OR R7, R8	;ORing None, None
MOV R14, FP
ADI R14, #-8
LDR R14, R14
ADI R14, #8
LDR R14, R14
MOV R8, R14
MOVI R13, #25
CMP R8, R13
BRZ R8, equal22
MOVI R8, #0
JMP equal22end
equal22 MOVI R8, #1
equal22end MOV R0, R0
MOV R14, FP
ADI R14, #-8
LDR R14, R14
ADI R14, #0
LDR R14, R14
MOV R13, R14
MOVI R9, #46368
CMP R13, R9
BRZ R13, equal23
MOVI R13, #0
JMP equal23end
equal23 MOVI R13, #1
equal23end MOV R0, R0
MOV R9, R8
MOV R14, R13
AND R9, R14	;ANDing None, None
MOV R14, R7
MOV R13, R9
OR R14, R13	;ORing None, None
MOV R9, FP
ADI R9, #-8
LDR R9, R9
ADI R9, #8
LDR R9, R9
MOV R13, R9
MOVI R7, #47
CMP R13, R7
BRZ R13, equal24
MOVI R13, #0
JMP equal24end
equal24 MOVI R13, #1
equal24end MOV R0, R0
MOV R9, FP
ADI R9, #-8
LDR R9, R9
ADI R9, #0
LDR R9, R9
MOV R7, R9
MOVI R8, #1836311903
CMP R7, R8
BRZ R7, equal25
MOVI R7, #0
JMP equal25end
equal25 MOVI R7, #1
equal25end MOV R0, R0
MOV R8, R13
MOV R9, R7
AND R8, R9	;ANDing None, None
MOV R9, R14
MOV R7, R8
OR R9, R7	;ORing None, None
MOV R3, R9

            MOV R7, R3          ; get ret val
            STR R7, FP          ; store ret val where ret addr was
JMR R15


IF7end MOV R0, R0
JMP IF6end
IF6false MOV R0 R0
IF6end MOV R0, R0
JMP IF5end
IF5false MOV R0 R0
IF5end MOV R0, R0
LDR R10, FP          ; load ret addr
MOVI R3, #0

            MOV R12, R3          ; get ret val
            STR R12, FP          ; store ret val where ret addr was
JMR R10


objectReturnTest_objectTests MOV R0, R0
MOV R3, FP
MOV R10, SP
SUB R10, R3
STR R10, objectTest_objectTests_objectReturnTest
ADI SP, #-4
ALLC R12, #3
STR R12, objectToTest_~newval

    MOV R15, SP          ;save current SP into R15 so we can assign it to FP
    MOV R7, SP          ;save sp
    ADI R7, #-16
    CMP R7, SL
    BLT R7, STACKOVERFLOW

    ADI SP, #-4         ;reserve space for ret addr on stack
    STR FP, SP          ;store FP => 0, into PFP
    ADI SP, #-4         ;point to next int on stack
    ; params
    ; first one gonna be addr of space on heap
    STR R12, SP
    ADI SP, #-4

    MOV FP, R15          ;set FP == Former/Original SP
    ; put that below params
    MOV R15, SP          ;save sp - check for stack overflow
    CMP R15, SL
    BLT R15, STACKOVERFLOW
    MOV R15, PC          ;save current PC (which points at next instruction when executing
    ADI R15, #36
    STR R15, FP
    JMP objectToTest_objectToTest

    MOV SP, FP          ;get rid of top (no longer needed) frame
    MOV R15, FP          ;SP <= FP
    ADI R15, #-4         ;get the PFP

    LDR R3, FP          ;get ret val to put in frame

    LDR FP, R15          ;FP = PFP
    MOV R7, SP          ;check for stackunderflow
    CMP R7, SB
    BGT R7, STACKUNDERFLOW
LDR R7, objectTest_objectTests_objectReturnTest
ADD R7, FP
LDR R12, objectToTest_~newval
STR R12, R7
LDR R10, FP          ; load ret addr
LDR R3, objectTest_objectTests_objectReturnTest
ADD R3, FP
LDR R3, R3

            MOV R12, R3          ; get ret val
            STR R12, FP          ; store ret val where ret addr was
JMR R10


objectToTest_objectToTest MOV R0, R0
MOVI R10, 'k'
MOV R12, FP
ADI R12, #-8	;access self in constructor
LDR R12, R12
ADI R12, #0
STR R10, R12

        LDR R10, FP          ; load ret addr
        JMR R10


kToJ_objectToTest MOV R0, R0
MOVI R10, 'J'
MOV R12, FP
ADI R12, #-8	;access self
LDR R12, R12
ADI R12, #0
STR R10, R12

        LDR R10, FP          ; load ret addr
        JMR R10


main MOV R0, R0
MOV R10, SP
STR R10, functions
ADI SP, #-4
MOV R10, SP
STR R10, fibonacci
ADI SP, #-4
MOV R10, SP
STR R10, currentFib
ADI SP, #-4
MOVI R12, #0
LDR R7, currentFib
STR R12, R7
MOV R10, SP
STR R10, pastFib1
ADI SP, #-4
MOVI R12, #0
MOVI R7, #1
SUB R12, R7	;doing SUB with None, expr:num_literal value:1 at:0D1E3CAC0
LDR R7, pastFib1
STR R12, R7
MOV R10, SP
STR R10, pastFib2
ADI SP, #-4
MOVI R12, #0
MOVI R7, #2
SUB R12, R7	;doing SUB with None, expr:num_literal value:2 at:0D1E3CC70
LDR R7, pastFib2
STR R12, R7
MOV R10, SP
STR R10, B
ADI SP, #-4
MOVI R12, 'B'
LDR R7, B
STR R12, R7
MOV R10, SP
STR R10, B2
ADI SP, #-4
MOVI R12, 'q'
LDR R7, B2
STR R12, R7
MOV R10, SP
STR R10, i
ADI SP, #-4
MOVI R12, #4
MOVI R7, #2
MUL R12, R7	;doing MUL with expr:num_literal value:4 at:0D1E3CC10, expr:num_literal value:2 at:0D1E3CE80
MOVI R7, #3
MOV R15, R12
ADD R7, R15	;doing ADD with expr:num_literal value:3 at:0D1E3CD30, expr:* value:* at:0D1E3CF10
MOVI R15, #83
MOVI R12, #3
DIV R15, R12	;doing DIV with expr:num_literal value:83 at:0D1E3CCA0, expr:num_literal value:3 at:0D1E3CE50
MOV R12, R7
MOV R9, R15
ADD R12, R9	;doing ADD with expr:+ value:+ at:0D1E3CD90, expr:/ value:/ at:0D1E3CFD0
LDR R9, i
STR R12, R9
MOV R10, SP
STR R10, B3
ADI SP, #-4
MOVI R7, 'r'
LDR R9, B3
STR R7, R9
MOV R10, SP
STR R10, space
ADI SP, #-4
MOVI R7, #32
LDR R9, space
STR R7, R9
MOV R10, SP
STR R10, minus
ADI SP, #-4
MOVI R7, '-'
LDR R9, minus
STR R7, R9
MOV R10, SP
STR R10, endl
ADI SP, #-4
MOVI R7, #10
LDR R9, endl
STR R7, R9
MOV R10, SP
STR R10, s
ADI SP, #-4
MOVI R7, 's'
LDR R9, s
STR R7, R9
MOV R10, SP
STR R10, mathWithPrecedence
ADI SP, #-4
MOVI R7, #0
LDR R9, mathWithPrecedence
STR R7, R9
MOV R10, SP
STR R10, u
ADI SP, #-4
MOVI R7, 'u'
LDR R9, u
STR R7, R9
MOV R10, SP
STR R10, passingGrade
ADI SP, #-4
MOVI R7, #0
LDR R9, passingGrade
STR R7, R9
MOV R10, SP
STR R10, c
ADI SP, #-4
MOVI R7, 'c'
LDR R9, c
STR R7, R9
MOV R10, SP
STR R10, e
ADI SP, #-4
MOVI R7, 'e'
LDR R9, e
STR R7, R9
MOV R10, SP
STR R10, nl
ADI SP, #-4
MOV R10, SP
STR R10, f
ADI SP, #-4
MOVI R7, 'f'
LDR R9, f
STR R7, R9
MOV R10, SP
STR R10, l
ADI SP, #-4
MOVI R7, 'l'
LDR R9, l
STR R7, R9
MOV R10, SP
STR R10, numberOfFibonacciIterations
ADI SP, #-4
MOV R10, SP
STR R10, comma
ADI SP, #-4
MOVI R7, ','
LDR R9, comma
STR R7, R9
MOV R10, SP
STR R10, switchTest
ADI SP, #-4
MOVI R7, '&'
LDR R9, switchTest
STR R7, R9
MOV R10, SP
STR R10, nestedIfAndFibPass
ADI SP, #-4
MOVI R7, #0
LDR R9, nestedIfAndFibPass
STR R7, R9
MOV R10, SP
STR R10, j
ADI SP, #-4
LDR R7, i
LDR R7, R7
MOVI R9, #2
ADD R7, R9	;doing ADD with expr:identifier value:i at:0D1EF0610, expr:num_literal value:2 at:0D1EF04C0
MOVI R9, #0
MOVI R15, #2
SUB R9, R15	;doing SUB with None, expr:num_literal value:2 at:0D1EF0730
LDR R15, i
LDR R15, R15
MOV R12, R9
MUL R15, R12	;doing MUL with expr:identifier value:i at:0D1EF06A0, expr:- value:None at:0D1EF07C0
MOV R12, R7
MOV R9, R15
DIV R12, R9	;doing DIV with expr:+ value:+ at:0D1EF06D0, expr:* value:* at:0D1EF0640
MOVI R9, #0
MOVI R15, #23
SUB R9, R15	;doing SUB with None, expr:num_literal value:23 at:0D1EF0760
MOV R15, R12
MOV R7, R9
ADD R15, R7	;doing ADD with expr:/ value:/ at:0D1EF04F0, expr:- value:None at:0D1EF0790
MOVI R7, #0
MOVI R9, #2
ADD R7, R9	;doing ADD with None, expr:num_literal value:2 at:0D1EF0880
MOV R9, R15
MOV R12, R7
SUB R9, R12	;doing SUB with expr:+ value:+ at:0D1EF0700, expr:+ value:None at:0D1EF08B0
MOVI R12, #0
MOVI R7, #12
SUB R12, R7	;doing SUB with None, expr:num_literal value:12 at:0D1EF0820
MOV R7, R9
MOV R15, R12
ADD R7, R15	;doing ADD with expr:- value:- at:0D1EF08E0, expr:- value:None at:0D1EF0940
LDR R15, j
STR R7, R15
MOV R10, SP
STR R10, switchSuccessOneOption
ADI SP, #-4
MOVI R12, #0
LDR R15, switchSuccessOneOption
STR R12, R15
MOV R10, SP
STR R10, switchOptionsTaken
ADI SP, #-4
MOVI R12, #0
LDR R15, switchOptionsTaken
STR R12, R15
MOV R10, SP
STR R10, defaultTaken
ADI SP, #-4
MOVI R12, #1
LDR R15, defaultTaken
STR R12, R15
MOV R10, SP
STR R10, objectSuccess
ADI SP, #-4
MOVI R12, #0
LDR R15, objectSuccess
STR R12, R15
MOV R10, SP
STR R10, objectTest
ADI SP, #-4
MOV R10, SP
STR R10, obTest
ADI SP, #-4
MOVI R10, #1
MOVI R12, #1
ADD R10, R12	;doing ADD with expr:num_literal value:1 at:0D1E3E430, expr:num_literal value:1 at:0D1EF0C10
MOVI R12, #1
MOVI R15, #1
ADD R12, R15	;doing ADD with expr:num_literal value:1 at:0D1EF0BB0, expr:num_literal value:1 at:0D1EF0CD0
MOV R15, R10
MOV R9, R12
ADD R15, R9	;doing ADD with expr:+ value:+ at:0D1EF0BE0, expr:+ value:+ at:0D1EF0D60
MOVI R9, #1
MOVI R12, #1
ADD R9, R12	;doing ADD with expr:num_literal value:1 at:0D1EF0D90, expr:num_literal value:1 at:0D1EF0CA0
MOVI R12, #1
MOVI R10, #1
ADD R12, R10	;doing ADD with expr:num_literal value:1 at:0D1EF0DF0, expr:num_literal value:1 at:0D1EF0E80
MOV R10, R9
MOV R7, R12
ADD R10, R7	;doing ADD with expr:+ value:+ at:0D1EF0E20, expr:+ value:+ at:0D1EF0F10
MOV R7, R15
MOV R12, R10
ADD R7, R12	;doing ADD with expr:+ value:+ at:0D1EF0D30, expr:+ value:+ at:0D1EF0EE0
MOVI R12, #1
MOVI R10, #1
ADD R12, R10	;doing ADD with expr:num_literal value:1 at:0D1EF0D00, expr:num_literal value:1 at:0D1EF0E50
MOVI R10, #1
MOVI R15, #1
ADD R10, R15	;doing ADD with expr:num_literal value:1 at:0D1EF0F70, expr:num_literal value:1 at:0D1EE9040
MOV R15, R12
MOV R9, R10
ADD R15, R9	;doing ADD with expr:+ value:+ at:0D1EF0FA0, expr:+ value:+ at:0D1EE90D0
MOVI R9, #1
MOVI R10, #1
ADD R9, R10	;doing ADD with expr:num_literal value:1 at:0D1EF0F40, expr:num_literal value:1 at:0D1EE9100
MOVI R10, #1
MOVI R12, #1
ADD R10, R12	;doing ADD with expr:num_literal value:1 at:0D1EE9160, expr:num_literal value:1 at:0D1EE91F0
MOV R12, R9
MOV R8, R10
ADD R12, R8	;doing ADD with expr:+ value:+ at:0D1EE9190, expr:+ value:+ at:0D1EE9280
MOV R8, R15
MOV R10, R12
ADD R8, R10	;doing ADD with expr:+ value:+ at:0D1EE9070, expr:+ value:+ at:0D1EE9250
MOV R10, R7
MOV R12, R8
ADD R10, R12	;doing ADD with expr:+ value:+ at:0D1EF0EB0, expr:+ value:+ at:0D1EE9220
MOVI R12, #1
MOVI R8, #1
ADD R12, R8	;doing ADD with expr:num_literal value:1 at:0D1E3CDC0, expr:num_literal value:1 at:0D1EE91C0
MOVI R8, #1
MOVI R7, #1
ADD R8, R7	;doing ADD with expr:num_literal value:1 at:0D1EE90A0, expr:num_literal value:1 at:0D1EE9340
MOV R7, R12
MOV R15, R8
ADD R7, R15	;doing ADD with expr:+ value:+ at:0D1EE92E0, expr:+ value:+ at:0D1EE93D0
MOVI R15, #1
MOVI R8, #1
ADD R15, R8	;doing ADD with expr:num_literal value:1 at:0D1EE9370, expr:num_literal value:1 at:0D1EE9130
MOVI R8, #1
MOVI R12, #1
ADD R8, R12	;doing ADD with expr:num_literal value:1 at:0D1EE9460, expr:num_literal value:1 at:0D1EE94F0
MOV R12, R15
MOV R9, R8
ADD R12, R9	;doing ADD with expr:+ value:+ at:0D1EE9490, expr:+ value:+ at:0D1EE9580
MOV R9, R7
MOV R8, R12
ADD R9, R8	;doing ADD with expr:+ value:+ at:0D1EE93A0, expr:+ value:+ at:0D1EE9550
MOVI R8, #1
MOVI R12, #1
ADD R8, R12	;doing ADD with expr:num_literal value:1 at:0D1EE9430, expr:num_literal value:1 at:0D1EE92B0
MOVI R12, #1
MOVI R7, #1
ADD R12, R7	;doing ADD with expr:num_literal value:1 at:0D1EE95E0, expr:num_literal value:1 at:0D1EE9670
MOV R7, R8
MOV R15, R12
ADD R7, R15	;doing ADD with expr:+ value:+ at:0D1EE9610, expr:+ value:+ at:0D1EE9700
MOVI R15, #1
MOVI R12, #1
ADD R15, R12	;doing ADD with expr:num_literal value:1 at:0D1EE96A0, expr:num_literal value:1 at:0D1EE9310
MOVI R12, #1
MOVI R8, #1
ADD R12, R8	;doing ADD with expr:num_literal value:1 at:0D1EE9790, expr:num_literal value:1 at:0D1EE9820
MOV R8, R15
MOV R14, R12
ADD R8, R14	;doing ADD with expr:+ value:+ at:0D1EE97C0, expr:+ value:+ at:0D1EE98B0
MOV R14, R7
MOV R12, R8
ADD R14, R12	;doing ADD with expr:+ value:+ at:0D1EE96D0, expr:+ value:+ at:0D1EE9880
MOV R12, R9
MOV R8, R14
ADD R12, R8	;doing ADD with expr:+ value:+ at:0D1EE9520, expr:+ value:+ at:0D1EE9850
MOV R8, R10
MOV R14, R12
ADD R8, R14	;doing ADD with expr:+ value:+ at:0D1EF0DC0, expr:+ value:+ at:0D1EE9760
MOVI R14, #1
MOVI R12, #1
ADD R14, R12	;doing ADD with expr:num_literal value:1 at:0D1EF0C70, expr:num_literal value:1 at:0D1EE98E0
MOVI R12, #1
MOVI R10, #1
ADD R12, R10	;doing ADD with expr:num_literal value:1 at:0D1EE9400, expr:num_literal value:1 at:0D1EE9940
MOV R10, R14
MOV R9, R12
ADD R10, R9	;doing ADD with expr:+ value:+ at:0D1EE94C0, expr:+ value:+ at:0D1EE99D0
MOVI R9, #1
MOVI R12, #1
ADD R9, R12	;doing ADD with expr:num_literal value:1 at:0D1EE9970, expr:num_literal value:1 at:0D1EE9730
MOVI R12, #1
MOVI R14, #1
ADD R12, R14	;doing ADD with expr:num_literal value:1 at:0D1EE9A60, expr:num_literal value:1 at:0D1EE9AF0
MOV R14, R9
MOV R7, R12
ADD R14, R7	;doing ADD with expr:+ value:+ at:0D1EE9A90, expr:+ value:+ at:0D1EE9B80
MOV R7, R10
MOV R12, R14
ADD R7, R12	;doing ADD with expr:+ value:+ at:0D1EE99A0, expr:+ value:+ at:0D1EE9B50
MOVI R12, #1
MOVI R14, #1
ADD R12, R14	;doing ADD with expr:num_literal value:1 at:0D1EE9A30, expr:num_literal value:1 at:0D1EE97F0
MOVI R14, #1
MOVI R10, #1
ADD R14, R10	;doing ADD with expr:num_literal value:1 at:0D1EE9BE0, expr:num_literal value:1 at:0D1EE9C70
MOV R10, R12
MOV R9, R14
ADD R10, R9	;doing ADD with expr:+ value:+ at:0D1EE9C10, expr:+ value:+ at:0D1EE9D00
MOVI R9, #1
MOVI R14, #1
ADD R9, R14	;doing ADD with expr:num_literal value:1 at:0D1EE9CA0, expr:num_literal value:1 at:0D1EE9AC0
MOVI R14, #1
MOVI R12, #1
ADD R14, R12	;doing ADD with expr:num_literal value:1 at:0D1EE9D90, expr:num_literal value:1 at:0D1EE9E20
MOV R12, R9
MOV R15, R14
ADD R12, R15	;doing ADD with expr:+ value:+ at:0D1EE9DC0, expr:+ value:+ at:0D1EE9EB0
MOV R15, R10
MOV R14, R12
ADD R15, R14	;doing ADD with expr:+ value:+ at:0D1EE9CD0, expr:+ value:+ at:0D1EE9E80
MOV R14, R7
MOV R12, R15
ADD R14, R12	;doing ADD with expr:+ value:+ at:0D1EE9B20, expr:+ value:+ at:0D1EE9E50
MOVI R12, #1
MOVI R15, #1
ADD R12, R15	;doing ADD with expr:num_literal value:1 at:0D1EE9BB0, expr:num_literal value:1 at:0D1EE9DF0
MOVI R15, #1
MOVI R7, #1
ADD R15, R7	;doing ADD with expr:num_literal value:1 at:0D1EE95B0, expr:num_literal value:1 at:0D1EE9F70
MOV R7, R12
MOV R10, R15
ADD R7, R10	;doing ADD with expr:+ value:+ at:0D1EE9F10, expr:+ value:+ at:0D1F0C040
MOVI R10, #1
MOVI R15, #1
ADD R10, R15	;doing ADD with expr:num_literal value:1 at:0D1EE9FA0, expr:num_literal value:1 at:0D1F0C070
MOVI R15, #1
MOVI R12, #1
ADD R15, R12	;doing ADD with expr:num_literal value:1 at:0D1F0C0A0, expr:num_literal value:1 at:0D1F0C160
MOV R12, R10
MOV R9, R15
ADD R12, R9	;doing ADD with expr:+ value:+ at:0D1F0C100, expr:+ value:+ at:0D1F0C1F0
MOV R9, R7
MOV R15, R12
ADD R9, R15	;doing ADD with expr:+ value:+ at:0D1EE9FD0, expr:+ value:+ at:0D1F0C1C0
MOVI R15, #1
MOVI R12, #1
ADD R15, R12	;doing ADD with expr:num_literal value:1 at:0D1EE9910, expr:num_literal value:1 at:0D1F0C0D0
MOVI R12, #1
MOVI R7, #1
ADD R12, R7	;doing ADD with expr:num_literal value:1 at:0D1F0C250, expr:num_literal value:1 at:0D1F0C2E0
MOV R7, R15
MOV R10, R12
ADD R7, R10	;doing ADD with expr:+ value:+ at:0D1F0C280, expr:+ value:+ at:0D1F0C370
MOVI R10, #1
MOVI R12, #1
ADD R10, R12	;doing ADD with expr:num_literal value:1 at:0D1F0C310, expr:num_literal value:1 at:0D1F0C190
MOVI R12, #1
MOVI R15, #1
ADD R12, R15	;doing ADD with expr:num_literal value:1 at:0D1F0C400, expr:num_literal value:1 at:0D1F0C490
MOV R15, R10
MOV R13, R12
ADD R15, R13	;doing ADD with expr:+ value:+ at:0D1F0C430, expr:+ value:+ at:0D1F0C520
MOV R13, R7
MOV R12, R15
ADD R13, R12	;doing ADD with expr:+ value:+ at:0D1F0C340, expr:+ value:+ at:0D1F0C4F0
MOV R12, R9
MOV R15, R13
ADD R12, R15	;doing ADD with expr:+ value:+ at:0D1F0C220, expr:+ value:+ at:0D1F0C4C0
MOV R15, R14
MOV R13, R12
ADD R15, R13	;doing ADD with expr:+ value:+ at:0D1EE9D60, expr:+ value:+ at:0D1F0C3D0
MOV R13, R8
MOV R12, R15
ADD R13, R12	;doing ADD with expr:+ value:+ at:0D1EE9640, expr:+ value:+ at:0D1EE9C40
MOVI R12, #1
MOVI R15, #1
ADD R12, R15	;doing ADD with expr:num_literal value:1 at:0D1EE9D30, expr:num_literal value:1 at:0D1F0C460
MOVI R15, #1
MOVI R8, #1
ADD R15, R8	;doing ADD with expr:num_literal value:1 at:0D1F0C550, expr:num_literal value:1 at:0D1F0C580
MOV R8, R12
MOV R14, R15
ADD R8, R14	;doing ADD with expr:+ value:+ at:0D1F0C130, expr:+ value:+ at:0D1F0C610
MOVI R14, #1
MOVI R15, #1
ADD R14, R15	;doing ADD with expr:num_literal value:1 at:0D1F0C640, expr:num_literal value:1 at:0D1F0C3A0
MOVI R15, #1
MOVI R12, #1
ADD R15, R12	;doing ADD with expr:num_literal value:1 at:0D1F0C6A0, expr:num_literal value:1 at:0D1F0C730
MOV R12, R14
MOV R9, R15
ADD R12, R9	;doing ADD with expr:+ value:+ at:0D1F0C6D0, expr:+ value:+ at:0D1F0C7C0
MOV R9, R8
MOV R15, R12
ADD R9, R15	;doing ADD with expr:+ value:+ at:0D1F0C5E0, expr:+ value:+ at:0D1F0C790
MOVI R15, #1
MOVI R12, #1
ADD R15, R12	;doing ADD with expr:num_literal value:1 at:0D1F0C5B0, expr:num_literal value:1 at:0D1F0C700
MOVI R12, #1
MOVI R8, #1
ADD R12, R8	;doing ADD with expr:num_literal value:1 at:0D1F0C820, expr:num_literal value:1 at:0D1F0C8B0
MOV R8, R15
MOV R14, R12
ADD R8, R14	;doing ADD with expr:+ value:+ at:0D1F0C850, expr:+ value:+ at:0D1F0C940
MOVI R14, #1
MOVI R12, #1
ADD R14, R12	;doing ADD with expr:num_literal value:1 at:0D1F0C8E0, expr:num_literal value:1 at:0D1F0C7F0
MOVI R12, #1
MOVI R15, #1
ADD R12, R15	;doing ADD with expr:num_literal value:1 at:0D1F0C9D0, expr:num_literal value:1 at:0D1F0CA60
MOV R15, R14
MOV R7, R12
ADD R15, R7	;doing ADD with expr:+ value:+ at:0D1F0CA00, expr:+ value:+ at:0D1F0CAF0
MOV R7, R8
MOV R12, R15
ADD R7, R12	;doing ADD with expr:+ value:+ at:0D1F0C910, expr:+ value:+ at:0D1F0CAC0
MOV R12, R9
MOV R15, R7
ADD R12, R15	;doing ADD with expr:+ value:+ at:0D1F0C760, expr:+ value:+ at:0D1F0CA90
MOVI R15, #1
MOVI R7, #1
ADD R15, R7	;doing ADD with expr:num_literal value:1 at:0D1F0CB20, expr:num_literal value:1 at:0D1F0CA30
MOVI R7, #1
MOVI R9, #1
ADD R7, R9	;doing ADD with expr:num_literal value:1 at:0D1F0C880, expr:num_literal value:1 at:0D1F0CBB0
MOV R9, R15
MOV R8, R7
ADD R9, R8	;doing ADD with expr:+ value:+ at:0D1F0CB50, expr:+ value:+ at:0D1F0CC40
MOVI R8, #1
MOVI R7, #1
ADD R8, R7	;doing ADD with expr:num_literal value:1 at:0D1F0CBE0, expr:num_literal value:1 at:0D1F0C970
MOVI R7, #1
MOVI R15, #1
ADD R7, R15	;doing ADD with expr:num_literal value:1 at:0D1F0CCD0, expr:num_literal value:1 at:0D1F0CD60
MOV R15, R8
MOV R14, R7
ADD R15, R14	;doing ADD with expr:+ value:+ at:0D1F0CD00, expr:+ value:+ at:0D1F0CDF0
MOV R14, R9
MOV R7, R15
ADD R14, R7	;doing ADD with expr:+ value:+ at:0D1F0CC10, expr:+ value:+ at:0D1F0CDC0
MOVI R7, #1
MOVI R15, #1
ADD R7, R15	;doing ADD with expr:num_literal value:1 at:0D1F0CCA0, expr:num_literal value:1 at:0D1F0C2B0
MOVI R15, #1
MOVI R9, #1
ADD R15, R9	;doing ADD with expr:num_literal value:1 at:0D1F0CE50, expr:num_literal value:1 at:0D1F0CEE0
MOV R9, R7
MOV R8, R15
ADD R9, R8	;doing ADD with expr:+ value:+ at:0D1F0CE80, expr:+ value:+ at:0D1F0CF70
MOVI R8, #1
MOVI R15, #1
ADD R8, R15	;doing ADD with expr:num_literal value:1 at:0D1F0CF10, expr:num_literal value:1 at:0D1F0CD30
MOVI R15, #1
MOVI R7, #1
ADD R15, R7	;doing ADD with expr:num_literal value:1 at:0D1F0C670, expr:num_literal value:1 at:0D1EE60D0
MOV R7, R8
MOV R10, R15
ADD R7, R10	;doing ADD with expr:+ value:+ at:0D1EE6070, expr:+ value:+ at:0D1EE6160
MOV R10, R9
MOV R15, R7
ADD R10, R15	;doing ADD with expr:+ value:+ at:0D1F0CF40, expr:+ value:+ at:0D1EE6130
MOV R15, R14
MOV R7, R10
ADD R15, R7	;doing ADD with expr:+ value:+ at:0D1F0CD90, expr:+ value:+ at:0D1EE6190
MOV R7, R12
MOV R10, R15
ADD R7, R10	;doing ADD with expr:+ value:+ at:0D1F0C9A0, expr:+ value:+ at:0D1F0CFD0
MOVI R10, #1
MOVI R15, #1
ADD R10, R15	;doing ADD with expr:num_literal value:1 at:0D1F0CB80, expr:num_literal value:1 at:0D1F0CEB0
MOVI R15, #1
MOVI R12, #1
ADD R15, R12	;doing ADD with expr:num_literal value:1 at:0D1EE6100, expr:num_literal value:1 at:0D1EE61F0
MOV R12, R10
MOV R14, R15
ADD R12, R14	;doing ADD with expr:+ value:+ at:0D1EE60A0, expr:+ value:+ at:0D1EE6280
MOVI R14, #1
MOVI R15, #1
ADD R14, R15	;doing ADD with expr:num_literal value:1 at:0D1EE62B0, expr:num_literal value:1 at:0D1EE61C0
MOVI R15, #1
MOVI R10, #1
ADD R15, R10	;doing ADD with expr:num_literal value:1 at:0D1EE6310, expr:num_literal value:1 at:0D1EE63A0
MOV R10, R14
MOV R9, R15
ADD R10, R9	;doing ADD with expr:+ value:+ at:0D1EE6340, expr:+ value:+ at:0D1EE6430
MOV R9, R12
MOV R15, R10
ADD R9, R15	;doing ADD with expr:+ value:+ at:0D1EE6250, expr:+ value:+ at:0D1EE6400
MOVI R15, #1
MOVI R10, #1
ADD R15, R10	;doing ADD with expr:num_literal value:1 at:0D1EE6220, expr:num_literal value:1 at:0D1EE6370
MOVI R10, #1
MOVI R12, #1
ADD R10, R12	;doing ADD with expr:num_literal value:1 at:0D1EE6490, expr:num_literal value:1 at:0D1EE6520
MOV R12, R15
MOV R14, R10
ADD R12, R14	;doing ADD with expr:+ value:+ at:0D1EE64C0, expr:+ value:+ at:0D1EE65B0
MOVI R14, #1
MOVI R10, #1
ADD R14, R10	;doing ADD with expr:num_literal value:1 at:0D1EE6550, expr:num_literal value:1 at:0D1EE6460
MOVI R10, #1
MOVI R15, #1
ADD R10, R15	;doing ADD with expr:num_literal value:1 at:0D1EE6640, expr:num_literal value:1 at:0D1EE66D0
MOV R15, R14
MOV R8, R10
ADD R15, R8	;doing ADD with expr:+ value:+ at:0D1EE6670, expr:+ value:+ at:0D1EE6760
MOV R8, R12
MOV R10, R15
ADD R8, R10	;doing ADD with expr:+ value:+ at:0D1EE6580, expr:+ value:+ at:0D1EE6730
MOV R10, R9
MOV R15, R8
ADD R10, R15	;doing ADD with expr:+ value:+ at:0D1EE63D0, expr:+ value:+ at:0D1EE6700
MOVI R15, #1
MOVI R8, #1
ADD R15, R8	;doing ADD with expr:num_literal value:1 at:0D1EE6790, expr:num_literal value:1 at:0D1EE66A0
MOVI R8, #1
MOVI R9, #1
ADD R8, R9	;doing ADD with expr:num_literal value:1 at:0D1EE64F0, expr:num_literal value:1 at:0D1EE6820
MOV R9, R15
MOV R12, R8
ADD R9, R12	;doing ADD with expr:+ value:+ at:0D1EE67C0, expr:+ value:+ at:0D1EE68B0
MOVI R12, #1
MOVI R8, #1
ADD R12, R8	;doing ADD with expr:num_literal value:1 at:0D1EE6850, expr:num_literal value:1 at:0D1EE65E0
MOVI R8, #1
MOVI R15, #1
ADD R8, R15	;doing ADD with expr:num_literal value:1 at:0D1EE6940, expr:num_literal value:1 at:0D1EE69D0
MOV R15, R12
MOV R14, R8
ADD R15, R14	;doing ADD with expr:+ value:+ at:0D1EE6970, expr:+ value:+ at:0D1EE6A60
MOV R14, R9
MOV R8, R15
ADD R14, R8	;doing ADD with expr:+ value:+ at:0D1EE6880, expr:+ value:+ at:0D1EE6A30
MOVI R8, #1
MOVI R15, #1
ADD R8, R15	;doing ADD with expr:num_literal value:1 at:0D1EE6910, expr:num_literal value:1 at:0D1EE6040
MOVI R15, #1
MOVI R9, #1
ADD R15, R9	;doing ADD with expr:num_literal value:1 at:0D1EE6AC0, expr:num_literal value:1 at:0D1EE6B50
MOV R9, R8
MOV R12, R15
ADD R9, R12	;doing ADD with expr:+ value:+ at:0D1EE6AF0, expr:+ value:+ at:0D1EE6BE0
MOVI R12, #1
MOVI R15, #1
ADD R12, R15	;doing ADD with expr:num_literal value:1 at:0D1EE6B80, expr:num_literal value:1 at:0D1EE69A0
MOVI R15, #1
MOVI R8, #1
ADD R15, R8	;doing ADD with expr:num_literal value:1 at:0D1EE6C70, expr:num_literal value:1 at:0D1EE6D00
MOV R8, R12
MOV R6, R15
ADD R8, R6	;doing ADD with expr:+ value:+ at:0D1EE6CA0, expr:+ value:+ at:0D1EE6D90
MOV R6, R9
MOV R15, R8
ADD R6, R15	;doing ADD with expr:+ value:+ at:0D1EE6BB0, expr:+ value:+ at:0D1EE6D60
MOV R15, R14
MOV R8, R6
ADD R15, R8	;doing ADD with expr:+ value:+ at:0D1EE6A00, expr:+ value:+ at:0D1EE6D30
MOV R8, R10
MOV R6, R15
ADD R8, R6	;doing ADD with expr:+ value:+ at:0D1EE6610, expr:+ value:+ at:0D1EE6C40
MOV R6, R7
MOV R15, R8
ADD R6, R15	;doing ADD with expr:+ value:+ at:0D1F0CFA0, expr:+ value:+ at:0D1EE6A90
MOV R15, R13
MOV R8, R6
ADD R15, R8	;doing ADD with expr:+ value:+ at:0D1EE9EE0, expr:+ value:+ at:0D1EE6C10
MOV R3, R15
TRP #1
LDR R3, endl
LDR R3, R3
TRP #3
MOVI R3, 'I'
TRP #3
MOVI R3, 'n'
TRP #3
MOVI R3, 'p'
TRP #3
LDR R3, u
LDR R3, R3
TRP #3
MOVI R3, 't'
TRP #3
LDR R3, space
LDR R3, R3
TRP #3
MOVI R3, 'n'
TRP #3
LDR R3, u
LDR R3, R3
TRP #3
MOVI R3, 'm'
TRP #3
MOVI R3, 'b'
TRP #3
LDR R3, e
LDR R3, R3
TRP #3
LDR R3, B3
LDR R3, R3
TRP #3
LDR R3, space
LDR R3, R3
TRP #3
MOVI R3, 'o'
TRP #3
LDR R3, f
LDR R3, R3
TRP #3
LDR R3, space
LDR R3, R3
TRP #3
MOVI R3, 'i'
TRP #3
MOVI R3, 't'
TRP #3
LDR R3, e
LDR R3, R3
TRP #3
LDR R3, B3
LDR R3, R3
TRP #3
MOVI R3, 'a'
TRP #3
MOVI R3, 't'
TRP #3
MOVI R3, 'i'
TRP #3
MOVI R3, 'o'
TRP #3
MOVI R3, 'n'
TRP #3
LDR R3, s
LDR R3, R3
TRP #3
MOVI R3, #32
TRP #3
MOVI R3, '('
TRP #3
MOVI R3, '-'
TRP #3
MOVI R3, '1'
TRP #3
MOVI R3, ','
TRP #3
MOVI R3, #32
TRP #3
MOVI R3, '1'
TRP #3
MOVI R3, ','
TRP #3
MOVI R3, #32
TRP #3
MOVI R3, '1'
TRP #3
MOVI R3, '0'
TRP #3
MOVI R3, ','
TRP #3
MOVI R3, #32
TRP #3
MOVI R3, '2'
TRP #3
MOVI R3, '0'
TRP #3
MOVI R3, ','
TRP #3
MOVI R3, #32
TRP #3
MOVI R3, '2'
TRP #3
MOVI R3, '5'
TRP #3
MOVI R3, ','
TRP #3
MOVI R3, #32
TRP #3
MOVI R3, '4'
TRP #3
MOVI R3, '7'
TRP #3
MOVI R3, ')'
TRP #3
MOVI R3, ':'
TRP #3
LDR R3, endl
LDR R3, R3
TRP #3
TRP #2
LDR R15, numberOfFibonacciIterations
STR R3, R15
LDR R3, numberOfFibonacciIterations
LDR R3, R3
TRP #1
LDR R3, endl
LDR R3, R3
TRP #3
IF8start MOV R0, R0
LDR R15, numberOfFibonacciIterations
LDR R15, R15
MOVI R8, #0
CMP R15, R8
BGT R15, great0
MOVI R15, #0
JMP great0end
great0 MOVI R15, #1
great0end MOV R0, R0
LDR R8, numberOfFibonacciIterations
LDR R8, R8
MOVI R6, #0
CMP R8, R6
BRZ R8, equal26
MOVI R8, #0
JMP equal26end
equal26 MOVI R8, #1
equal26end MOV R0, R0
MOV R6, R15
MOV R13, R8
OR R6, R13	;ORing None, None
BRZ R6, IF8false
IF8true MOV R0 R0
MOVI R15, #0
LDR R13, nestedIfAndFibPass
STR R15, R13
ALLC R13, #9
STR R13, Fibonacci_~newval

    MOV R15, SP          ;save current SP into R15 so we can assign it to FP
    MOV R6, SP          ;save sp
    ADI R6, #-16
    CMP R6, SL
    BLT R6, STACKOVERFLOW

    ADI SP, #-4         ;reserve space for ret addr on stack
    STR FP, SP          ;store FP => 0, into PFP
    ADI SP, #-4         ;point to next int on stack
    ; params
    ; first one gonna be addr of space on heap
    STR R13, SP
    ADI SP, #-4
LDR R3, numberOfFibonacciIterations
LDR R3, R3
STR R3, SP
ADI SP, #-4
LDR R3, l
LDR R3, R3
STR R3, SP
ADI SP, #-4

    MOV FP, R15          ;set FP == Former/Original SP
    ; put that below params
    MOV R15, SP          ;save sp - check for stack overflow
    CMP R15, SL
    BLT R15, STACKOVERFLOW
    MOV R15, PC          ;save current PC (which points at next instruction when executing
    ADI R15, #36
    STR R15, FP
    JMP Fibonacci_Fibonacci

    MOV SP, FP          ;get rid of top (no longer needed) frame
    MOV R15, FP          ;SP <= FP
    ADI R15, #-4         ;get the PFP

    LDR R3, FP          ;get ret val to put in frame

    LDR FP, R15          ;FP = PFP
    MOV R6, SP          ;check for stackunderflow
    CMP R6, SB
    BGT R6, STACKUNDERFLOW
LDR R13, Fibonacci_~newval
STR R13, fibonacci
STR R13, fibonacci_Fibonacci_Fibonacci

            
            MOV R13, SP          ;save current SP into R13 so we can assign it to FP
            STR R13, universal_FP
            MOV R6, SP          ;save sp
            ADI R6, #20  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R6, SL
            BLT R6, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params

LDR R3, fibonacci
STR R3, SP
ADI SP, #-4

            LDR R13, universal_FP
            MOV FP, R13          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV R13, SP          ;save sp - check for stack overflow
            CMP R13, SL
            BLT R13, STACKOVERFLOW
            MOV R13, PC          ;save current PC (which points at next instruction when executing
            ADI R13, #36
            STR R13, FP
            JMP fibonacciSequence_Fibonacci

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R13, FP          ;SP <= FP
            ADI R13, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R15, FP      ;and one for oher uses just in case
        
            LDR FP, R13          ;FP = PFP
            MOV R6, SP          ;check for stackunderflow
            CMP R6, SB
            BGT R6, STACKUNDERFLOW
LDR R6, nestedIfAndFibPass
STR R15, R6
LDR R3, endl
LDR R3, R3
TRP #3
TRP #2
LDR R6, numberOfFibonacciIterations
STR R3, R6
LDR R3, numberOfFibonacciIterations
LDR R3, R3
TRP #1
LDR R3, endl
LDR R3, R3
TRP #3
LDR R6, numberOfFibonacciIterations
LDR R6, R6
MOVI R13, #0
CMP R6, R13
BGT R6, great1
MOVI R6, #0
JMP great1end
great1 MOVI R6, #1
great1end MOV R0, R0
LDR R13, numberOfFibonacciIterations
LDR R13, R13
MOVI R8, #0
CMP R13, R8
BRZ R13, equal27
MOVI R13, #0
JMP equal27end
equal27 MOVI R13, #1
equal27end MOV R0, R0
MOV R8, R6
MOV R15, R13
OR R8, R15	;ORing None, None
BGT R8, IF8true
IF8false MOV R0 R0
IF8end MOV R0, R0
LDR R3, endl
LDR R3, R3
TRP #3
MOVI R3, #10
TRP #3
LDR R3, switchTest
LDR R3, R3
TRP #3
LDR R3, endl
LDR R3, R3
TRP #3
MOVI R3, 'i'
TRP #3
MOVI R3, 'n'
TRP #3
MOVI R3, 'p'
TRP #3
LDR R3, u
LDR R3, R3
TRP #3
MOVI R3, 't'
TRP #3
LDR R3, space
LDR R3, R3
TRP #3
LDR R3, c
LDR R3, R3
TRP #3
MOVI R8, 'h'
LDR R6, c
STR R8, R6
LDR R3, c
LDR R3, R3
TRP #3
MOVI R6, 'c'
LDR R8, c
STR R6, R8
MOVI R3, 'a'
TRP #3
LDR R3, B3
LDR R3, R3
TRP #3
MOVI R3, ':'
TRP #3
LDR R3, endl
LDR R3, R3
TRP #3
TRP #4
LDR R8, switchTest
STB R3, R8
TRP #4
LDR R8, nl
STB R3, R8
LDR R3, switchTest
LDR R3, R3
TRP #3
LDR R3, nl
LDR R3, R3
TRP #3
LDR R3, endl
LDR R3, R3
TRP #3
SWITCH0start MOV R0, R0
LDR R8, switchTest
LDR R8, R8
CMPI R8, 'a'
BRZ R8, SWITCH0case'a'
LDR R8, switchTest
LDR R8, R8
CMPI R8, 'z'
BRZ R8, SWITCH0case'z'
LDR R8, switchTest
LDR R8, R8
CMPI R8, 'l'
BRZ R8, SWITCH0case'l'
JMP DEFAULT0start
SWITCH0case'a' MOV R0, R0
MOVI R3, 's'
TRP #3
MOVI R3, 't'
TRP #3
MOVI R3, 'a'
TRP #3
MOVI R3, 'r'
TRP #3
MOVI R3, 't'
TRP #3
MOVI R3, #10
TRP #3
IF9start MOV R0, R0
LDR R8, switchSuccessOneOption
LDR R8, R8
CMP R8, R6
BRZ R8, equal28
MOVI R8, #0
JMP equal28end
equal28 MOVI R8, #1
equal28end MOV R0, R0
BRZ R8, IF9false
IF9true MOV R0 R0
MOVI R6, #0
LDR R15, switchSuccessOneOption
STR R6, R15
JMP IF9end
IF9false MOV R0 R0
MOVI R8, #1
LDR R15, switchSuccessOneOption
STR R8, R15
IF9end MOV R0, R0
MOVI R15, #0
LDR R8, defaultTaken
STR R15, R8
LDR R8, switchOptionsTaken
LDR R8, R8
MOVI R15, #1
ADD R8, R15	;doing ADD with expr:identifier value:switchOptionsTaken at:0D1E97460, expr:num_literal value:1 at:0D1E974F0
LDR R15, switchOptionsTaken
STR R8, R15
JMP SWITCH0end
SWITCH0case'z' MOV R0, R0
MOVI R3, 'e'
TRP #3
MOVI R3, 'n'
TRP #3
MOVI R3, 'd'
TRP #3
MOVI R3, #10
TRP #3
IF10start MOV R0, R0
LDR R15, switchSuccessOneOption
LDR R15, R15
CMP R15, R8
BRZ R15, equal30
MOVI R15, #0
JMP equal30end
equal30 MOVI R15, #1
equal30end MOV R0, R0
BRZ R15, IF10false
IF10true MOV R0 R0
MOVI R8, #0
LDR R6, switchSuccessOneOption
STR R8, R6
JMP IF10end
IF10false MOV R0 R0
MOVI R15, #1
LDR R6, switchSuccessOneOption
STR R15, R6
IF10end MOV R0, R0
MOVI R6, #0
LDR R15, defaultTaken
STR R6, R15
LDR R15, switchOptionsTaken
LDR R15, R15
MOVI R6, #1
ADD R15, R6	;doing ADD with expr:identifier value:switchOptionsTaken at:0D1E97940, expr:num_literal value:1 at:0D1E97B50
LDR R6, switchOptionsTaken
STR R15, R6
JMP SWITCH0end
SWITCH0case'l' MOV R0, R0
MOVI R3, 'e'
TRP #3
LDR R3, l
LDR R3, R3
TRP #3
LDR R3, e
LDR R3, R3
TRP #3
MOVI R3, 'm'
TRP #3
MOVI R3, 'i'
TRP #3
MOVI R3, 'o'
TRP #3
MOVI R3, 'p'
TRP #3
MOVI R3, 'e'
TRP #3
MOVI R3, 'e'
TRP #3
LDR R3, endl
LDR R3, R3
TRP #3
IF11start MOV R0, R0
LDR R6, switchSuccessOneOption
LDR R6, R6
CMP R6, R15
BRZ R6, equal32
MOVI R6, #0
JMP equal32end
equal32 MOVI R6, #1
equal32end MOV R0, R0
BRZ R6, IF11false
IF11true MOV R0 R0
MOVI R15, #0
LDR R8, switchSuccessOneOption
STR R15, R8
JMP IF11end
IF11false MOV R0 R0
MOVI R6, #1
LDR R8, switchSuccessOneOption
STR R6, R8
IF11end MOV R0, R0
MOVI R8, #0
LDR R6, defaultTaken
STR R8, R6
LDR R6, switchOptionsTaken
LDR R6, R6
MOVI R8, #1
ADD R6, R8	;doing ADD with expr:identifier value:switchOptionsTaken at:0D1E775B0, expr:num_literal value:1 at:0D1E77640
LDR R8, switchOptionsTaken
STR R6, R8
JMP SWITCH0end
DEFAULT0start MOV R0, R0
SWITCH1start MOV R0, R0
LDR R8, switchTest
LDR R8, R8
CMPI R8, 'x'
BRZ R8, SWITCH1case'x'
JMP DEFAULT1start
SWITCH1case'x' MOV R0, R0
MOVI R3, 'x'
TRP #3
LDR R3, minus
LDR R3, R3
TRP #3
MOVI R3, 'r'
TRP #3
MOVI R3, 'a'
TRP #3
MOVI R3, 'y'
TRP #3
LDR R3, endl
LDR R3, R3
TRP #3
JMP SWITCH1end
DEFAULT1start MOV R0, R0
JMP SWITCH1end
SWITCH1end MOV R0, R0
SWITCH0end MOV R0, R0
LDR R3, nl
LDR R3, R3
TRP #3
LDR R3, nl
LDR R3, R3
TRP #3
LDR R3, B2
LDR R3, R3
TRP #3
LDR R3, B3
LDR R3, R3
TRP #3
LDR R8, B3
LDR R6, B
LDR R6, R6
STR R6, R8
LDR R6, B2
LDR R8, B
LDR R8, R8
STR R8, R6
MOVI R3, #9
TRP #3
LDR R3, B2
LDR R3, R3
TRP #3
LDR R3, B3
LDR R3, R3
TRP #3
MOVI R3, #10
TRP #3
LDR R3, i
LDR R3, R3
TRP #1
LDR R3, endl
LDR R3, R3
TRP #3
LDR R3, j
LDR R3, R3
TRP #1
LDR R3, nl
LDR R3, R3
TRP #3
IF12start MOV R0, R0
LDR R8, i
LDR R8, R8
MOVI R6, #38
CMP R8, R6
BRZ R8, equal34
MOVI R8, #0
JMP equal34end
equal34 MOVI R8, #1
equal34end MOV R0, R0
BRZ R8, IF12false
IF12true MOV R0 R0
IF13start MOV R0, R0
LDR R6, j
LDR R6, R6
MOVI R15, #0
MOVI R13, #38
SUB R15, R13	;doing SUB with None, expr:num_literal value:38 at:0D1E89160
MOV R13, R15
CMP R6, R13
BRZ R6, equal36
MOVI R6, #0
JMP equal36end
equal36 MOVI R6, #1
equal36end MOV R0, R0
BRZ R6, IF13false
IF13true MOV R0 R0
LDR R15, j
LDR R15, R15
MOVI R13, #1
ADD R15, R13	;doing ADD with expr:identifier value:j at:0D1E89250, expr:num_literal value:1 at:0D1E89280
LDR R13, j
STR R15, R13
JMP IF13end
IF13false MOV R0 R0
IF13end MOV R0, R0
IF14start MOV R0, R0
LDR R6, j
LDR R6, R6
MOVI R13, #0
MOVI R15, #37
SUB R13, R15	;doing SUB with None, expr:num_literal value:37 at:0D1E89130
MOV R15, R13
CMP R6, R15
BRZ R6, equal38
MOVI R6, #0
JMP equal38end
equal38 MOVI R6, #1
equal38end MOV R0, R0
BRZ R6, IF14false
IF14true MOV R0 R0
MOVI R13, #40
MOVI R15, #9
SUB R13, R15	;doing SUB with expr:num_literal value:40 at:0D1E89640, expr:num_literal value:9 at:0D1E896D0
MOVI R15, #44
MOV R7, R13
DIV R15, R7	;doing DIV with expr:num_literal value:44 at:0D1E895B0, expr:- value:- at:0D1E89760
MOVI R7, #0
MOVI R13, #5
ADD R7, R13	;doing ADD with None, expr:num_literal value:5 at:0D1E89580
MOVI R13, #0
MOVI R10, #5
SUB R13, R10	;doing SUB with None, expr:num_literal value:5 at:0D1E89550
MOV R10, R7
MOV R14, R13
SUB R10, R14	;doing SUB with expr:+ value:None at:0D1E896A0, expr:- value:None at:0D1E89850
MOV R14, R15
MOV R13, R10
ADD R14, R13	;doing ADD with expr:/ value:/ at:0D1E89730, expr:- value:- at:0D1E89670
LDR R13, j
LDR R13, R13
MOV R10, R14
MUL R13, R10	;doing MUL with expr:identifier value:j at:0D1E89520, expr:+ value:+ at:0D1E897C0
LDR R10, i
LDR R10, R10
MOV R14, R13
MUL R10, R14	;doing MUL with expr:identifier value:i at:0D1E89490, expr:* value:* at:0D1E89880
LDR R14, j
STR R10, R14
JMP IF14end
IF14false MOV R0 R0
IF14end MOV R0, R0
IF15start MOV R0, R0
LDR R6, j
LDR R6, R6
MOVI R14, #0
MOVI R10, #15466
SUB R14, R10	;doing SUB with None, expr:num_literal value:15466 at:0D1E894C0
MOV R10, R14
CMP R6, R10
BRZ R6, equal40
MOVI R6, #0
JMP equal40end
equal40 MOVI R6, #1
equal40end MOV R0, R0
BRZ R6, IF15false
IF15true MOV R0 R0
MOVI R14, #1
LDR R10, mathWithPrecedence
STR R14, R10
JMP IF15end
IF15false MOV R0 R0
IF15end MOV R0, R0
LDR R3, j
LDR R3, R3
TRP #1
LDR R3, endl
LDR R3, R3
TRP #3
JMP IF12end
IF12false MOV R0 R0
IF12end MOV R0, R0
IF16start MOV R0, R0
LDR R8, obTest
ADI R8, #0
LDR R8, R8
MOV R6, R8
MOVI R14, 'k'
CMP R6, R14
BRZ R6, equal42
MOVI R6, #0
JMP equal42end
equal42 MOVI R6, #1
equal42end MOV R0, R0
BRZ R6, IF16false
IF16true MOV R0 R0

            
            MOV R8, SP          ;save current SP into R8 so we can assign it to FP
            STR R8, universal_FP
            MOV R14, SP          ;save sp
            ADI R14, #8  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R14, SL
            BLT R14, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params

LDR R3, obTest
STR R3, SP
ADI SP, #-4

            LDR R8, universal_FP
            MOV FP, R8          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV R8, SP          ;save sp - check for stack overflow
            CMP R8, SL
            BLT R8, STACKOVERFLOW
            MOV R8, PC          ;save current PC (which points at next instruction when executing
            ADI R8, #36
            STR R8, FP
            JMP kToJ_objectToTest

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R8, FP          ;SP <= FP
            ADI R8, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R13, FP      ;and one for oher uses just in case
        
            LDR FP, R8          ;FP = PFP
            MOV R14, SP          ;check for stackunderflow
            CMP R14, SB
            BGT R14, STACKUNDERFLOW
IF17start MOV R0, R0
LDR R14, obTest
ADI R14, #0
LDR R14, R14
MOV R13, R14
MOVI R8, 'J'
CMP R13, R8
BRZ R13, equal44
MOVI R13, #0
JMP equal44end
equal44 MOVI R13, #1
equal44end MOV R0, R0
BRZ R13, IF17false
IF17true MOV R0 R0
MOVI R14, #1
LDR R8, objectSuccess
STR R14, R8
JMP IF17end
IF17false MOV R0 R0
IF17end MOV R0, R0
JMP IF16end
IF16false MOV R0 R0
IF16end MOV R0, R0
IF18start MOV R0, R0
LDR R6, nestedIfAndFibPass
LDR R6, R6
CMP R6, R13
BRZ R6, equal46
MOVI R6, #0
JMP equal46end
equal46 MOVI R6, #1
equal46end MOV R0, R0
LDR R13, mathWithPrecedence
LDR R13, R13
CMP R13, R8
BRZ R13, equal47
MOVI R13, #0
JMP equal47end
equal47 MOVI R13, #1
equal47end MOV R0, R0
MOV R8, R6
MOV R14, R13
AND R8, R14	;ANDing None, None
LDR R14, objectSuccess
LDR R14, R14
CMP R14, R13
BRZ R14, equal48
MOVI R14, #0
JMP equal48end
equal48 MOVI R14, #1
equal48end MOV R0, R0
MOV R13, R8
MOV R6, R14
AND R13, R6	;ANDing None, None
LDR R6, switchSuccessOneOption
LDR R6, R6
CMP R6, R14
BRZ R6, equal49
MOVI R6, #0
JMP equal49end
equal49 MOVI R6, #1
equal49end MOV R0, R0
LDR R14, defaultTaken
LDR R14, R14
CMP R14, R8
BRZ R14, equal50
MOVI R14, #0
JMP equal50end
equal50 MOVI R14, #1
equal50end MOV R0, R0
MOV R8, R6
MOV R15, R14
AND R8, R15	;ANDing None, None
LDR R15, switchOptionsTaken
LDR R15, R15
MOVI R14, #1
CMP R15, R14
BRZ R15, equal51
MOVI R15, #0
JMP equal51end
equal51 MOVI R15, #1
equal51end MOV R0, R0
MOV R14, R8
MOV R6, R15
AND R14, R6	;ANDing None, None
LDR R6, switchSuccessOneOption
LDR R6, R6
CMP R6, R15
BRZ R6, equal52
MOVI R6, #0
JMP equal52end
equal52 MOVI R6, #1
equal52end MOV R0, R0
LDR R15, defaultTaken
LDR R15, R15
CMP R15, R8
BRZ R15, equal53
MOVI R15, #0
JMP equal53end
equal53 MOVI R15, #1
equal53end MOV R0, R0
MOV R8, R6
MOV R7, R15
AND R8, R7	;ANDing None, None
LDR R7, switchOptionsTaken
LDR R7, R7
MOVI R15, #0
CMP R7, R15
BRZ R7, equal54
MOVI R7, #0
JMP equal54end
equal54 MOVI R7, #1
equal54end MOV R0, R0
MOV R15, R8
MOV R6, R7
AND R15, R6	;ANDing None, None
MOV R6, R14
MOV R7, R15
OR R6, R7	;ORing None, None
MOV R7, R13
MOV R15, R6
AND R7, R15	;ANDing None, None
BRZ R7, IF18false
IF18true MOV R0 R0
MOVI R14, #1
LDR R7, passingGrade
STR R14, R7
JMP IF18end
IF18false MOV R0 R0
IF18end MOV R0, R0
IF19start MOV R0, R0
LDR R8, passingGrade
LDR R8, R8
CMP R8, R7
BRZ R8, equal64
MOVI R8, #0
JMP equal64end
equal64 MOVI R8, #1
equal64end MOV R0, R0
BRZ R8, IF19false
IF19true MOV R0 R0

            
            MOV R7, SP          ;save current SP into R7 so we can assign it to FP
            STR R7, universal_FP
            MOV R14, SP          ;save sp
            ADI R14, #20  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R14, SL
            BLT R14, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params

LDR R3, functions
STR R3, SP
ADI SP, #-4
LDR R3, B2
LDR R3, R3
STR R3, SP
ADI SP, #-4
LDR R3, nl
LDR R3, R3
STR R3, SP
ADI SP, #-4

            LDR R7, universal_FP
            MOV FP, R7          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV R7, SP          ;save sp - check for stack overflow
            CMP R7, SL
            BLT R7, STACKOVERFLOW
            MOV R7, PC          ;save current PC (which points at next instruction when executing
            ADI R7, #36
            STR R7, FP
            JMP printPassing_Functions

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R7, FP          ;SP <= FP
            ADI R7, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R15, FP      ;and one for oher uses just in case
        
            LDR FP, R7          ;FP = PFP
            MOV R14, SP          ;check for stackunderflow
            CMP R14, SB
            BGT R14, STACKUNDERFLOW
JMP IF19end
IF19false MOV R0 R0

            
            MOV R8, SP          ;save current SP into R8 so we can assign it to FP
            STR R8, universal_FP
            MOV R15, SP          ;save sp
            ADI R15, #20  ; one int for every param and every local var and one for PFP one for ret addr/val
            CMP R15, SL
            BLT R15, STACKOVERFLOW

            ADI SP, #-4         ;reserve space for ret addr on stack
            STR FP, SP          ;store FP => 0, into PFP
            ADI SP, #-4         ;point to next int on stack
            ; params

LDR R3, functions
STR R3, SP
ADI SP, #-4

            LDR R8, universal_FP
            MOV FP, R8          ;set FP == Former/Original SP
            ; I moved the above to below params, maybe works?
            MOV R8, SP          ;save sp - check for stack overflow
            CMP R8, SL
            BLT R8, STACKOVERFLOW
            MOV R8, PC          ;save current PC (which points at next instruction when executing
            ADI R8, #36
            STR R8, FP
            JMP printFail_Functions

            MOV SP, FP          ;get rid of top (no longer needed) frame
            MOV R8, FP          ;SP <= FP
            ADI R8, #-4         ;get the PFP
            
            LDR R3, FP          ;get ret val to put in frame
            LDR R14, FP      ;and one for oher uses just in case
        
            LDR FP, R8          ;FP = PFP
            MOV R15, SP          ;check for stackunderflow
            CMP R15, SB
            BGT R15, STACKUNDERFLOW
IF19end MOV R0, R0
TRP #0
STACKOVERFLOW TRP #99
TRP #0
STACKUNDERFLOW TRP #99
TRP #0
