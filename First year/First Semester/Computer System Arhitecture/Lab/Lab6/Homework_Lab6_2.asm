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
    ;s db -22, 145, -48, 127
    ;len equ $ - s
    ;d times len db 0
    
    ;18.
    sir dw 12345, 20778, 4596 
    len equ ($-sir)/2
    rez times len*5 db 0

; our code starts here
segment code use32 class=code
    start:
        ; Initialize index
        ;mov esi, 0

        ;calculate_counts:
            ; Check if we reached the end of the string
        ;    cmp esi, len
        ;    je  done

            ; Load the current element from s
        ;    mov al, [s + esi]

            ; Count the number of ones or zeros in the binary representation
        ;    mov ecx, 8
        ;    xor ebx, ebx  ; Clear the count
        ;count_bits_loop:
        ;    shl al, 1
        ;    adc ebx, 0
        ;    loop count_bits_loop

            ; Store the count in d
        ;    mov [d + esi], ebx

            ; Move to the next element
        ;    inc esi
        ;    jmp calculate_counts

        ;done:
        
        
        ;18. Being given a string of words, obtain the string (of bytes) of the digits in base 10 of each word from this string
        mov ecx, len
        mov esi, sir
        mov edi, rez
 
        repeta:
            cld
            push ecx
            lodsw 
     
            push esi
            push edi 
     
            cmp ax, 10000
            jb _4cifre
     
            mov ecx, 5
            jmp bag_ecx
     
            _4cifre:
            cmp ax, 1000
            jb _3cifre
     
            mov ecx, 4
            jmp bag_ecx
     
            _3cifre:
            cmp ax, 100
            jb _2cifre
     
            mov ecx, 3
            jmp bag_ecx
     
            _2cifre:
            cmp ax, 10
            jb _1cifra
     
            mov ecx, 2
            jmp bag_ecx
     
            _1cifra:
            mov ecx, 1
     
            bag_ecx:
            push ecx
     
            dec ecx
            add edi, ecx
            inc ecx
     
            std    
     
            divide:            
                mov dx, 0
     
                mov bh, 0
                mov bl, 10
                div bx 
     
     
                xchg ax, dx
                stosb 
                xchg ax, dx
     
                loop divide
     
            pop ecx
     
            pop edi
            pop esi 
     
            add edi, ecx 
     
            pop ecx
            loop repeta
     
     
        final:

        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
