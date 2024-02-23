bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit               ; tell nasm that exit exists even if we won't be defining it
extern printf             ; printf is used for displaying formatted output
extern fopen              ; fopen is used to open a file
extern fscanf             ; fscanf is used to read from a file
extern fclose             ; fclose is used to close a file

import exit msvcrt.dll
import printf msvcrt.dll
import fopen msvcrt.dll
import fscanf msvcrt.dll
import fclose msvcrt.dll

; our data is declared here (the variables needed by our program)
section data use32 class=data
    file_name       db "numbers.txt", 0
    file_access_mode db "r", 0
    file_descriptor resd 1
    
    text resd 10  
    reversed_doubled_text   resd 10
    input_format    db "%d", 0
    output_format   db "Reversed double numbers are: ", 10, 0
    output_format_with_comma db "%d ", 10, 0
    number_of_elements db 0
    copy_of_number_of_elements db 0
    

; our code starts here
section code use32 class=code
    start:
        ; Open the file
        push dword file_access_mode
        push dword file_name
        call [fopen]
        add ESP, 4 * 2

        mov [file_descriptor], EAX
        cmp EAX, 0
        je done_processing

        ; Initialize reversed_doubled_text to 0
        mov dword [reversed_doubled_text], 0
        mov esi, 0

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

            mov eax, [text]
            add eax, eax      ; double the number
            mov [reversed_doubled_text + esi], eax        ; add the number to the result string
            inc byte [number_of_elements]
            add esi, 4
            
            jmp process_characters


        done_processing:
            ; Close the file
            push dword [file_descriptor]
            call [fclose]
            add ESP, 4 * 1
            
            mov esi, 0
            mov eax, [number_of_elements]
            add [copy_of_number_of_elements], eax
            
            ; Display the result on the screen
            push dword output_format
            call [printf]
            add ESP, 4 * 1
            
            get_to_end_of_string:
                cmp byte [copy_of_number_of_elements], 0
                je dec_once
                dec byte [copy_of_number_of_elements]
                
                add esi, 4
                jmp get_to_end_of_string
            
            dec_once:
            sub esi, 4
            
            print_loop:
                cmp byte [number_of_elements], 0
                je end_of_string
                dec byte [number_of_elements]
            
                push dword [reversed_doubled_text + esi]
                push dword output_format_with_comma
                call [printf]
                add ESP, 4 * 2
                sub esi, 4
                jmp print_loop
            
        end_of_string:
        ; Exit the program
        push dword 0
        call [exit]



