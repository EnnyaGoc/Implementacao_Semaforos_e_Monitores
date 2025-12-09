import subprocess
import time
import argparse
import sys
import os

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
    
    # Limpar resultado.txt anterior
    if os.path.exists("resultado.txt"):
        os.remove("resultado.txt")
    
    for pid in range(1, N + 1):
        # Detectar sistema operacional e usar comando apropriado
        if sys.platform == "win32":
            # Windows
            subprocess.Popen(
                [sys.executable, "processo.py", "--id", str(pid), "--r", str(R), "--k", str(K)],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Linux/Mac - usar xterm ou gnome-terminal se disponível
            try:
                subprocess.Popen(
                    [sys.executable, "processo.py", "--id", str(pid), "--r", str(R), "--k", str(K)]
                )
            except Exception as e:
                print(f"Erro ao iniciar processo {pid}: {e}")
        
        print(f"[SCRIPT] Processo {pid} iniciado.")
        time.sleep(0.1)  # pequeno retardo para evitar problemas de conexão
    
    print("[SCRIPT] Todos os processos foram iniciados.")

if __name__ == "__main__":
    main()
