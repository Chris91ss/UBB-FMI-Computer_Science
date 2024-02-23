bits 32

global _base10

segment data public data use32
    
segment code public code use32

_base10:
    ; Multiple numbers in base 2 are read from the keyboard. Display these numbers in the base 16.
    push ebp
    mov ebp, esp
    mov esi, [ebp + 8]
	cld
	mov edx, 0
	mov eax, 0
	compute_nr:
		LODSB
		cmp al, 0
		jz final
		sub al, '0'
		shl edx, 1
		add edx, eax
		jmp compute_nr		
	final:
	mov eax, edx
	mov esp, ebp
    pop ebp
    ret
    