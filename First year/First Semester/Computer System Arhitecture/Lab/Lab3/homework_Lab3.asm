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
        var db 2
        var2 db 100
        var3 db 10

; our code starts here
segment code use32 class=code
    start:
        
        ;First set
        ;4. Unsigned
        ;(a-b)+(c-b-d)+d
        ;xor eax, eax
        ;mov ax, [a]
        ;sub ax, [b]
        ;xor ebx, ebx
        ;mov bx, [c]
        ;sub bx, [b]
        ;sub bx, [d]
        ;add ax, bx
        ;add ax, [d]
        
        
        ;19.
        ;(d+d)-(a+a)-(b+b)-(c+c)
        ;xor eax, eax
        ;mov ax, [d]
        ;add ax, [d]
        ;xor ebx, ebx
        ;mov bx, [a]
        ;add bx, [a]
        ;sub ax, bx
        ;xor ebx, ebx
        ;mov bx, [b]
        ;add bx, [b]
        ;sub ax, bx
        ;xor ebx, ebx
        ;mov bx, [c]
        ;add bx, [c]
        ;sub ax, bx
        
        
        ;Signed
        ;4.
        ;(b+b)-c-(a+d)
        ;xor eax, eax;
        ;mov ax, [b]
        ;add ax, [b]
        ;sub ax, [c]
        ;sub ax, [a]
        ;subb ax, [d]
        
        
        ;19
        ;(d+a)-(c-b)-(b-a)+(c+d)
        ;xor eax, eax
        ;add eax, [d]
        ;add eax, [a]
        ;sub eax, [c]
        ;add eax, [b]
        ;sub eax, [b]
        ;add eax, [a]
        ;add eax, [c]
        ;add eax, [d]
        
        
        ;Second set
        ;4.
        ;(a*2+b/2+e)/(c-d)+x/a - unsigned 
        ;xor eax, eax
        ;mov al, [a]
        ;mul byte [var]
        ;mov bx, ax     ; bx = a * 2
        ;mov al, [b]
        ;div byte [var] ; ax = b / 2
        ;add ax, bx
        ;add ax, [e] ; ax = a*2+b/2+e
        ;xor ebx, ebx
        ;mov bl, [c]
        ;sub bl, [d] ; bl = (c-d)
        ;div bl ; al = a*2+b/2+e)/(c-d)
        ;mov ah, 0
        ;xor ebx, ebx
        ;mov bx, ax
        ;xor eax, eax
        ;mov eax, [x]
        ;div byte [a] ; x/a
        ;add ebx, eax  ; ebx = (a*2+b/2+e)/(c-d)+x/a
        
        
        ;19.
        ;(a+a+b*c*100+x)/(a+10)+e*a - unsigned
        ;xor eax, eax
        ;mov al, [b]
        ;imul byte [c]
        ;imul byte [var2] ; ax = b*c*100
        ;add ax, [a]
        ;add ax, [a]
        ;add ax, [x]  ; ax = a+a+b*c*100+x
        ;xor ebx, ebx
        ;mov ebx, eax ; bx = a+a+b*c*100+x
        ;xor eax, eax
        ;mov ax, [e]
        ;imul byte [a]
        ;xor ecx, ecx
        ;mov cx, ax ; cx = e*a
        ;xor eax, eax
        ;mov eax, ebx 
        ;xor ebx, ebx
        ;add bl, [a]
        ;add bl, [var3] ; bx = (a+10)
        ;idiv bl ; ax = (a+a+b*c*100+x)/(a+10)
        ;add al, cl ; al = (a+a+b*c*100+x)/(a+10)+e*a
        
        
        
        ;4.
        ;(a*2+b/2+e)/(c-d)+x/a - signed 
        ;xor eax, eax
        ;mov al, [a]
        ;imul byte [var]
        ;mov bx, ax     ; bx = a * 2
        ;mov al, [b]
        ;idiv byte [var] ; ax = b / 2
        ;add ax, bx
        ;add ax, [e] ; ax = a*2+b/2+e
        ;xor ebx, ebx
        ;mov bl, [c]
        ;sub bl, [d] ; bl = (c-d)
        ;idiv bl ; al = a*2+b/2+e)/(c-d)
        ;cbw
        ;xor ebx, ebx
        ;mov bx, ax
        ;xor eax, eax
        ;mov eax, [x]
        ;idiv byte [a] ; x/a
        ;add ebx, eax  ; ebx = (a*2+b/2+e)/(c-d)+x/a
        
        
        ;19.
        ;(a+a+b*c*100+x)/(a+10)+e*a - signed
        xor eax, eax
        mov al, [b]
        imul byte [c] 
        mov bx, ax
        mov al, [var2]
        cbw
        imul bx ; dx:ax = b*c*100
        add ax, [a]
        adc dx, 0
        add ax, [a]
        adc dx, 0
        cdq
        add eax, [x]  ; edx:eax = a+a+b*c*100+x
        adc edx, 0
        mov bl, [a]
        add bl, 10
        cbw
        cwd
        idiv ebx ; eax = (a+a+b*c*100+x)/(a+10)
        add eax, [e]
        add eax, [a] ; eax = (a+a+b*c*100+x)/(a+10)+e*a

        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
