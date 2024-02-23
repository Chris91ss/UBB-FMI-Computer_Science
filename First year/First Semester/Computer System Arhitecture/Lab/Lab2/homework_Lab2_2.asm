bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit               ; tell nasm that exit exists even if we won't be defining it
import exit msvcrt.dll    ; exit is a function that ends the calling process. It is defined in msvcrt.dll
                          ; msvcrt.dll contains exit, printf and all the other important C-runtime specific functions

; our data is declared here (the variables needed by our program)
segment data use32 class=data

    ;Second set
    ;a db 1
    ;b db 2
    ;c db 3
    ;d db 4
    
    ;Third set
    ;a dw 1
    ;b dw 2
    ;c dw 3
    ;d dw 4
    
    ;4th set
    ;a db 1
    ;b db 2
    ;c db 3
    ;d dw 4
    
    ;5th set
    a db 5
    b db 2
    c db 7
    d db 8
    e dw 5
    f dw 20
    g dw 7
    h dw 8
    

; our code starts here
segment code use32 class=code
    start:
        ;First set:
        ;3. 128+128
        ;mov eax, 128
        ;add eax, 128
        
        ;18. 127+129
        ;mov eax, 127
        ;add eax, 129
        
        ;Second set
        ;3. (c+d)-(a+d)+b
        ;xor al, al
        ;add al, [c]
        ;add al, [d]
        ;sub al, [a]
        ;sub al, [d]
        ;add al, [b]
        
        ;18. d-(a+b)+c
        ;xor al, al
        ;add al, [d]
        ;sub al, [a]
        ;sub al, [b]
        ;add al, [c]
        
        ;Third set
        ;3.(b+b+d)-(c+a)
        ;xor ax, ax
        ;add ax, [b]
        ;add ax, [b]
        ;add ax, [d]
        ;sub ax, [c]
        ;sub ax, [a]
        
        ;18. (a-b-c)+(a-c-d-d)
        ;xor ax, ax
        ;add ax, [a]
        ;sub ax, [b]
        ;sub ax, [c]
        ;add ax, [a]
        ;sub ax, [c]
        ;sub ax, [d]
        ;sub ax, [d]
        
        ;4th set
        ;3. [-1+d-2*(b+1)]/a
        ;xor eax, eax
        ;add al, -1
        ;add al, [d]
        ;mov bx, ax
        ;mov al, 2
        ;mul byte [b]
        ;add al, 2
        ;add ax, bx
        ;div byte [a]
        
        ;18. 200-[3*(c+b-d/a)-300]
        ;xor eax, eax
        ;xor ebx, ebx
        ;add bl, 200
        ;add cl, [c]
        ;add cl, [b]
        ;add ax, [d]
        ;div byte [a]
        ;mov dl, ax
        ;mov ax, cl
        ;add ax, dl
        ;mul byte 3
        ;add ax, 300
        ;add ax, bl
        
        ;5th set
        ;3. (e+f)*g
        ;xor eax, eax
        ;mov ax, [e]
        ;add ax, [f]
        ;mul word [g]
        
        ;18. f+(c-2)*(3+a)/(d-4)
        mov al, [c] ; al = c
        sub al, 2 ; al = c - 2 = 7 - 2 = 5
        mov bl, 3 ; bl = 3
        add bl, [a]; bl = 3 + a = 3 + 5 = 8
        mul bl; ax = 40
        mov bl, [d] ; bl = 8
        sub bl, 4 ; bl = 8 - 4 = 4
        div bl ; al = 40 / 4 = 10
        mov ah, 0 ; ax = 10 we convert from byte to word
        mov bx, [f] ; bx = 20
        add bx, ax ; bx = 20 + 10 = 30
        
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
