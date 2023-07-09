import socket
import threading

def receive_m():
    while True:
        data, addr = s.recvfrom(1024)
        global n_address
        n_address = addr
        print(data.decode('utf-8'))

def send_m():
    while True:
        s.sendto(input(" ➤ ").encode('utf-8'), n_address)

host = 'localhost' 
port = 4005

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
n_address = (('localhost', 4000))

print("Par inicializado.")

t1 = threading.Thread(target=send_m)
t2 = threading.Thread(target=receive_m)

t1.start()
t2.start()

t1.join()
t2.join()