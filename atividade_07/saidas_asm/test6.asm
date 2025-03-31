.global _start
.section .data

.section .text
_start:
mov $42, %rax
call imprime_num
call sair
.include "runtime.s"
