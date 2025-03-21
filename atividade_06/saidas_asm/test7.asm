.global _start
.section .data

.section .text
_start:
mov $25, %rax
push %rax
mov $4, %rax
push %rax
mov $100, %rax
pop %rbx
mov $0, %rdx
div %rbx
pop %rbx
add %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
