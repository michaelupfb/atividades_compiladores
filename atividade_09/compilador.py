import os
import re

# Lista de tokens
TOKENS = [
    ("IF", r"if"),
    ("ELSE", r"else"),
    ("WHILE", r"while"),
    ("RETURN", r"return"),
    ("LT", r"<"),
    ("GT", r">"),
    ("EQ", r"=="),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("NUM", r"\d+"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("TIMES", r"\*"),
    ("DIVIDE", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("EQUALS", r"="),
    ("SEMI", r";"),
    ("ID", r"[a-zA-Z][a-zA-Z0-9]*"),
    ("WHITESPACE", r"\s+"),
]

def tokenize(program):
    tokens = []
    i = 0
    while i < len(program):
        match = None
        for token_type, token_regex in TOKENS:
            regex = re.compile("^" + token_regex)
            match = regex.match(program[i:])
            if match:
                lexeme = match.group(0)
                if token_type == "ID":
                    if lexeme == "if":
                        tokens.append(("IF", lexeme))
                    elif lexeme == "else":
                        tokens.append(("ELSE", lexeme))
                    elif lexeme == "while":
                        tokens.append(("WHILE", lexeme))
                    elif lexeme == "return":
                        tokens.append(("RETURN", lexeme))
                    else:
                        tokens.append((token_type, lexeme))
                elif token_type != "WHITESPACE":
                    tokens.append((token_type, lexeme))
                i += len(lexeme)
                match = True
                break
        if not match:
            raise ValueError(f"Token inválido encontrado na posição {i}: '{program[i:i+20]}...'")
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbols = set()

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, token_type):
        if self.current_token() and self.current_token()[0] == token_type:
            self.pos += 1
        else:
            expected = token_type
            actual = self.current_token()[0] if self.current_token() else "fim do arquivo"
            raise ValueError(f"Esperado token do tipo '{expected}', mas encontrado '{actual}'")

    def programa(self):
        declaracoes = []
        while self.current_token() and self.current_token()[0] == "ID":
            declaracoes.append(self.decl())

        self.consume("LBRACE")
        comandos = self.bloco_de_comandos()
        self.consume("RBRACE")

        return ("PROGRAMA", declaracoes, comandos)

    def decl(self):
        nome_var = self.current_token()[1]
        self.consume("ID")
        self.consume("EQUALS")
        expr = self.exp()
        self.consume("SEMI")
        self.symbols.add(nome_var)
        return ("DECL", nome_var, expr)

    def bloco_de_comandos(self):
        comandos = []
        while self.current_token() and self.current_token()[0] != "RBRACE":
            comandos.append(self.comando())
        return comandos

    def comando(self):
        if self.current_token()[0] == "IF":
            return self.comando_if()
        elif self.current_token()[0] == "WHILE":
            return self.comando_while()
        elif self.current_token()[0] == "ID":
            return self.comando_atribuicao()
        elif self.current_token()[0] == "RETURN":
            return self.comando_return()
        else:
            raise ValueError(f"Comando inesperado: {self.current_token()}")

    def comando_if(self):
        self.consume("IF")
        condicao = self.exp_comparacao()
        self.consume("LBRACE")
        bloco_if = self.bloco_de_comandos()
        self.consume("RBRACE")
        self.consume("ELSE")
        self.consume("LBRACE")
        bloco_else = self.bloco_de_comandos()
        self.consume("RBRACE")
        return ("IF", condicao, bloco_if, bloco_else)

    def comando_while(self):
        self.consume("WHILE")
        condicao = self.exp_comparacao()
        self.consume("LBRACE")
        bloco_while = self.bloco_de_comandos()
        self.consume("RBRACE")
        return ("WHILE", condicao, bloco_while)

    def comando_atribuicao(self):
        nome_var = self.current_token()[1]
        if nome_var not in self.symbols:
            raise ValueError(f"Variável '{nome_var}' não declarada antes da atribuição.")
        self.consume("ID")
        self.consume("EQUALS")
        expr = self.exp()
        self.consume("SEMI")
        return ("ATRIBUICAO", nome_var, expr)
    
    def comando_return(self):
        self.consume("RETURN")
        resultado = self.exp()
        self.consume("SEMI")
        return ("RETURN", resultado)

    def exp_comparacao(self):
        esq = self.exp()
        while self.current_token() and self.current_token()[0] in ["LT", "GT", "EQ"]:
            op_token = self.current_token()
            self.consume(op_token[0])
            dir = self.exp()
            esq = (op_token[0], esq, dir)
        return esq

    def exp(self):
        esq = self.exp_m()
        while self.current_token() and self.current_token()[0] in ["PLUS", "MINUS"]:
            op_token = self.current_token()
            self.consume(op_token[0])
            dir = self.exp_m()
            esq = (op_token[0], esq, dir)
        return esq

    def exp_m(self):
        esq = self.prim()
        while self.current_token() and self.current_token()[0] in ["TIMES", "DIVIDE"]:
            op_token = self.current_token()
            self.consume(op_token[0])
            dir = self.prim()
            esq = (op_token[0], esq, dir)
        return esq

    def prim(self):
        token = self.current_token()
        if token:
            if token[0] == "NUM":
                self.consume("NUM")
                return ("NUM", int(token[1]))
            elif token[0] == "ID":
                self.consume("ID")
                return ("VAR", token[1])
            elif token[0] == "LPAREN":
                self.consume("LPAREN")
                inner = self.exp()
                self.consume("RPAREN")
                return inner
            else:
                raise ValueError(f"Expressão primária inválida: {token}")
        else:
            raise ValueError("Fim inesperado do arquivo durante a análise de uma expressão primária.")

    def parse(self):
        return self.programa()

def generate_code(ast):
    code_lines = [
        ".section .bss",
    ]
    declarations = ast[1]
    declared_variables = set()
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

    def add_debug_comment(message):
        code_lines.append(f"# DEBUG: {message}")

    def gen_expr(node):
        if node[0] == "NUM":
            code_lines.append(f"mov ${node[1]}, %rax")
        elif node[0] == "VAR":
            code_lines.append(f"mov {node[1]}, %rax")
        elif node[0] in ["LT", "GT", "EQ"]:
            op, left, right = node
            gen_expr(left)     # avalia o lado esquerdo, deixa em %rax
            code_lines.append("push %rax")  # salva %rax
            gen_expr(right)    # avalia o lado direito, fica em %rax
            code_lines.append("pop %rbx")   # recupera o lado esquerdo para %rbx
            code_lines.append("cmp %rax, %rbx")  # compara %rbx - %rax
            if op == "LT":
                code_lines.append("setl %al")
            elif op == "GT":
                code_lines.append("setg %al")
            elif op == "EQ":
                code_lines.append("setz %al")
            code_lines.append("movzx %al, %rax")  # estende para 64 bits
        else:
            op, left, right = node
            gen_expr(left)
            code_lines.append("push %rax")
            gen_expr(right)
            code_lines.append("pop %rbx")
            if op == "PLUS":
                code_lines.append("add %rbx, %rax")
            elif op == "MINUS":
                code_lines.append("sub %rbx, %rax")
            elif op == "TIMES":
                code_lines.append("imul %rbx, %rax")
            elif op == "DIVIDE":
                code_lines.append("cqo")
                code_lines.append("idiv %rbx")

    label_counter = [0]

    def gen_comando(comando):
        nonlocal label_counter
        tipo = comando[0]
        if tipo == "ATRIBUICAO":
            nome_var = comando[1]
            expr = comando[2]
            gen_expr(expr)
            code_lines.append(f"mov %rax, {nome_var}")
        elif tipo == "IF":
            condicao, bloco_if, bloco_else = comando[1], comando[2], comando[3]
            label_if_false = f".LIF_FALSE_{label_counter[0]}"
            label_if_end = f".LIF_END_{label_counter[0]}"
            label_counter[0] += 1
            gen_expr(condicao)
            code_lines.append("cmp $0, %rax")
            code_lines.append(f"je {label_if_false}")
            for cmd in bloco_if:
                gen_comando(cmd)
            code_lines.append(f"jmp {label_if_end}")
            code_lines.append(f"{label_if_false}:")
            for cmd in bloco_else:
                gen_comando(cmd)
            code_lines.append(f"{label_if_end}:")
        elif tipo == "WHILE":
            condicao, bloco_while = comando[1], comando[2]
            label_start = f".LWHILE_START_{label_counter[0]}"
            label_end = f".LWHILE_END_{label_counter[0]}"
            label_counter[0] += 1
            code_lines.append(f"{label_start}:")
            gen_expr(condicao)
            code_lines.append("cmp $0, %rax")
            code_lines.append(f"je {label_end}")
            for cmd in bloco_while:
                gen_comando(cmd)
            code_lines.append(f"jmp {label_start}")
            code_lines.append(f"{label_end}:")
        elif tipo == "RETURN":
            expr = comando[1]
            gen_expr(expr)
            code_lines.append("call imprime_num")
            code_lines.append("call sair")

    for decl in declarations:
        var_name = decl[1]
        expr = decl[2]
        gen_expr(expr)
        code_lines.append(f"mov %rax, {var_name}")

    for comando in ast[2]:
        gen_comando(comando)

    return "\n".join(code_lines) + '\n.include "runtime.s"\n'

def compile_program(program):
    tokens = tokenize(program)
    parser = Parser(tokens)
    ast = parser.parse()
    return generate_code(ast)

# Caminhos
input_dir = "programas_cmd"
output_dir = "saidas_asm_cmd"
expected_output_dir = "saida_esperada_cmd"

os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(expected_output_dir, exist_ok=True)

# Processar todos os arquivos
for filename in sorted(os.listdir(input_dir)):
    if filename.endswith(".cmd"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".cmd", ".asm"))
        expected_output_path = os.path.join(expected_output_dir, filename.replace(".cmd", ".txt"))

        try:
            with open(input_path, "r") as f:
                program = f.read().strip()
                tokens = tokenize(program)
                # Debbug:
                # print(f"Tokens de {filename}: {tokens}")
                parser = Parser(tokens)
                ast = parser.parse()
                # Debbug:
                # print(f"AST de {filename}: {ast}")
                asm_code = generate_code(ast)
                with open(output_path, "w") as out_f:
                    out_f.write(asm_code)
                print(f"✅ Gerado: {filename.replace('.cmd', '.asm')}")
        except ValueError as e:
            print(f"❌ Erro em {filename}: {e}")