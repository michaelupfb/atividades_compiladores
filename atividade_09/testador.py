import os
import subprocess

PASTA_ASM_CMD = "saidas_asm_cmd"
PASTA_CMD = "programas_cmd"
PASTA_EXPECTED_CMD = "saida_esperada_cmd"

os.makedirs(PASTA_EXPECTED_CMD, exist_ok=True)
os.makedirs(PASTA_ASM_CMD, exist_ok=True)
os.makedirs(PASTA_CMD, exist_ok=True)

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

# Testes para a linguagem Cmd
print("\n--- Testando Linguagem Cmd ---")
for filename in sorted(os.listdir(PASTA_CMD)):
    if filename.endswith(".cmd"):
        nome_base = filename[:-4]
        caminho_cmd = os.path.join(PASTA_CMD, filename)
        caminho_asm = os.path.join(PASTA_ASM_CMD, f"{nome_base}.asm")
        caminho_obj = os.path.join(PASTA_ASM_CMD, f"{nome_base}.o")
        caminho_exec = os.path.join(PASTA_ASM_CMD, nome_base)
        caminho_esperado = os.path.join(PASTA_EXPECTED_CMD, f"{nome_base}.txt")

        print(f"\n🧪 Testando {nome_base}.cmd...")

        # Se o arquivo .asm não existir, compila
        if not os.path.exists(caminho_asm):
            print(f"🛠️ Compilando...")
            try:
                subprocess.run(["python3", "compilador.py", caminho_cmd, "-o", caminho_asm], check=True, capture_output=True)
                print("✅ Compilação OK.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro de compilação:\n{e.stderr.decode()}")
                continue
        else:
            print(f"📄 Usando arquivo .asm já existente: {caminho_asm}")


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