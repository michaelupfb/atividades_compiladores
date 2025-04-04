.section .bss
.lcomm x, 8
.lcomm y, 8
.section .text
.global _start
_start:
mov $10, %rax
mov %rax, x
mov $2, %rax
push %rax
mov x, %rax
pop %rbx
imul %rbx, %rax
mov %rax, y
mov y, %rax
push %rax
mov x, %rax
pop %rbx
add %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
