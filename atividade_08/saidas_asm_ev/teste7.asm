.section .bss
.lcomm p, 8
.lcomm q, 8
.lcomm r, 8
.section .text
.global _start
_start:
mov $2, %rax
mov %rax, p
mov $8, %rax
mov %rax, q
mov $2, %rax
push %rax
mov q, %rax
push %rax
mov p, %rax
pop %rbx
add %rbx, %rax
pop %rbx
imul %rbx, %rax
mov %rax, r
mov p, %rax
push %rax
mov r, %rax
pop %rbx
mov $0, %rdx
div %rbx
call imprime_num
call sair
.include "runtime.s"
