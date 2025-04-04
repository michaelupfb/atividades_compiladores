.section .bss
.lcomm inicial, 8
.lcomm fator, 8
.lcomm dobrado, 8
.lcomm dividido, 8
.section .text
.global _start
_start:
mov $50, %rax
mov %rax, inicial
mov $2, %rax
mov %rax, fator
mov fator, %rax
push %rax
mov inicial, %rax
pop %rbx
imul %rbx, %rax
mov %rax, dobrado
mov fator, %rax
push %rax
mov inicial, %rax
pop %rbx
mov $0, %rdx
div %rbx
mov %rax, dividido
mov dividido, %rax
push %rax
mov dobrado, %rax
pop %rbx
sub %rbx, %rax
call imprime_num
call sair
.include "runtime.s"
