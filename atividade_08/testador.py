# testador.py

import os
import subprocess

PASTA_ASM = "saidas_asm_ev"
PASTA_EV = "expressoes"
PASTA_EXPECTED = "saida_esperada"

os.makedirs(PASTA_EXPECTED, exist_ok=True)

def run_assembler(asm_path, obj_path):
    try:
        subprocess.run(["as", "--64", "-o", obj_path, asm_path], check=True, capture_output=True)
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, e.stderr.decode()

def run_linker(obj_path, exec_path):
    try:
        subprocess.run(["ld", "-o", exec_path, obj_path], check=True, capture_output=True)
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, e.stderr.decode()

def run_executable(exec_path):
    try:
        result = subprocess.run([exec_path], capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.decode()

def read_expected_output(expected_path):
    if os.path.exists(expected_path):
        with open(expected_path, "r") as f:
            return f.read().strip()
    return None

for filename in sorted(os.listdir(PASTA_ASM)):
    if filename.endswith(".asm"):
        nome_base = filename[:-4]
        caminho_asm = os.path.join(PASTA_ASM, filename)
        caminho_obj = os.path.join(PASTA_ASM, f"{nome_base}.o")
        caminho_exec = os.path.join(PASTA_ASM, nome_base)
        caminho_ev = os.path.join(PASTA_EV, f"{nome_base}.ev")
        caminho_esperado = os.path.join(PASTA_EXPECTED, f"{nome_base}.txt")

        print(f"\n🧪 Testando {nome_base}...")

        # Montagem
        print(f"⚙️ Montando...")
        montagem_ok, montagem_erro = run_assembler(caminho_asm, caminho_obj)
        if not montagem_ok:
            print(f"❌ Erro de montagem:\n{montagem_erro}")
            continue
        print("✅ Montagem OK.")

        # Linkagem
        print(f"🔗 Linkando...")
        linkagem_ok, linkagem_erro = run_linker(caminho_obj, caminho_exec)
        if not linkagem_ok:
            print(f"❌ Erro de linkagem:\n{linkagem_erro}")
            continue
        print("✅ Linkagem OK.")

        # Execução
        print(f"🚀 Executando...")
        execucao_ok, saida_exec = run_executable(caminho_exec)
        if not execucao_ok:
            print(f"❌ Erro de execução:\n{saida_exec}")
            continue
        print(f"📄 Saída do programa: '{saida_exec}'")

        # Leitura da saída esperada
        saida_esperada = read_expected_output(caminho_esperado)

        if saida_esperada is not None:
            print(f"🎯 Saída esperada: '{saida_esperada}'")
            if saida_exec == saida_esperada:
                print("✅ Teste PASSOU!")
            else:
                print("❌ Teste FALHOU!")
        else:
            print("⚠️ Arquivo de saída esperada não encontrado. Teste manual necessário.")

        # Limpeza
        if os.path.exists(caminho_obj):
            os.remove(caminho_obj)
        if os.path.exists(caminho_exec):
            os.remove(caminho_exec)