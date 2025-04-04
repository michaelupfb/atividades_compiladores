# compilador.py

import os
import re

# Definir tokens
TOKENS = [
    ("NUM", r"\d+"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("TIMES", r"\*"),
    ("DIVIDE", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("EQUALS", r"="),  # Novo token para o sinal de igual
    ("SEMI", r";"),    # Novo token para ponto e vírgula
    ("ID", r"[a-zA-Z][a-zA-Z0-9]*"),  # Novo token para identificadores
    ("WHITESPACE", r"\s+"),
]


def tokenize(program):
    tokens = []
    while program:
        match = None
        for token_type, token_regex in TOKENS:
            match = re.match(token_regex, program)
            if match:
                if token_type != "WHITESPACE":
                    tokens.append((token_type, match.group(0)))
                program = program[len(match.group(0)):]
                break
        if not match:
            raise ValueError(f"Token inválido encontrado: '{program[:20]}...'")
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbols = set()  # Tabela de símbolos para variáveis declaradas

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        self.pos += 1

    def olhar_proximo_token(self):
        return self.current_token()[0] if self.current_token() else None

    def avancar_token(self):
        self.consume()

    def programa(self):
        declaracoes = []
        while self.olhar_proximo_token() == "ID":
            declaracoes.append(self.decl())
        if self.olhar_proximo_token() != "EQUALS":
            raise ValueError("Esperado '=' para a expressão final.")
        self.avancar_token()  # Consome o '='
        resultado = self.exp()
        return ("PROGRAMA", declaracoes, resultado)

    def decl(self):
        if self.olhar_proximo_token() != "ID":
            raise ValueError("Esperado um nome de variável na declaração.")
        nome_var = self.current_token()[1]
        self.avancar_token()
        if self.olhar_proximo_token() != "EQUALS":
            raise ValueError(f"Esperado '=' após '{nome_var}'.")
        self.avancar_token()
        expr = self.exp()
        if self.olhar_proximo_token() != "SEMI":
            raise ValueError("Esperado ';' no final da declaração.")
        self.avancar_token()
        self.symbols.add(nome_var)  # Adiciona a variável à tabela de símbolos
        return ("DECL", nome_var, expr)

    def exp(self):
        esq = self.exp_m()
        while self.olhar_proximo_token() in ["PLUS", "MINUS"]:
            op_token = self.current_token()
            self.avancar_token()
            dir = self.exp_m()
            esq = (op_token[0], esq, dir)
        return esq

    def exp_m(self):
        esq = self.prim()
        while self.olhar_proximo_token() in ["TIMES", "DIVIDE"]:
            op_token = self.current_token()
            self.avancar_token()
            dir = self.prim()
            esq = (op_token[0], esq, dir)
        return esq

    def prim(self):
        token = self.current_token()
        if token[0] == "NUM":
            self.avancar_token()
            return ("NUM", int(token[1]))
        elif token[0] == "ID":
            var_name = token[1]
            if var_name not in self.symbols:
                raise ValueError(f"Variável '{var_name}' não declarada.")
            self.avancar_token()
            return ("VAR", var_name)
        elif token[0] == "LPAREN":
            self.avancar_token()
            inner = self.exp()
            if self.olhar_proximo_token() != "RPAREN":
                raise ValueError("Esperado ')'")
            self.avancar_token()
            return inner
        else:
            raise ValueError(f"Expressão primária inválida: {token}")

    def parse(self):
        return self.programa()


def generate_code(ast):
    code_lines = [
        ".section .bss",
    ]
    declarations = ast[1]
    declared_variables = set()  # Conjunto para rastrear variáveis declaradas
    for decl in declarations:
        var_name = decl[1]
        if var_name not in declared_variables:
            code_lines.append(f".lcomm {var_name}, 8")
            declared_variables.add(var_name)
    code_lines.extend([
        ".section .text",
        ".global _start",
        "_start:",
    ])

    def gen_expr(node):
        if node[0] == "NUM":
            code_lines.append(f"mov ${node[1]}, %rax")
        elif node[0] == "VAR":
            code_lines.append(f"mov {node[1]}, %rax")
        else:
            op, left, right = node
            gen_expr(right)
            code_lines.append("push %rax")
            gen_expr(left)
            code_lines.append("pop %rbx")
            if op == "PLUS":
                code_lines.append("add %rbx, %rax")
            elif op == "MINUS":
                code_lines.append("sub %rbx, %rax")
            elif op == "TIMES":
                code_lines.append("imul %rbx, %rax")
            elif op == "DIVIDE":
                code_lines.append("mov $0, %rdx")
                code_lines.append("div %rbx")

    for decl in declarations:
        var_name = decl[1]
        expr = decl[2]
        gen_expr(expr)
        code_lines.append(f"mov %rax, {var_name}")

    final_expression = ast[2]
    gen_expr(final_expression)

    code_lines.append("call imprime_num")
    code_lines.append("call sair")

    # Inclui runtime no final
    return "\n".join(code_lines) + '\n.include "runtime.s"\n'


def compile_program(program):
    tokens = tokenize(program)
    parser = Parser(tokens)
    ast = parser.parse()
    return generate_code(ast)


# Caminhos
input_dir = "expressoes"
output_dir = "saidas_asm_ev"

os.makedirs(output_dir, exist_ok=True)

# Processar todos os arquivos .ev
for filename in sorted(os.listdir(input_dir)):
    if filename.endswith(".ev"):
        with open(os.path.join(input_dir, filename), "r") as f:
            program = f.read().strip()
            try:
                asm_code = compile_program(program)
                out_filename = filename.replace(".ev", ".asm")
                with open(os.path.join(output_dir, out_filename), "w") as out_f:
                    out_f.write(asm_code)
                print(f"✅ Gerado: {out_filename}")
            except ValueError as e:
                print(f"❌ Erro em {filename}: {e}")