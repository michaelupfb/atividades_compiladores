.section .bss
.lcomm x, 8
.lcomm y, 8
.lcomm z, 8
.section .text
.global _start
_start:
mov $100, %rax
mov %rax, x
mov $20, %rax
mov %rax, y
mov y, %rax
push %rax
mov x, %rax
pop %rbx
mov $0, %rdx
div %rbx
mov %rax, z
mov $1, %rax
push %rax
mov z, %rax
pop %rbx
sub %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
