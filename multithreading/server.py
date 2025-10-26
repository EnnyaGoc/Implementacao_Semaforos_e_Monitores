import socket
import threading

HOST = "localhost"
PORTA = 3456

def atender_cliente(conn, addr, thread_id):
    print(f"Thread-{thread_id} está conectada com o cliente {addr}")

    try:
        data = conn.recv(1024).decode()
        print(f"Thread-{thread_id} recebeu mensagem {data}")
        resposta = f"Serviço feito pela thread_{thread_id}"
        conn.send(resposta.encode())
        print(f"Thread-{thread_id} respondeu o cliente")

    except Exception as e:
        print(f"Thread-{thread_id} Erro {e}")

    finally:        
        conn.close()
        print(f"Thead-{thread_id} Conexao encerrada \n")


def servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORTA))
    s.listen(7)
    print(f"Servidor iniciado e aguardando conexoes na porta {PORTA}\n")

    thread_id = 0
    while True:
        conn, addr = s.accept()
        thread_id += 1

        t = threading.Thread(target=atender_cliente, args=(conn, addr, thread_id))
        t.start()


if __name__ == "__main__":
    servidor()