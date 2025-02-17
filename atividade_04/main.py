# // GRUPO:
# // - ARTHUR MIRANDA TAVARES
# // - LUCAS FARIAS DE MEDEIROS
# // - MIHCAEL DA CUNHA PINHO
# // - RENAN GONDIM DIAS DE ALBUQUERQUE

from typing import List

# Definição das classes de token
class TokenType:
    NUMERO = "Numero"
    PAREN_ESQ = "ParenEsq"
    PAREN_DIR = "ParenDir"
    SOMA = "Soma"
    SUBTRACAO = "Sub"
    MULTIPLICACAO = "Mult"
    DIVISAO = "Div"
    EOF = "EOF"

# Classe do Token
class Token:
    def __init__(self, tipo: str, lexema: str, posicao: int):
        self.tipo = tipo
        self.lexema = lexema
        self.posicao = posicao
    
    def __repr__(self):
        return f"<{self.tipo}, '{self.lexema}', {self.posicao}>"

# Analisador léxico
class Lexer:
    def __init__(self, entrada: str):
        self.entrada = entrada
        self.posicao = 0
        self.tamanho = len(entrada)

    def proximo_token(self) -> Token:
        while self.posicao < self.tamanho:
            char = self.entrada[self.posicao]
            
            if char.isspace():
                self.posicao += 1
                continue
            
            if char.isdigit():
                return self._extrair_numero()
            
            if char == '(': 
                return self._criar_token(TokenType.PAREN_ESQ, "(")
            if char == ')': 
                return self._criar_token(TokenType.PAREN_DIR, ")")
            if char == '+': 
                return self._criar_token(TokenType.SOMA, "+")
            if char == '-': 
                return self._criar_token(TokenType.SUBTRACAO, "-")
            if char == '*': 
                return self._criar_token(TokenType.MULTIPLICACAO, "*")
            if char == '/': 
                return self._criar_token(TokenType.DIVISAO, "/")
            
            raise ValueError(f"Erro léxico: caractere inesperado '{char}' na posição {self.posicao}")
        
        return Token(TokenType.EOF, "", self.posicao)
    
    def _extrair_numero(self) -> Token:
        inicio = self.posicao
        while self.posicao < self.tamanho and self.entrada[self.posicao].isdigit():
            self.posicao += 1
        lexema = self.entrada[inicio:self.posicao]
        return Token(TokenType.NUMERO, lexema, inicio)
    
    def _criar_token(self, tipo: str, lexema: str) -> Token:
        token = Token(tipo, lexema, self.posicao)
        self.posicao += 1
        return token
    
    def todos_tokens(self) -> List[Token]:
        tokens = []
        while True:
            token = self.proximo_token()
            tokens.append(token)
            if token.tipo == TokenType.EOF:
                break
        return tokens

def processar_arquivo(arquivo: str):
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    lexer = Lexer(conteudo)
    tokens = lexer.todos_tokens()
    for token in tokens:
        print(token)

# Testes
if __name__ == "__main__":
    processar_arquivo("testes/teste_02.ci")
