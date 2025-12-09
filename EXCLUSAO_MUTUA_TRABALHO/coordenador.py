import socket
import threading
from mensagens import *   
import queue
import time


connections = {}  
fila_pedidos = queue.Queue()       # fila de processos esperando
atendimentos = {}                  # {process_id: número de vezes atendido}
rc_ocupada = False                 # indica se a região crítica está ocupada
lock_fila = threading.Lock()       # protege acesso à fila


def conexoes(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        print(f"[CONEXÃO] Novo processo conectado: {addr}")

        data = client_socket.recv(F)
        tipo, processo_id = decode(data)

        print(f"[CONEXÃO] Processo {processo_id} identificado.")

        connections[processo_id] = client_socket
        client_socket.setblocking(False)



def iniciar_servidor(host="127.0.0.1", porta=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, porta))
    server_socket.listen()

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
    print(f"[GRANT] Enviando permissão para o processo {pid}.")
    msg = encode(GRANT, pid)
    connections[pid].send(msg)


def interface_usuario():
    print("[INTERFACE] Comandos disponíveis:")
    print("1 - Mostrar fila de pedidos")
    print("2 - Mostrar número de atendimentos por processo")
    print("3 - Encerrar coordenador")

    while True:
        comando = input("Digite um comando: ")

        if comando == "1":
            with lock_fila:
                fila_list = list(fila_pedidos.queue)
            print("\n[FILA ATUAL]", fila_list)

        elif comando == "2":
            print("\n[ATENDIMENTOS]", atendimentos)

        elif comando == "3":
            print("\nEncerrando coordenador...")
            exit(0)

        else:
            print("Comando inválido.")



if __name__ == "__main__":
    iniciar_servidor()

    t2 = threading.Thread(target=listen_messages)
    t2.daemon = True
    t2.start()

    t3 = threading.Thread(target=interface_usuario)
    t3.daemon = True
    t3.start()

    print("[SERVIDOR] Coordenador pronto.")
    while True:
        pass
