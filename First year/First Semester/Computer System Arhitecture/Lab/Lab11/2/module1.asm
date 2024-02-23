bits 32


global start

extern exit, gets, printf
import exit msvcrt.dll
import gets msvcrt.dll
import printf msvcrt.dll

extern get_numbers


segment data use32 class=data
    format db "%s", 0
    
    message_input db "Enter the string (mustn't be longer than 100 characters): ", 0
    message_output db "The digit string is: ", 0
    
    string resb 100
    digit_string_address dd 0

segment code use32 class=code
    start:
		
        ; print the input message
        push message_input
        push format
        call [printf]
        add esp, 4 * 2
        
        ; read the input string
		push string
		call [gets]
		add esp, 4 * 1
		
        ; get the digit string
		push string
		call get_numbers
		add esp, 4 * 1
        mov [digit_string_address], eax  ; move the returned string address into digit_string_address
        
        ; print the output message
        push message_output
        push format
        call [printf]
        add esp, 4 * 2
        
        ; print the digit string
        push dword [digit_string_address]
        push format
        call [printf]
        add esp, 4 * 2
        
        ; this is just so the program doesn't close immediately
        push string
		call [gets]
		add esp, 4 * 1
		
		push 0
		call [exit]