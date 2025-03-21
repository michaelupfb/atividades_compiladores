.global _start
.section .data

.section .text
_start:
mov $2, %rax
push %rax
mov $1, %rax
pop %rbx
add %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
