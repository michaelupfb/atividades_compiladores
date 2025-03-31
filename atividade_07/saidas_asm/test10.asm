.global _start
.section .data

.section .text
_start:
mov $1, %rax
push %rax
mov $3, %rax
push %rax
mov $3, %rax
pop %rbx
imul %rbx, %rax
pop %rbx
sub %rbx, %rax
push %rax
mov $5, %rax
push %rax
mov $20, %rax
pop %rbx
mov $0, %rdx
div %rbx
pop %rbx
add %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
