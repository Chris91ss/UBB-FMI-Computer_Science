bits 32

global _convert

segment code:
_convert:
    ; read an integer in base 2 and convert it to a base 10 integer 
    push ebp
    mov ebp, esp
    mov eax, [ebp + 8]
    mov ebx, 0
    mov ecx, 1
    get_digit:
        mov edx, 0
        mov esi, 10
        div esi
        cmp edx, 0
        je no_add
        add ebx, ecx
        no_add:
            shl ecx, 1
            cmp eax, 0
            jne get_digit
    pop ebp
    mov eax, ebx
    ret
        