import threading #permite criar threads e usar semáforos.
import time #usado para sleep, simulando tempo de produção/consumo.
import random #usado para gerar tempos e valores aleatórios.

buffer = [] # lista usada como buffer compartilhado
N = 5 # tamanho máximo do buffer

mutex = threading.Semaphore(1) # exclusão mútua
empty = threading.Semaphore(N)# controla espaços vazios
full =  threading.Semaphore(0)# controla itens cheios

def produtor(id):
    for _ in range(10):
        item = random.randint(1, 100)     # cria um item aleatório
        time.sleep(random.random())       # simula tempo de produção
        empty.acquire()                   # espera espaço no buffer
        mutex.acquire()                   # trava o buffer
        buffer.append(item)               # adiciona item
        print(f"Produtor {id} produziu {item} | Buffer: {buffer}")
        mutex.release()                   # libera o buffer
        full.release()                    # aumenta contagem de itens


def consumidor(id):
    for _ in range(10):
        time.sleep(random.random())       # simula tempo de espera
        full.acquire()                    # espera até haver item
        mutex.acquire()                   # trava o buffer
        item = buffer.pop(0)              # remove item do buffer
        print(f"Consumidor {id} consumiu {item} | Buffer: {buffer}")
        mutex.release()                   # libera o buffer
        empty.release()                   # aumenta contagem de espaços


for i in range(3): # cria 3 produtores
    threading.Thread(target=produtor, args=(i,)).start()

for i in range(2): # cria 3 produtores
    threading.Thread(target=consumidor, args=(i,)).start()    