@R1
D=A
@R2
M=D

(LOOP_POT)
    @R2
    D=M
    @a
    M=D
    @R0
    D=M
    @b
    M=D
    @0
    D=A
    @c
    M=D

    (LOOP) 
    @a
    D=M
    @c
    M=M+D
    @b
    D=M
    D=D - 1
    M=D
    @LOOP
    D;JGT

    @c
    D=M
    @R2
    M=D

    @1
    D=A
    @R1
    M=M - D
    D=M

    @LOOP_POT
    D;JGT


(END)
@END
0;JMP