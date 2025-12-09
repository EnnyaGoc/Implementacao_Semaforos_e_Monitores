import socket
import time
import argparse
from mensagens import *

def escrever_no_arquivo(pid):
    """Função que representa a região crítica."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    milis = int((time.time() % 1) * 1000)
    linha = f"Processo {pid} - {timestamp}.{milis:03d}\n"
    
    with open("resultado.txt", "a") as f:
        f.write(linha)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--r", type=int, default=3)
    parser.add_argument("--k", type=int, default=1)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    
    args = parser.parse_args()
    
    PID = args.id
    R = args.r
    K = args.k
    
    # Criar socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.host, args.port))
    
    # Enviar primeira mensagem para registrar ID
    s.send(encode(REQUEST, PID))
    
    print(f"[PROCESSO {PID}] Conectado ao coordenador.")
    
    for i in range(R):
        print(f"[PROCESSO {PID}] Enviando REQUEST ({i+1}/{R})...")
        s.send(encode(REQUEST, PID))
        
        # Esperar GRANT
        while True:
            data = s.recv(F)
            tipo, pid = decode(data)
            
            if tipo == GRANT:
                break
        
        print(f"[PROCESSO {PID}] Recebi GRANT! Entrando na RC...")
        
        # Região crítica
        escrever_no_arquivo(PID)
        
        # Aguardar k segundos DENTRO da região crítica
        time.sleep(K)
        
        print(f"[PROCESSO {PID}] Saindo da RC. Enviando RELEASE.")
        s.send(encode(RELEASE, PID))
    
    print(f"[PROCESSO {PID}] Finalizado.")
    s.close()

if __name__ == "__main__":
    main()
