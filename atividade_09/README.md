# Atividade 09 - Comandos, Expressões e Variáveis

## Apresentação do Grupo

- **Lucas Farias de Medeiros**
- **Renan Gondim Dias de Albuquerque**
- **Michael da Cunha Pinho**
- **Arthur Miranda Tavares**

## Descrição

Este repositório contém os arquivos da **Atividade 09** da disciplina de Construção de Compiladores I.  
O objetivo foi expandir o compilador anterior para suportar **comandos estruturados** (`if`, `else`, `while`, `return`), além de **expressões aritméticas e lógicas** com variáveis.

A linguagem implementada, chamada **CMD** (Comandos e Declarações), permite:

- Declarações de variáveis.
- Blocos de comandos `{ ... }`.
- Comandos `if-else`, `while`, `return` e atribuições.
- Expressões aritméticas (`+`, `-`, `*`, `/`) e comparações (`<`, `>`, `==`).

O compilador realiza:

- **Análise léxica** (tokenização dos programas).
- **Análise sintática** (montagem da AST).
- **Análise semântica** (checagem de variáveis declaradas).
- **Geração de código Assembly x86-64**.

## Estrutura do Projeto

| Arquivo / Pasta | Descrição |
|:---------------|:-----------|
| `compilador.py` | Código principal do compilador CMD. |
| `testador.py` | Script para compilar todos os testes e comparar saídas automaticamente. |
| `runtime.s` | Código Assembly fornecido para suporte (`imprime_num`, `sair`). |
| `programas_cmd/` | Contém arquivos de teste `.cmd` na linguagem CMD. |
| `saida_esperada_cmd/` | Contém saídas esperadas `.txt` para cada programa de teste. |
| `saidas_asm_cmd/` | Onde os arquivos Assembly `.asm` compilados são gerados. |
| `README.md` | Este arquivo com as instruções e descrição do projeto. |

## Como Usar

### Compilar todos os programas de teste

```bash
python compilador.py
```

Isso irá gerar os arquivos `.asm` correspondentes na pasta `saidas_asm_cmd/`.

### Testar a saída gerada automaticamente

```bash
python testador.py
```

O `testador.py` compara os resultados reais com as saídas esperadas em `saida_esperada_cmd/`.

---

## Contato

Em caso de dúvidas sobre o funcionamento do projeto, entre em contato com qualquer membro do grupo!  
Obrigado!

