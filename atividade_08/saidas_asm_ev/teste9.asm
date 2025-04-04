.section .bss
.lcomm primeiro, 8
.lcomm segundo, 8
.lcomm terceiro, 8
.section .text
.global _start
_start:
mov $30, %rax
mov %rax, primeiro
mov $5, %rax
mov %rax, segundo
mov segundo, %rax
push %rax
mov primeiro, %rax
pop %rbx
mov $0, %rdx
div %rbx
mov %rax, terceiro
mov terceiro, %rax
push %rax
mov primeiro, %rax
pop %rbx
sub %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
