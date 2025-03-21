.global _start
.section .data

.section .text
_start:
mov $3, %rax
push %rax
mov $8, %rax
pop %rbx
sub %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
