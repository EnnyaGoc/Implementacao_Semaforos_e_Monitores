import subprocess
import time
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True, help="Número de processos")
    parser.add_argument("--r", type=int, default=3, help="Repetições por processo")
    parser.add_argument("--k", type=int, default=1, help="Tempo dentro da RC")
    args = parser.parse_args()

    N = args.n
    R = args.r
    K = args.k

    print(f"[SCRIPT] Iniciando {N} processos...")

    for pid in range(1, N + 1):
        subprocess.Popen(
            ["python", "processo.py", "--id", str(pid), "--r", str(R), "--k", str(K)],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print(f"[SCRIPT] Processo {pid} iniciado.")
        time.sleep(0.1)  # sem retardo grande, apenas segurança

    print("[SCRIPT] Todos os processos foram iniciados.")


if __name__ == "__main__":
    main()
