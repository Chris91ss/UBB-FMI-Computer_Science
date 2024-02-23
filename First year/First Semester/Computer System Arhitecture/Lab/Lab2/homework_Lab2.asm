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
    ;x db -1
    ;var db 2
    ;var2 db 3
    
    ;5th set
    a db 1
    b db 2
    c db 3
    d db 4
    e dw 5
    f dw 6
    g dw 7
    h dw 8
    var db 3
    result dw 0
    
; our code starts here
segment code use32 class=code
    start:
        
        ;First set:
        ;4. 5-6
        ;mov eax, 5
        ;sub eax, 6
        
        ;19. 12/4
        ;mov eax, 12
        ;mov ebx, 4
        ;xor edx, edx ; empty edx
        ;div ebx
    
        ;Second set
        ;4. (a-b)+(c-b-d)+d
        ;xor al, al
        ;add al, [a]
        ;sub al, [b]
        ;add al, [c]
        ;sub al, [b]
        ;sub al, [d]
        ;add al, [d]
        
        ;19. d-(a+b)-c
        ;xor al, al
        ;add al, [d]
        ;sub al, [a]
        ;sub al, [b]
        ;sub al, [c]
        
        ;Third set
        ;4. (b+b)-c-(a+d)
        ;xor ax, ax
        ;add ax, [b]
        ;add ax, [b]
        ;sub ax, [c]
        ;sub ax, [a]
        ;sub ax, [d]
        
        ;19. b+a-(4-d+2)+c+(a-b)
        ;xor ax, ax
        ;add ax, [b]
        ;add ax, [a]
        ;sub ax, 4
        ;add ax, [d]
        ;sub ax, 2
        ;add ax, [c]
        ;add ax, [a]
        ;sub ax, [b]
        
        ;4th set
        ;4. –a*a + 2*(b-1) – d
        ;xor eax, eax
        ;mov al, [a]
        ;mul byte [x] ; ax = -a
        ;mul byte [a] ; ax = -a * a
        ;mov bx, ax
        ;mov ax, [b]
        ;sub ax, 1
        ;mul byte [var]
        ;add bx, ax ; bx = -a * a + 2(b-1)
        ;mov ax, bx ; ax = -a * a + 2(b-1)
        ;mov ah, 0
        ;sub ax, [d]
        
        ;19. [(a-b)*3+c*2]-d
        ;xor eax, eax
        ;mov al, [a]
        ;sub al, [b]
        ;mul byte [var2]
        ;add ax, [c]
        ;mul byte [var]
        ;sub ax, [d]
        
        ;5th set
        ;4. –a*a + 2*(b-1) – d
        ;xor eax, eax
        ;mov al, [a]
        ;sub al, [c]
        ;mul byte [var]
        ;mov bx, ax
        ;mov al, [b]
        ;mul byte [b]
        ;add ax, bx
        
        ;19. (e + g) * 2 / (a * c) + (h – f) + b * 3
        mov ax, [e]
        add ax, [g] ; AX = e + g
        add ax, ax ; AX = 2 * (e + g)
        mov bx, ax
        mov al, [a]
        mov cl, [c] ; BL = c
        mul cl ; AL = a * c
        mov cl, al ; CL = a * c
        mov ax, bx
        div cl ; AX = 2 * (e + g) / (a * c)
        mov [result], ax ; result = 2 * (e + g) / (a * c)
        mov dx, [h]
        sub dx, [f] ; DX = h - f 
        add [result], dx ; result = 2 * (e + g) / (a * c) + h - f
        mov al, [b]
        mov bl, 3
        mul bl ; Ax = b * 3
        add [result], ax ; result = 2 * (e + g) / (a * c) + h - f + b * 3
        
        
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
