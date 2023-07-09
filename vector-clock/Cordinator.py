import socket
import threading

#Set if the critical region is in use or not
global in_use
in_use = False

queue = []
process_network = []

def receive_m():
    while True:
        data, addr = s.recvfrom(1024)
        global n_address, in_use 
        n_address = addr
        print(data.decode('utf-8'), "recebido de:", addr[1])
        #if(in_use):
            # if("RC" == data.decode('utf-8') or "rc" == data.decode('utf-8')):
            #     print("\nRequisição para RC ACEITA\nBLOQUEANDO ACESSO A REGIÃO CRÍTICA PARA OUTROS")
            #     in_use = True
            #     s.sendto(("aceito").encode('utf-8'), n_address)

        # if("liberar" == data.decode('utf-8')):
        #     in_use = False
        #     print("REGIÃO CRÍTICA LIVRE")

        #     if(len(queue) > 0): 
        #         print("PRÓXIMO DA FILA: ", queue[0])
        #         s.sendto(("aceito").encode('utf-8'), ('localhost', queue[0]))
        #         queue.pop(0)

        if("connect" == data.decode('utf-8')):
            process_network.append(addr[-1])
            print("Novo processo na rede: ", addr[-1])
            notice_new_process(addr[-1])

        else:
            print(data.decode('utf-8'))
            # print("\nREGIÃO CRÍTICA EM USO\nAGUARDE...\n")
            # queue.append(addr[1])
            # print("FILA DE ESPERA: ", queue)
            # s.sendto("A RC ESTÁ EM USO\nADICIONADO A FILA.".encode('utf-8'), n_address)

def send_m():
    while True:
        s.sendto(input("").encode('utf-8'), n_address)

def notice_new_process(new_process_id):
    for process in process_network:
        s.sendto(('new_process ' + str(new_process_id)).encode('utf-8'), ('localhost', process))
    for process in process_network:
        s.sendto(('new_process ' + str(process)).encode('utf-8'), ('localhost', new_process_id))


host = 'localhost' 
port = 4000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

n_address = (('localhost', 4001))

print("Cordenador inicializado.")

process_in_line = []

t1 = threading.Thread(target=send_m)
t2 = threading.Thread(target=receive_m)

t1.start()
t2.start()

t1.join()
t2.join()
