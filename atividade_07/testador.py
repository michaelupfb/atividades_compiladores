import os
import subprocess

PASTA_ASM = "saidas_asm"
PASTA_EXP = "expressoes"

for filename in sorted(os.listdir(PASTA_ASM)):
    if filename.endswith(".asm"):
        nome_base = filename[:-4]
        caminho_asm = os.path.join(PASTA_ASM, filename)
        caminho_obj = os.path.join(PASTA_ASM, f"{nome_base}.o")
        caminho_exec = os.path.join(PASTA_ASM, nome_base)
        caminho_exp = os.path.join(PASTA_EXP, f"{nome_base}.ci")

        print(f"\n🔧 Compilando {filename}...")

        try:
            # Etapa 1: Montar .asm -> .o
            subprocess.run(
                ["as", "--64", "-o", caminho_obj, caminho_asm], check=True)

            # Etapa 2: Linkar .o -> executável
            subprocess.run(["ld", "-o", caminho_exec, caminho_obj], check=True)

            print(f"✅ Compilado com sucesso: {nome_base}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao compilar {filename}: {e}")
            continue

        # Verifica se expressão existe
        if not os.path.exists(caminho_exp):
            print(f"❌ Expressão não encontrada: {caminho_exp}")
            continue

        try:
            # Executa binário e captura saída
            resultado_exec = subprocess.run(
                [caminho_exec], capture_output=True, text=True)
            saida_exec = resultado_exec.stdout.strip()

            # Lê e avalia expressão
            with open(caminho_exp, "r") as f:
                expressao = f.read().strip()
            resultado_avaliado = eval(expressao)
            if type(resultado_avaliado) == float:
                resultado_avaliado = int(resultado_avaliado)

            resultado_esperado = str(resultado_avaliado)

            # Comparação
            print(f"🖨️ Saída do programa: {saida_exec}")
            print(f"🧮 Resultado esperado: {resultado_esperado}")

            if saida_exec == resultado_esperado:
                print("✅ Resultado CORRETO")
            else:
                print("❌ Resultado INCORRETO")

        except Exception as e:
            print(f"⚠️ Erro ao testar {nome_base}: {e}")

        finally:
            # Limpeza dos arquivos gerados (.o e executável)
            if os.path.exists(caminho_obj):
                os.remove(caminho_obj)
            if os.path.exists(caminho_exec):
                os.remove(caminho_exec)
