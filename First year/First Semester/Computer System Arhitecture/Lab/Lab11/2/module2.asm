bits 32


global get_numbers

extern strlen
import strlen msvcrt.dll


segment data use32 class=data
    digit_string resb 100

segment code use32 class=code
    get_numbers:
        push ebp
        mov ebp, esp
            
            mov esi, dword [ebp + 8] ; parameter: string address
            
            ; determine lenght of string
            
            push esi
            call [strlen]
            add esp, 4 * 1
            mov ecx, eax  ; move returned value into ecx
            
            ; determine lenght of string
            
            jecxz .end
			mov edi, digit_string
			.loop:			
				cmp byte [esi], '1'  ; not 0 to make it save 01 as 1 instead of 01
				jb .not_digit
				cmp byte [esi], '9'
				ja .not_digit
                
                cmp byte [esi - 1], '-'  ; add - if necessary
                jne .not_minus
                mov al, '-'
                stosb
                .not_minus:
				
                .inner_loop:  ; put digits that are next to each other into the same number
                    mov al, [esi]
                    stosb
                    inc esi
                    
                    cmp byte [esi], '0'  ; not a digit
                    jb .break_inner_loop
                    cmp byte [esi], '9'
                    ja .break_inner_loop  ; not a digit
                    
                jmp .inner_loop
                .break_inner_loop:
                
                mov al, ' ' ; add whitespace between numbers
                stosb
                
                jmp .end_loop
                
                .not_digit:
                inc esi
                
                .end_loop:
                
			loop .loop
            
			.end:
		
        mov eax, digit_string  ; returned value = the string with only numbers
        
        mov esp, ebp
        pop ebp
        ret