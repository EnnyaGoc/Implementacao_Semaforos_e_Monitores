import threading 
import time 
import random 

buffer = [] 
N = 3 

mutex = threading.Semaphore(1) 
empty = threading.Semaphore(N)
full =  threading.Semaphore(0)

def produtor(id):
    for _ in range(3):
        item = random.randint(1, 100)  
        time.sleep(random.random())      
        empty.acquire()                 
        mutex.acquire()        
        buffer.append(item)   
        print(f"Produtor {id} produziu {item} ->  Buffer: {buffer}")
        mutex.release()         
        full.release()                    


def consumidor(id):
    for _ in range(3):
        time.sleep(random.random())  
        full.acquire()              
        mutex.acquire()      
        item = buffer.pop(0)        
        print(f"Consumidor {id} consumiu {item} -> Buffer: {buffer}")
        mutex.release()       
        empty.release()                   


for i in range(2): 
    threading.Thread(target=produtor, args=(i,)).start()

for i in range(1): 
    threading.Thread(target=consumidor, args=(i,)).start()    