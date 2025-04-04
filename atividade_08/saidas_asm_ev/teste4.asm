.section .bss
.lcomm counter, 8
.lcomm increment, 8
.section .text
.global _start
_start:
mov $0, %rax
mov %rax, counter
mov $5, %rax
mov %rax, increment
mov increment, %rax
push %rax
mov counter, %rax
pop %rbx
add %rbx, %rax
mov %rax, counter
mov increment, %rax
push %rax
mov counter, %rax
pop %rbx
add %rbx, %rax
mov %rax, counter
mov counter, %rax
call imprime_num
call sair
.include "runtime.s"
