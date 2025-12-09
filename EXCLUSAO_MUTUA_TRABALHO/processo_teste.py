import socket
from mensagens import *
import time

HOST = "127.0.0.1"
PORT = 5000
PID = 3

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# enviar ID
s.send(encode(REQUEST, PID))

# enviar REQUEST real
time.sleep(1)
s.send(encode(REQUEST, PID))

# receber GRANT
grant = s.recv(F)
print("Recebi:", decode(grant))

# enviar RELEASE
time.sleep(1)
s.send(encode(RELEASE, PID))

print("Processo terminou.")
