bits 32


global _read_input

extern _gets


segment data use32 class=data


segment code use32 class=code
; read a sentence from the keyboard that contains letters and numbers, display the numbers from within the sentece separated by a space
    _read_input:
        push ebp
        mov ebp, esp
            
            push dword [ebp + 8] ; read_input receives as a parameter a string
            call _gets
            add esp, 4 * 1
        
        mov esp, ebp
        pop ebp
        ret