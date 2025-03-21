.global _start
.section .data

.section .text
_start:
mov $5, %rax
push %rax
mov $2, %rax
push %rax
mov $4, %rax
push %rax
mov $3, %rax
pop %rbx
add %rbx, %rax
pop %rbx
imul %rbx, %rax
pop %rbx
sub %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
