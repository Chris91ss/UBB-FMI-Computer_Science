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
    s1 db 1, -2, -3, 4 ; declare the string of bytes
    s2 db 5, 6, 7, 8
	l1 equ $-s1 ; compute the length of the s1 string in l1
	d times l1 db 0 ; reserve l bytes for the destination string and initialize it
    
    ;19.
    ;A db 2, 1, 3, -3, -4, 2, -6 ; declare the string of bytes
    ;B db  4, 5, -5, 7, -6, -2, 1
	;l1 equ $-A ; compute the length of the A string in l1
    ;l2 equ $-B ; compute the length of the B string in l2
	;R times (l1+l2) db 0 ; reserve l bytes for the destination string and initialize it

; our code starts here
segment code use32 class=code
    start:
        
        ;4.
        mov ecx, l1 ; we put the length l in ECX in order to make the loop
        mov esi, 0     
        jecxz END_P
        Repeat:
            ; Calculate even positions (sum)
            mov al, [s1 + esi]
            add al, [s2 + esi]
            mov [d + esi], al
            
            
            ; Calculate odd positions (difference)
            mov al, [s1 + esi + 1]
            sub al, [s2 + esi + 1]
            mov [d + esi + 1], al

            add esi, 1   ; Move to the next pair of elements
        loop Repeat 
        
        END_P: ; END of program
        
       
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
