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
    ;S1 db 1, 2, 3, 4          ; Byte string S1
    ;S1_len equ $ - S1         ; Length of S1
    ;S2 db 5, 6, 7             ; Byte string S2
    ;S2_len equ $ - S2         ; Length of S2
    ;D times (S1_len+S2_len) db 0      ; String D
    
    ;18.
    A db 2, 1, 3, -3
    B db  4, 5, -5, 7
	l1 equ $-A ; length of string A
    l2 equ $-B ; length of string B
	R times (l1+l2) db 0 ; reserve bytes for the destination string and initialize it

; our code starts here
segment code use32 class=code
    start:
        ; Copy S1 to D
        ;mov esi, 0             ; Source index for S1
        ;mov ecx, S1_len         ; Counter for the loop

        ;copy_s1_loop:
        ;    mov al, [S1 + esi]
        ;    mov [D + esi], al
        ;    inc esi
        ;loop copy_s1_loop       ; Loop until ECX becomes zero

        ; Copy S2 to D in reverse order
        ;mov esi, S2_len - 1         ; Source index for S2 (starting from the end)
        ;mov ecx, S2_len         ; Counter for the loop
        ;mov edi, 0

        ;copy_s2_reverse_loop:
        ;    mov al, [S2 + esi]
        ;    mov [D + S1_len + edi], al
        ;    dec esi  
        ;    inc edi
        ;loop copy_s2_reverse_loop ; Loop until ECX becomes zero
        
        
        ;18.
        
        mov ecx, l1         ; set the loop counter for A
        mov esi, 0          ; initialize the source index for A
        mov edi, 0          ; initialize the destination index for R
        
        Check_A_Loop:
            mov al, [A + esi]   ; load the byte from A into AL
            cmp al, 0           ; check if the byte is zero (end of string)
            je  Check_string_B        ; if yes, jump to processing B

            test al, 10000000b         ; test if the byte is positive
            js NextElementA           ; if positive, skip to the next element in A (JS check the Sign flag)

            ; If we reach here, the element is positive
            test al, 1b ; check if odd
            jz NextElementA ; if is not odd jump to the next element
            
            mov [R + edi], al   ; copy the element to R
            inc edi             ; move to the next destination index in R

        NextElementA:
            inc esi             ; move to the next source index in A
        loop Check_A_Loop       ; repeat the loop for A

        Check_string_B:
            mov ecx, l2        ; set the loop counter for B
            mov esi, 0          ; initialize the source index for B

        Check_B_Loop:
            mov al, [B + esi]   ; load the byte from B into AL
            cmp al, 0           ; check if the byte is zero (end of string)
            je  End_label           ; if yes, end the program

            test al, 10000000b        ; test if the byte is positive
            js NextElementB    ; if positive, skip to the next element in B


            ; If we reach here, the element is positive
            test al, 1b ; check if odd
            jz NextElementB ; if is not odd jump to the next element
            
            mov [R + edi], al   ; copy the element to R
            inc edi             ; move to the next destination index in R

        NextElementB:
            inc esi             ; move to the next source index in B
        loop Check_B_Loop   ; repeat the loop for B

        
        End_label:
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
