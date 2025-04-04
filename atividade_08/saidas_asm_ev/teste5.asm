.section .bss
.lcomm num1, 8
.lcomm num2, 8
.lcomm resultMult, 8
.lcomm resultAdd, 8
.section .text
.global _start
_start:
mov $7, %rax
mov %rax, num1
mov $3, %rax
mov %rax, num2
mov num2, %rax
push %rax
mov num1, %rax
pop %rbx
imul %rbx, %rax
mov %rax, resultMult
mov num2, %rax
push %rax
mov num1, %rax
pop %rbx
add %rbx, %rax
mov %rax, resultAdd
mov resultAdd, %rax
push %rax
mov resultMult, %rax
pop %rbx
add %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
