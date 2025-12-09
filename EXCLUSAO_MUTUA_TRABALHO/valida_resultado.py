import argparse
from collections import defaultdict
from datetime import datetime

def ler_linhas(arquivo):
    linhas = []
    with open(arquivo, "r") as f:
        for linha in f:
            linhas.append(linha.strip())
    return linhas

def extrair_info(linha):
    # Exemplo de linha:
    # Processo 1 - 2025-02-10 22:01:12.315
    partes = linha.split(" - ")

    pid = int(partes[0].replace("Processo ", ""))
    timestamp = partes[1]

    # converter timestamp para datetime
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    return pid, dt

def validar(n, r, arquivo="resultado.txt"):
    linhas = ler_linhas(arquivo)
    esperado = n * r

    print(f"[VALIDAÇÃO] Linhas esperadas: {esperado}")
    print(f"[VALIDAÇÃO] Linhas encontradas: {len(linhas)}")

    if len(linhas) != esperado:
        print("❌ ERRO: número de linhas não confere!")
        return

    print("✔ Número de linhas OK")

    # Validar timestamps crescentes
    anterior = None
    for linha in linhas:
        pid, dt = extrair_info(linha)
        if anterior and dt < anterior:
            print("❌ ERRO: timestamps fora de ordem!")
            print("Linha:", linha)
            return
        anterior = dt

    print("✔ Timestamps em ordem crescente")

    # Validar ocorrências de cada processo
    contagem = defaultdict(int)
    for linha in linhas:
        pid, dt = extrair_info(linha)
        contagem[pid] += 1

    print("\n[VALIDAÇÃO] Contagem por processo:")
    for pid in sorted(contagem):
        print(f"Processo {pid}: {contagem[pid]} vezes")

        if contagem[pid] != r:
            print(f"❌ ERRO: Processo {pid} deveria aparecer {r} vezes!")
            return

    print("\n✔ Todos os processos aparecem r vezes")
    print("\n🎉 VALIDAÇÃO COMPLETA: TUDO CORRETO!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--r", type=int, required=True)
    parser.add_argument("--arquivo", type=str, default="resultado.txt")
    args = parser.parse_args()

    validar(args.n, args.r, args.arquivo)
