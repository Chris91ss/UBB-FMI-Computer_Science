bits 32

global _minim

segment data public data use32

segment code public code use32

;Read a string of signed numbers in base 10 from keyboard. Determine the minimum value of the string and write it in the file min.txt (it will be created) in 16 base.

_minim:
    push ebp
    mov ebp, esp
    mov eax, [ebp + 8]       
    mov ebx, [ebp + 12]        
	cmp eax, ebx ; 
	jl final ; 
    mov eax, ebx            
	final:
    mov esp, ebp
    pop ebp
    ret
