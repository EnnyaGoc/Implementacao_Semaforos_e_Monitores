import socket
import time

HOST = "localhost"
PORTA = 3456


def cliente(mensagem):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORTA))

        s.send(mensagem.encode())

        resposta = s.recv(1024).decode()
        print("Resposta do servidor: ", resposta)


        s.close()

    except Exception as e:
        print("Erro do cliente: ", e)


if __name__ == "__main__":
    for i in range(7):
        cliente("Preciso de um serviço seu...")
        time.sleep(0.5)
