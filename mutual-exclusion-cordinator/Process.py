import socket
import threading
import time

def receive_m():
    while True:
        data, addr = s.recvfrom(1024)
        global n_address
        n_address = addr
        if("aceito"==data.decode('utf-8')):
            print("\nRequisição ACEITA\fnIniciando acesso.\n")
            use_rc()
        else:
            print(data.decode('utf-8'))

def send_m():
    while True:
        s.sendto(input("").encode('utf-8'), n_address)

def use_rc():
    print("\nPROCESSANDO EM ANDAMENTO\n")
    time.sleep(5)
    print("\nProcesso Terminado, enviando liberação.\n")
    s.sendto(("liberar").encode('utf-8'), n_address)

host = 'localhost' 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, 0))

_, port = s.getsockname()
print('Porta deste processo:', port)

n_address = (('localhost', 4000))

print("Par inicializado.")

t1 = threading.Thread(target=send_m)
t2 = threading.Thread(target=receive_m)

t1.start()
t2.start()

t1.join()
t2.join()