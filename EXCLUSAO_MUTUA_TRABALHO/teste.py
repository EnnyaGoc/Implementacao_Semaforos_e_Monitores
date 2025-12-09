from mensagens import *

msg = encode(REQUEST, 4)
print("Mensagem gerada", msg)

tipo, pid = decode(msg)
print("tipo: ", tipo, "processo: ", pid)
