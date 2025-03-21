.section .text
.global imprime_num
.global sair

# Função imprime_num
# Entrada: número em %rax
imprime_num:
    mov %rax, %rdi
    mov $buf + 20, %rsi
    mov $10, %rbx

.convert_loop:
    xor %rdx, %rdx
    div %rbx
    add $'0', %rdx
    dec %rsi
    mov %dl, (%rsi)
    test %rax, %rax
    jnz .convert_loop

    mov $1, %rax        # syscall write
    mov $1, %rdi        # stdout
    mov %rsi, %rsi
    mov $buf + 20, %rdx
    sub %rsi, %rdx
    syscall

    mov $1, %rax        # syscall write
    mov $1, %rdi
    mov $newline, %rsi
    mov $1, %rdx
    syscall
    ret

# Função sair
sair:
    mov $60, %rax       # syscall: exit
    xor %rdi, %rdi
    syscall

.section .bss
    .lcomm buf, 20

.section .data
newline:
    .ascii "\n"
