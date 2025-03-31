.global _start
.section .data

.section .text
_start:
mov $7, %rax
push %rax
mov $2, %rax
push %rax
mov $10, %rax
pop %rbx
mov $0, %rdx
div %rbx
pop %rbx
add %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
