bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit, printf, scanf, fprintf, fscanf, fopen, fclose               ; tell nasm that exit exists even if we won't be defining it
import exit msvcrt.dll    ; exit is a function that ends the calling process. It is defined in msvcrt.dll
                          ; msvcrt.dll contains exit, printf and all the other important C-runtime specific functions
import printf msvcrt.dll     ; indicating to the assembler that the printf fct can be found in the msvcrt.dll library
import scanf msvcrt.dll      ; similar for scanf
import fprintf msvcrt.dll
import fscanf msvcrt.dll
import fopen msvcrt.dll
import fclose msvcrt.dll                        

; our data is declared here (the variables needed by our program)
segment data use32 class=data
    ;set 1
    ;3.
    ;inputMessage db "Enter a and b: ", 0
    ;inputFormat db "%d %d", 0
    ;outputFormat db "%d + %d = %d", 10, 0
    
    ;a dd 0
    ;b dd 0
    ;result dd 0
    
    ;18.
    ;inputMessage db "Enter a and b: ", 0
    ;inputFormat db "%d %x", 0  ; Change the format specifier for the second number to hexadecimal
    ;outputFormat db "Number of set bits in the sum: %d", 10, 0
    
    ;a dd 0
    ;b dd 0
    ;result dd 0
    
    ;set 2
    ;3.
    ;file_name       db "your_text_file.txt", 0
    ;file_access_mode db "r", 0
    ;file_descriptor resd 1
    
    ;text resd 1  
    ;number_of_words   resd 1
    ;input_format    db "%c", 0
    ;output_format   db "Number of words: %d", 10, 0
    
    ;18.
    file_name db "your_text_file.txt", 0
    file_access_mode db "r", 0
    file_descriptor resd 1
    
    digit resd 1
    even_digit_count resd 1
    input_format db "%c", 0
    output_format db "Number of even digits: %d", 10, 0
    
; our code starts here
segment code use32 class=code
    start:
        ;set 1
        ;3.
        ; print the prompt message
        ;push inputMessage
        ;call [printf]
        ;add esp, 4 * 1
        
        ; read a and b
        ;push dword b
        ;push dword a
        ;push inputFormat
        ;call [scanf]
        ;add esp, 4 * 3
        
        ; compute the result
        ;mov eax, dword [a]
        ;mov ebx, dword [b]
        ;add eax, ebx
        ;mov [result], eax
        
        ; print the result
        ;push dword [result]
        ;push dword [b]
        ;push dword [a]
        ;push outputFormat
        ;call [printf]
        ;add esp, 4 * 4
        
        
        ;18.
        ; print input message
        ;push inputMessage
        ;call [printf]
        ;add esp, 4  ; adjust the stack pointer after printf

        ; read input values
        ;push dword b
        ;push dword a
        ;push inputFormat
        ;call [scanf]
        ;add esp, 4 * 3  ; adjust the stack pointer after scanf

        ; calculate sum
        ;mov eax, [a]
        ;add eax, [b]
        ;mov [result], eax

        ; count set bits in the sum
        ;mov ecx, 0  ; initialize the counter
        ;mov ebx, [result]  ; load the sum into ebx

        ;count_bits_loop:
        ;    shr ebx, 1  ; shift right, removing the least significant bit
            ;adc ecx, 0  ; add the carry flag to the counter
            ;cmp ebx, 0  ; compare ebx with 0
            ;jnz count_bits_loop  ; jump if not zero -> continue until ebx becomes zero

            ; print the result
            ;push ecx
            ;push outputFormat
            ;call [printf]
            ;add esp, 4 * 2  ; adjust the stack pointer after printf


        ;set 2
        ;3.
        ; Open the file
        ;push dword file_access_mode
        ;push dword file_name
        ;call [fopen]
        ;add ESP, 4 * 2

        ;mov [file_descriptor], EAX
        ;cmp EAX, 0
        ;je end_program

        ; Initialize number_of_words to 0
        ;mov dword [number_of_words], 0

        ; Read characters from the file
        ;process_characters:
        ;    push dword text
        ;    push dword input_format
        ;    push dword [file_descriptor]
        ;    call [fscanf]
        ;    add ESP, 4 * 3

            ; Check if fscanf successful
        ;    cmp eax, 1
        ;    jl  end_program
            
            ; Check if the character is a letter
        ;    cmp dword [text], 'a'
        ;    jl  is_not_word
        ;    cmp dword [text], 'z'
        ;    jg  is_not_word
            
        ;    cmp dword [text], 'A'
        ;    jb  is_not_word
        ;    cmp dword [text], 'Z'
        ;    ja  is_not_word
            
        ;    cmp dword [text + 1], ' '
        ;    jne is_not_word

        ;    cmp dword [text + 1], '.'
        ;    jne is_not_word
            
        ;    inc dword [number_of_words]

        ;is_not_word:
        ;    jmp process_characters

        ;end_program:
            ; Close the file
        ;    push dword [file_descriptor]
        ;    call [fclose]
        ;    add ESP, 4 * 1

            ; Display the result on the screen
        ;    push dword [number_of_words]
        ;    push dword output_format
        ;    call [printf]
        ;    add ESP, 4 * 2
        
        
        
        ;18.
        ; Open the file
        push dword file_access_mode
        push dword file_name
        call [fopen]
        add ESP, 4 * 2
        
        mov [file_descriptor], EAX
        cmp EAX, 0
        je exit_program
       
        ; Initialize even_digit_count to 0
        mov dword [even_digit_count], 0

        ; Read characters from the file
        read_characters:
            push dword digit
            push dword input_format
            push dword [file_descriptor]
            call [fscanf]
            add ESP, 4 * 3
            
            ; Check if fscanf successful
            cmp eax, 1
            jl exit_program
            
            ; Check if the read character is a digit
            cmp dword [digit], '0'
            jl  not_digit
            cmp dword [digit], '9'
            jg  not_digit
            
            ; Convert the character to integer
            sub dword [digit], '0'
            
            ; Check if the digit is even
            test dword [digit], 1
            jz  even_digit
            
        not_digit:
            jmp  read_characters
        
        even_digit:
            ; Increment the even_digit_count
            inc dword [even_digit_count]
            jmp  read_characters

        exit_program:
            ; Close the file
            push dword [file_descriptor]
            call [fclose]
            add ESP, 4 * 1
            
            ; Display the result
            push dword [even_digit_count]
            push dword output_format
            call [printf]
            add ESP, 4 * 2
        
    
        ;exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
