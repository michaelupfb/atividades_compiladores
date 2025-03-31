.global _start
.section .data

.section .text
_start:
mov $5, %rax
push %rax
mov $7, %rax
push %rax
mov $6, %rax
pop %rbx
imul %rbx, %rax
pop %rbx
sub %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
