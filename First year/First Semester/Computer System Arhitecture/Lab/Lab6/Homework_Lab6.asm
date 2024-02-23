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
    ;s db 5, 25, 55, 127
    ;len equ $ - s
    ;d times len db 0
    
    ;18.
    s dd  12345607h, 1A2B3C01h, 13A33412h
    l equ ($ - s) / 4
    multiple_of_7 db 7
    d times l db 0


; our code starts here
segment code use32 class=code
    start:
        ;3.
        ;mov esi, s       ; source index (input byte string)
        ;mov edi, d       ; destination index (output byte string)
        ;mov ecx, len     ; set the loop counter

        ;convert_loop:
        ;    lodsb            ; load the next byte from s into AL
        ;    popcnt eax, eax  ; count the number of set bits in AL
        ;    stosb            ; store the result in d
        ;loop convert_loop
        
        
        ;18. Given an array S of doublewords, build the array of bytes D formed from lower bytes of lower words, bytes multiple of 7
        mov esi, s
        mov edi, d
        mov ecx, l
        jecxz ending
        repeat:
            lodsd ; eax = [esi], esi += 4
            mov ebx, eax
            mov eax, 0
            mov al, bl
            div byte [multiple_of_7] ; ax / multiple_of_7 = al, rest = ah
            cmp ah, 0
            jne divisor ; if ah == 0
                mov al, bl
                stosb ; [edi] = al, edi += 1
            divisor:
        loop repeat
        ending:
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
