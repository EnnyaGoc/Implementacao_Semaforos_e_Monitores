import socket
import threading
import logging
from datetime import datetime
from mensagens import *
import queue
import time

connections = {} # para guardar os sockets dos processos
fila_pedidos = queue.Queue()  # fila de processos esperando
atendimentos = {}  # {process_id: número de vezes atendido}
rc_ocupada = False  # indica se a região crítica está ocupada
lock_fila = threading.Lock()  # protege acesso à fila
encerrar = False  # variável para encerrar o servidor

# Configurar logging
logging.basicConfig(
    filename='coordenador.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def conexoes(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        logging.info(f"[CONEXAO] Novo processo conectado: {addr}")
        print(f"[CONEXAO] Novo processo conectado: {addr}")
        
        data = client_socket.recv(F)
        tipo, processo_id = decode(data)
        
        logging.info(f"[CONEXAO] Processo {processo_id} identificado")
        print(f"[CONEXAO] Processo {processo_id} identificado.")
        
        connections[processo_id] = client_socket
        client_socket.setblocking(False)

def iniciar_servidor(host="127.0.0.1", porta=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, porta))
    server_socket.listen()
    
    logging.info(f"[SERVIDOR] Coordenador iniciado em {host}:{porta}")
    print(f"[SERVIDOR] Coordenador iniciado em {host}:{porta}")
    
    t = threading.Thread(target=conexoes, args=(server_socket,))
    t.daemon = True
    t.start()
    
    return server_socket

def listen_messages():
    global rc_ocupada
    
    while True:
        # ouvir mensagens de todos os processos conectados
        for pid, sock in list(connections.items()):
            try:
                data = sock.recv(F)
                
                if not data:
                    continue
                
                tipo, processo = decode(data)
                
                # PROCESSOU REQUEST
                if tipo == REQUEST:
                    logging.info(f"[RECEBIDO] REQUEST de Processo {processo}")
                    print(f"[REQUEST] Processo {processo} quer entrar na RC.")
                    
                    with lock_fila:
                        fila_pedidos.put(processo)
                        
                        # Se RC está livre, enviar GRANT imediatamente
                        if not rc_ocupada:
                            prox = fila_pedidos.get()
                            rc_ocupada = True
                            enviar_grant(prox)
                
                # PROCESSOU RELEASE
                elif tipo == RELEASE:
                    logging.info(f"[RECEBIDO] RELEASE de Processo {processo}")
                    print(f"[RELEASE] Processo {processo} saiu da RC.")
                    
                    rc_ocupada = False
                    
                    # conta atendimento
                    atendimentos[processo] = atendimentos.get(processo, 0) + 1
                    
                    # libera próximo da fila
                    with lock_fila:
                        if not fila_pedidos.empty():
                            prox = fila_pedidos.get()  
                            rc_ocupada = True
                            enviar_grant(prox)
            
            except BlockingIOError:
                continue

def enviar_grant(pid):
    logging.info(f"[ENVIADO] GRANT para Processo {pid}")
    print(f"[GRANT] Enviando permissão para o processo {pid}.")
    
    msg = encode(GRANT, pid)
    connections[pid].send(msg)

def interface_usuario():
    global encerrar 

    while not encerrar:

        print("[INTERFACE] Comandos disponíveis:")
        print("1 - Mostrar fila de pedidos")
        print("2 - Mostrar número de atendimentos por processo")
        print("3 - Encerrar coordenador")
    
        comando = input("Digite um comando: ")
        
        if comando == "1":
            with lock_fila:
                fila_list = list(fila_pedidos.queue)
                print("\n[FILA ATUAL]", fila_list)
        
        elif comando == "2":
            print("\n[ATENDIMENTOS]", atendimentos)
        
        elif comando == "3":
            logging.info("[SERVIDOR] Coordenador encerrado")
            print("\nEncerrando coordenador...")
            encerrar = True
        
        else:
            print("Comando inválido.")

        time.sleep(1)

if __name__ == "__main__":
    iniciar_servidor()
    
    t2 = threading.Thread(target=listen_messages)
    t2.daemon = True
    t2.start()
    
    t3 = threading.Thread(target=interface_usuario)
    t3.daemon = True
    t3.start()
    
    logging.info("[SERVIDOR] Coordenador pronto.")
    print("[SERVIDOR] Coordenador pronto.")
    
    while not encerrar:
        time.sleep(1)
