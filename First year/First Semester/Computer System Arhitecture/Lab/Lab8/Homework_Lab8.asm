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
    ;4.
    ;set 1
    ;inputMessage db "Enter a and b: ", 0
    ;inputFormat db "%d %d", 0
    ;outputFormat db "%d * %d = %d", 10, 0
    
    ;a dd 0
    ;b dd 0
    ;product dd 0
    
    ;19
    ;inputMessage db "Enter a decimal number: ", 0
    ;inputFormat db "%d", 0
    ;outputFormat db "Value in hexadecimal: %X", 10, 0
    ;inputValue dd 0
    
    ;set 2
    ;4.
    ;file_name db "your_text_file.txt", 0
    ;file_access_mode db "r", 0
    ;file_descriptor resd 1
    
    ;digit resd 1
    ;odd_digit_count resd 1
    ;input_format db "%c", 0
    ;output_format db "Number of odd digits: %d", 10, 0
    
    ;19.
    file_name       db "your_text_file.txt", 0
    file_access_mode db "r", 0
    file_descriptor resd 1
    
    text resd 1  
    sum_of_digits   resd 1
    input_format    db "%c", 0
    output_format   db "Sum of digits: %d", 10, 0

; our code starts here
segment code use32 class=code
    start:
        ;set 1
        ;4.
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
        
        ; compute the product
        ;mov eax, dword [a]
        ;mov ebx, dword [b]
        ;imul eax, ebx
        ;mov [product], eax
        
        ; print the product
        ;push dword [product]
        ;push dword [b]
        ;push dword [a]
        ;push outputFormat
        ;call [printf]
        ;add esp, 4 * 4

        
        ;19
        ; print the prompt message
        ;push inputMessage
        ;call [printf]
        ;add esp, 4 * 1
        
        ; read the decimal number
        ;push dword inputValue
        ;push inputFormat
        ;call [scanf]
        ;add esp, 4 * 2  ; adjust the stack pointer after scanf

        ; display the value in hexadecimal
        ;push dword [inputValue]
        ;push outputFormat
        ;call [printf]
        ;add esp, 4 * 2  ; adjust the stack pointer after printf
        
        
        ;set 2
        ;4.
        ; Open the file
        ;push dword file_access_mode
        ;push dword file_name
        ;call [fopen]
        ;add ESP, 4 * 2
        
        ;mov [file_descriptor], EAX
        ;cmp EAX, 0
        ;je exit_program
       
        ; Initialize odd_digit_count to 0
        ;mov dword [odd_digit_count], 0

        ; Read characters from the file
        ;read_characters:
        ;    push dword digit
        ;    push dword input_format
        ;    push dword [file_descriptor]
        ;    call [fscanf]
        ;    add ESP, 4 * 3
            
            ; Check if fscanf successful
        ;    cmp eax, 1
        ;    jl exit_program
            
            ; Check if the read character is a digit
        ;    cmp dword [digit], '0'
        ;    jl  not_digit
        ;    cmp dword [digit], '9'
        ;    jg  not_digit
            
            ; Convert the character to integer
        ;    sub dword [digit], '0'
            
            ; Check if the digit is odd
        ;    test dword [digit], 1
        ;    jnz  odd_digit
            
        ;not_digit:
        ;    jmp  read_characters
        
        ;odd_digit:
            ; Increment the odd_digit_count
        ;    inc dword [odd_digit_count]
        ;    jmp  read_characters

        ;exit_program:
            ; Close the file
        ;    push dword [file_descriptor]
        ;    call [fclose]
        ;    add ESP, 4 * 1
            
            ; Display the result
        ;    push dword [odd_digit_count]
        ;    push dword output_format
        ;    call [printf]
        ;    add ESP, 4 * 2
        
        
        ;19.
        ; Open the file
        push dword file_access_mode
        push dword file_name
        call [fopen]
        add ESP, 4 * 2

        mov [file_descriptor], EAX
        cmp EAX, 0
        je done_processing

        ; Initialize sum_of_digits to 0
        mov dword [sum_of_digits], 0

        ; Read characters from the file
        process_characters:
            push dword text
            push dword input_format
            push dword [file_descriptor]
            call [fscanf]
            add ESP, 4 * 3

            ; Check if fscanf successful
            cmp eax, 1
            jl  done_processing
            
            ;Check if the character is "."
            cmp dword [text], '.'
            je not_digit

            ; Check if the character is a digit
            cmp dword [text], '0'
            jl  not_digit
            cmp dword [text], '9'
            jg  not_digit

            sub dword [text], '0'                    ; Convert ASCII character to integer
            mov eax, [text]
            add [sum_of_digits], eax        ; Add the digit to sum_of_digits

        not_digit:
            jmp process_characters

        done_processing:
            ; Close the file
            push dword [file_descriptor]
            call [fclose]
            add ESP, 4 * 1

            ; Display the result on the screen
            push dword [sum_of_digits]
            push dword output_format
            call [printf]
            add ESP, 4 * 2
        
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
