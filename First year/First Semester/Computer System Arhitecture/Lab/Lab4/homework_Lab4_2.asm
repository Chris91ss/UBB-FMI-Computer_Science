bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit               ; tell nasm that exit exists even if we won't be defining it
import exit msvcrt.dll    ; exit is a function that ends the calling process. It is defined in msvcrt.dll
                          ; msvcrt.dll contains exit, printf and all the other important C-runtime specific functions

; our data is declared here (the variables needed by our program)
segment data use32 class=data
        ;3.
        ;A dw 1101100011011000b
        ;B dw 1001101010010011b
        ;C dd 00000000000000000000000000000000b

        
        ;18.
        A dw 1101100011011000b 
        B dd 00000000000000000000000000000000b
; our code starts here
segment code use32 class=code
    start:
    
        ;3.
        ;xor eax, eax
        ;xor edx, edx
        ;mov bx, [A]
        ;and bx, 00000111000000000000b ; isolate bits 12-14 from A
        ;form the result in dx:ax because it's a double word
        ;mov cl, 12
        ;shr bx, cl ; shift right bx with 10 positions, so the bits 12-14 are on position 0-2
        ;or ax, bx ; set the bits 0-2 the same as the 12-14 bits
        
        ;mov bx, [B]
        ;and bx, 00000000000000111111b ; isolate bits 0-5 of B
        ;mov cl, 3
        ;shl bx, cl ; shift left bx with 3 positions, so the bits 0-5 are on position 3-8
        ;or ax, bx ; set the bits 3-8 of C as the bits 0-5 of B
        
        ;mov bx, [A]
        ;and bx, 00000000001111111000b ; isolate bits 3-9 of A
        ;mov cl, 6
        ;shl bx, cl  ; shift left with 6 positions, so the bits 3-9 are on position 9-15
        ;or ax, bx ; set the bits 9-15 of C the same as the bits 3-9 of A
        
        ;mov bx, [A]
        ;or dx, bx ; the bits 16-31 of C are the same as the bits of A
                   ; we have the result in dx:ax
        
        
        ;18.
        xor eax, eax
        xor edx, edx
        mov bx, [A]
        and bx, 0000111100000000b ; isolate the bits 8-11 of A
        mov cl, 4
        shr bx, cl ; shift right with 4 positions, so the bits 8-11 are on position 4-7
        or ax, bx ; the bits 4-7 of B are the same as the bits 8-11 of A
        
        mov bx, [A]
        and bx, 0000000000000011b ; isolate the bits 0-1 of A
        neg bx ; inverse the bits
        mov cl, 8
        shl bx, cl ; shift left with 8 positions, so the bits 0-1 are on position 8-9
        or ax, bx ; the bits 8-9 of B are the invert of the bits 0-1 of A 
        mov cl, 2
        shl bx, cl ; shift left with 2 positions, so the bits 8-9 are on position 10-11
        mov ax, bx ; the bits 10-11 of B are the invert of the bits 0-1 of A 
        
        or ax, 1111000000000000 ; the bits 12-15 of B have the value 1
        
        or dx, ax ; the bits 16-31 of B are the same as the bits 0-15 of B.
                  ; we have the final result in dx:ax
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
