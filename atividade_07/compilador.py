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
    ("WHITESPACE", r"\s+"),
]


def tokenize(expression):
    tokens = []
    while expression:
        match = None
        for token_type, token_regex in TOKENS:
            match = re.match(token_regex, expression)
            if match:
                if token_type != "WHITESPACE":
                    tokens.append((token_type, match.group(0)))
                expression = expression[len(match.group(0)):]
                break
        if not match:
            raise ValueError("Token inválido encontrado.")
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        self.pos += 1

    def olhar_proximo_token(self):
        return self.current_token()[0] if self.current_token() else None

    def avancar_token(self):
        self.consume()

    def parse(self):
        return self.exp_a()

    def exp_a(self):
        esq = self.exp_m()
        tok = self.olhar_proximo_token()
        while tok in ["PLUS", "MINUS"]:
            self.avancar_token()
            dir = self.exp_m()
            operador = "PLUS" if tok == "PLUS" else "MINUS"
            esq = (operador, esq, dir)
            tok = self.olhar_proximo_token()
        return esq

    def exp_m(self):
        esq = self.prim()
        tok = self.olhar_proximo_token()
        while tok in ["TIMES", "DIVIDE"]:
            self.avancar_token()
            dir = self.prim()
            operador = "TIMES" if tok == "TIMES" else "DIVIDE"
            esq = (operador, esq, dir)
            tok = self.olhar_proximo_token()
        return esq

    def prim(self):
        token = self.current_token()
        if token[0] == "NUM":
            self.avancar_token()
            return int(token[1])
        elif token[0] == "LPAREN":
            self.avancar_token()
            inner = self.exp_a()
            if self.olhar_proximo_token() != "RPAREN":
                raise ValueError("Esperado ')'")
            self.avancar_token()
            return inner
        else:
            raise ValueError("Expressão primária inválida.")


def generate_code(ast):
    code_lines = [
        ".global _start",
        ".section .data",
        "",
        ".section .text",
        "_start:",
    ]

    def gen(node):
        if isinstance(node, int):
            code_lines.append(f"mov ${node}, %rax")
        else:
            op, left, right = node
            gen(right)
            code_lines.append("push %rax")
            gen(left)
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

    gen(ast)
    code_lines.append("call imprime_num")
    code_lines.append("call sair")

    # Inclui runtime no final
    return "\n".join(code_lines) + '\n.include "runtime.s"\n'


def compile_expression(expression):
    tokens = tokenize(expression)
    parser = Parser(tokens)
    ast = parser.parse()
    return generate_code(ast)


# Caminhos
input_dir = "expressoes"
output_dir = "saidas_asm"

os.makedirs(output_dir, exist_ok=True)

# Processar todos os arquivos .ci
for filename in sorted(os.listdir(input_dir)):
    if filename.endswith(".ci"):
        with open(os.path.join(input_dir, filename), "r") as f:
            expression = f.read().strip()
            try:
                asm_code = compile_expression(expression)
                out_filename = filename.replace(".ci", ".asm")
                with open(os.path.join(output_dir, out_filename), "w") as out_f:
                    out_f.write(asm_code)
                print(f"✅ Gerado: {out_filename}")
            except Exception as e:
                print(f"❌ Erro em {filename}: {e}")