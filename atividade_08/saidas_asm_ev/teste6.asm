.section .bss
.lcomm val1, 8
.lcomm val2, 8
.lcomm remainder, 8
.section .text
.global _start
_start:
mov $15, %rax
mov %rax, val1
mov $4, %rax
mov %rax, val2
mov val2, %rax
push %rax
mov val1, %rax
pop %rbx
mov $0, %rdx
div %rbx
push %rax
mov val2, %rax
pop %rbx
imul %rbx, %rax
push %rax
mov val1, %rax
pop %rbx
sub %rbx, %rax
mov %rax, remainder
mov remainder, %rax
call imprime_num
call sair
.include "runtime.s"
