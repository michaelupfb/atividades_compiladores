.section .bss
.lcomm a, 8
.lcomm b, 8
.lcomm c, 8
.section .text
.global _start
_start:
mov $5, %rax
mov %rax, a
mov $10, %rax
mov %rax, b
mov b, %rax
push %rax
mov a, %rax
pop %rbx
add %rbx, %rax
mov %rax, c
mov $3, %rax
push %rax
mov c, %rax
pop %rbx
imul %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
