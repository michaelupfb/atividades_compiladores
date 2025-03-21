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

    def parse(self):
        return self.expression()

    def expression(self):
        token = self.current_token()
        if token is None:
            raise ValueError("Expressão incompleta.")

        if token[0] == "NUM":
            value = int(token[1])
            self.consume()
            return value
        elif token[0] == "LPAREN":
            self.consume()
            inner = self.expression()
            token = self.current_token()

            if token is None:
                raise ValueError("Parêntese aberto não fechado.")

            # Verifica se é uma expressão binária ou apenas um número entre parênteses
            if token[0] in ["PLUS", "MINUS", "TIMES", "DIVIDE"]:
                operator = token[0]
                self.consume()
                right = self.expression()
                if self.current_token() is None or self.current_token()[0] != "RPAREN":
                    raise ValueError("Esperado ')'")
                self.consume()
                return (operator, inner, right)
            elif token[0] == "RPAREN":
                self.consume()
                return inner
            else:
                raise ValueError("Expressão inválida dentro dos parênteses.")

        raise ValueError("Expressão inválida.")


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
