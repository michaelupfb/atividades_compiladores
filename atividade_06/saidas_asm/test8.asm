.global _start
.section .data

.section .text
_start:
mov $2, %rax
push %rax
mov $7, %rax
pop %rbx
sub %rbx, %rax
push %rax
mov $8, %rax
pop %rbx
imul %rbx, %rax
push %rax
mov $9, %rax
pop %rbx
add %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
