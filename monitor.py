import threading
import time
import random

class BufferMonitor:
    def __init__(self, tamanho):
        self.buffer = []
        self.tamanho = tamanho
        self.cond = threading.Condition()  # lock + condição

    def inserir(self, item, id):
        with self.cond:  # entra no monitor (lock automático)
            while len(self.buffer) == self.tamanho:  # buffer cheio
                self.cond.wait()  # espera até alguém consumir
            self.buffer.append(item)
            print(f"Produtor {id} produziu {item} | Buffer: {self.buffer}")
            self.cond.notify_all()  # acorda consumidores

    def retirar(self, id):
        with self.cond:  # entra no monitor (lock automático)
            while len(self.buffer) == 0:  # buffer vazio
                self.cond.wait()  # espera até alguém produzir
            item = self.buffer.pop(0)
            print(f"Consumidor {id} consumiu {item} | Buffer: {self.buffer}")
            self.cond.notify_all()  # acorda produtores
            return item

# Teste com threads
buffer = BufferMonitor(5)

def produtor(id):
    for _ in range(10):  # produz só 10 itens para teste
        item = random.randint(1, 100)
        time.sleep(random.random())
        buffer.inserir(item, id)

def consumidor(id):
    for _ in range(10):  # consome só 10 itens para teste
        time.sleep(random.random())
        buffer.retirar(id)

for i in range(2):
    threading.Thread(target=produtor, args=(i,)).start()

for i in range(2):
    threading.Thread(target=consumidor, args=(i,)).start()
