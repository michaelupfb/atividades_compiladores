.section .bss
.lcomm a, 8
.lcomm b, 8
.lcomm temp, 8
.lcomm final, 8
.section .text
.global _start
_start:
mov $12, %rax
mov %rax, a
mov $6, %rax
mov %rax, b
mov b, %rax
push %rax
mov a, %rax
pop %rbx
sub %rbx, %rax
mov %rax, temp
mov $5, %rax
push %rax
mov temp, %rax
pop %rbx
imul %rbx, %rax
mov %rax, final
mov final, %rax
call imprime_num
call sair
.include "runtime.s"
