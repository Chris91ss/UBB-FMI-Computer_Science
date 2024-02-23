bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit               ; tell nasm that exit exists even if we won't be defining it
import exit msvcrt.dll    ; exit is a function that ends the calling process. It is defined in msvcrt.dll
                          ; msvcrt.dll contains exit, printf and all the other important C-runtime specific functions

; our data is declared here (the variables needed by our program)
segment data use32 class=data
        ;First set
        ;a db 1
        ;b dw 2
        ;c dd 3
        ;d dq 4
        
        
        ;Second set
        a dw 1
        b db 2
        c db 3
        d db 4
        e dd 5
        x dq 6
        var db 100
    
; our code starts here
segment code use32 class=code
    start:
        ;First set - Unsigned
        ;3. (c+d)-(a+d)+b
        ;xor eax, eax
        ;mov eax, [c]
        ;add eax, [d]
        ;sub eax, [a]
        ;sub eax, [d]
        ;add eax, [b]
        
        
        ;18. (d+d)-a-b-c
        ;xor eax, eax
        ;mov eax, [d]
        ;add eax, [d]
        ;sub eax, [a]
        ;sub eax, [b]
        ;sub eax, [c]
        
        
        ;Signed
        ;3.(b+b+d)-(c+a)
        ;xor eax, eax
        ;mov eax, [b]
        ;add eax, [b]
        ;add eax, [d]
        ;sub eax, [c]
        ;sub eax, [a]
        
        
        ;18.(d-b)-a-(b-c)
        ;xor eax, eax
        ;mov eax, [d]
        ;sub eax, [b]
        ;sub eax, [a]
        ;sub eax, [b]
        ;add eax, [c]
        
        ;Second set
        ;Unsigned
        ;3. (8-a*b*100+c)/d+x
        ;xor eax, eax
        ;mov bl, 8
        ;mov al, [a]
        ;mul word [b] 
        ;mov ah, 0
        ;mul byte [var] 
        ;add ax, [c] ; ax = a*b*100+c
        ;mov cx, ax ; cx = a*b*100+c
        ;mov ax, 0
        ;mov al, bl ; al = 8
        ;mov ah, 0
        ;sub ax, cx ; ax = 8-a*b*100+c
        ;mov bx, [d]
        ;add bx, [x]; bx = d+x
        ;div bx ; al = (8-a*b*100+c)/d+x
        
        ;18.(a+b*c+2/c)/(2+a)+e+x
        ;xor eax, eax
        ;mov al, [b]
        ;mul word [c] ; ax = b*c
        ;mov bx, ax ; bx = b*c
        ;xor eax, eax
        ;mov ax, 2
        ;div word [c] ; al = 2/c
        ;mov ah, 0 ; ax = 2/c
        ;xor ecx, ecx
        ;mov cl, 2
        ;add cl, [a] ; cl = 2+a
        ;add ax, bx
        ;add ax, [a] ; ax = (a+b*c+2/c)
        ;mov ah, 0 ; convert to make sure it's a word
        ;xor edx, edx
        ;div cl ; ax = (a+b*c+2/c)/(2+a)
        ;add ax, [e]
        ;add ax, [x] ; ax = (a+b*c+2/c)/(2+a)+e+x
        
        
        ;Signed
        ;3. (8-a*b*100+c)/d+x
        ;xor eax, eax
        ;mov bl, 8
        ;mov al, [a]
        ;imul word [b] 
        ;cbw
        ;imul byte [var] 
        ;add ax, [c] ; ax = a*b*100+c
        ;mov cx, ax ; cx = a*b*100+c
        ;xor eax, eax
        ;mov al, bl ; al = 8
        ;cbw
        ;sub ax, cx ; ax = 8-a*b*100+c
        ;mov bx, [d]
        ;add bx, [x]; bx = d+x
        ;idiv bx ; al = (8-a*b*100+c)/d+x
        
        
        ;18.(a+b*c+2/c)/(2+a)+e+x
        xor eax, eax
        mov al, [b]
        cbw ; ax = b
        imul word [c] ; ax = b*c
        mov bx, ax ; bx = b*c
        xor eax, eax
        mov al, 2
        cbw ; ax = 2
        idiv word [c] ; al = 2/c
        cbw ; ax = 2/c
        add ax, bx ; ax = b*c+2/c
        add ax, [a] ; ax = (a+b*c+2/c)
        mov bx, ax ; bx = (a+b*c+2/c)
        xor ecx, ecx
        mov cl, 2
        add cl, [a] ; cl = 2+a
        mov al, cl ; al = 2+a
        cbw ; ax = 2+a
        mov cx, ax ; cx = 2+a
        mov ax, bx
        idiv cx ; al = (a+b*c+2/c)/(2+a)
        cbw
        cwd
        cdq ; edx:eax = (a+b*c+2/c)/(2+a)
        add eax, [e]
        adc edx, 0
        add eax, [x] ; ax = (a+b*c+2/c)/(2+a)+e+x
        adc edx, 0
        
        
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
