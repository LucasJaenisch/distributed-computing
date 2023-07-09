import socket
import threading

#Set if the critical region is in use or not
global in_use

in_use = False

queue = []

def receive_m():
    while True:
        data, addr = s.recvfrom(1024)
        # print('\n@@@@@@@@@@@@@', queue)
        global n_address, in_use 
        # print("\n", in_use)
        n_address = addr
        print(data.decode('utf-8'), " recebido de: ", addr)
        if(not in_use):
            if("RC" == data.decode('utf-8') or "rc" == data.decode('utf-8')):
                print("\nRequisição para RC ACEITA\nBLOQUEANDO ACESSO A REGIÃO CRÍTICA PARA OUTROS")
                in_use = True
                s.sendto(("aceito").encode('utf-8'), n_address)
            elif(len(queue) > 0):
                print("PRÓXIMO DA FILA: ", queue[0])
                s.sendto(("aceito").encode('utf-8'), ('localhost', queue[0]))
                queue.pop(0)
        elif("liberar" == data.decode('utf-8')):
            in_use = False
            print("REGIÃO CRÍTICA LIVRE")
        else:
            print("\nREGIÃO CRÍTICA EM USO\nAGUARDE...\n")
            queue.append(addr[1])
            print("FILA DE ESPERA: ", queue)
            s.sendto("A RC ESTÁ EM USO\nADICIONADO A FILA.".encode('utf-8'), n_address)

def send_m():
    while True:
        s.sendto(input("").encode('utf-8'), n_address)



host = 'localhost' 
port = 4000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

n_address = (('localhost', 4001))

print("Cordenador Inicializado.")

process_in_line = []

t1 = threading.Thread(target=send_m)
t2 = threading.Thread(target=receive_m)

t1.start()
t2.start()

t1.join()
t2.join()