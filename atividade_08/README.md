# Atividade 08 - Expressões com Variáveis 

## Apresentação do Grupo

- LUCAS FARIAS DE MEDEIROS
- RENAN GONDIM DIAS DE ALBUQUERQUE
- MICHAEL DA CUNHA PINHO
- ARTHUR MIRANDA TAVARES

## Descrição

Este repositório contém os arquivos referentes à Atividade 08 da disciplina de Compiladores. O objetivo desta atividade é estender o compilador desenvolvido na Atividade 07 para suportar a declaração e o uso de variáveis em expressões. Isso envolve modificações em todas as fases do compilador: análise léxica, análise sintática e geração de código, além da introdução de uma tabela de símbolos para gerenciar os nomes das variáveis e realizar uma análise semântica básica para verificar se as variáveis utilizadas foram declaradas. A linguagem implementada, denominada EV (Expressões com Variáveis), permite uma sequência de declarações de variáveis seguida por uma expressão final cujo resultado é o do programa.

## Conteúdo

- **[compilador.py]**: Arquivo com o código-fonte da implementação.
- **[testador.py]**: Arquivo com as funções de teste para verificar a corretude da implementação, incluindo testes com declarações e uso de variáveis, bem como a detecção de variáveis não declaradas.
- **[runtime.s]**: Arquivo runtime em assembly (.s) fornecido para suporte à execução do código gerado.
- **[expressoes/]**: Diretório contendo arquivos de teste com programas na linguagem EV (.ev).
- **[saida_esperada/]**: Diretório contendo os arquivos de texto (.txt) com a saída esperada para cada arquivo de teste em expressoes/.
- **[saidas_asm_ev/]**:Diretório onde serão gerados os arquivos assembly (.s) resultantes da compilação dos arquivos em expressoes/.
- **README.md**: Este arquivo, contendo informações sobre a atividade, a linguagem EV implementada e o grupo.

## Contato

Em caso de dúvidas sobre o funcionamento do código, pode entrar em contato com qualquer membro do grupo! Obrigado!
