bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit               ; tell nasm that exit exists even if we won't be defining it
import exit msvcrt.dll    ; exit is a function that ends the calling process. It is defined in msvcrt.dll
                          ; msvcrt.dll contains exit, printf and all the other important C-runtime specific functions

; our data is declared here (the variables needed by our program)
segment data use32 class=data
        ;4.
        ;A db 11011000b
        ;B db 0
        ;C dd 00000000000000000000000000000000b
        
        
        ;19.
        A dw 1101100011011000b
        B dd 00000000000000000000000000000000b
; our code starts here
segment code use32 class=code
    start:
        ;4.
        ;mov al, [A]
        ;mov bl, 0
        ;and al, 00011100b
        ;or bl, al ; bl = n = the number represented on bits 2-4
        ;mov al, [A]
        ;mov cl, bl
        ;ror al, cl
        ;mov [B], al ; B = the number by rotating A n positions to the right.
        
        ;Compute the doubleword C
        
        ;xor eax, eax
        ;mov al, [B]
        ;mov ah, 0
        ;mov dx, 0 ; dx:ax = [B]
        ;mov cl, 8
        ;shl al, 8
        ;or [C], dx ; bits 16-23 from C are the same bits as B
        
        ;xor eax, eax
        ;mov al, [A]
        ;mov ah, 0
        ;mov dx, 0; dx:ax = [A]
        ;mov cl, 16
        ;shl al, cl
        ;or [C], dx ; bits 24-31 from C are the same bits as A
        
        ;or dword [C], 00000000000000000000000011111111b
        
        
        ;19.
        xor eax, eax
        xor edx, edx
        or dx, 1111000000000000b ; we form B in dx:ax, the bits 28-31 are set to 1
        
        mov bx, [A]
        and bx, 0000001100000000b ; isolate bits 8-9 from A
        or dx, bx ; the bits 24-25 are the same as the bits 8-9 from A
        mov cl, 2
        shl bx, cl 
        or dx, bx ; ; the bits 26-27 are the same as the bits 8-9 from A
        
        mov bx, [A]
        and bx, 0000000000001111b
        not bx 
        mov cl, 1
        shl bx, cl
        or dx, bx ; the bits 20-23 are the same as the inverted 0-3 bits from A
        mov ax, dx ; the bits 0-15 of B are the same as the bits 16-31 of B.
                  ; we have the result in dx:ax
                  
        
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
