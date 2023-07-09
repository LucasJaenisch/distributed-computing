import threading
import socket
import time
import sys
import os

global relative_time
global id
global score

operation = 'op'

relative_time = 1
score = 1000

messages_queue = [] #list of messages
ack_queue = []

def receive_m():
    while True:
        data, addr = s.recvfrom(1024)
        global n_address

        global score
        n_address = addr
        if("negado"==data.decode('utf-8')):
            print("\nRequisção NEGADA\n")
        elif("aceito"==data.decode('utf-8')):
            print("\nRequisição ACEITA\nIniciando acesso.\n")
            use_rc()
        elif("new_process"==data.decode('utf-8').split()[0]):
            process_network.update({int(data.decode('utf-8').split()[1])})
        elif("msg" == data.decode('utf-8').split('(')[0]):
            messages_queue.append(data.decode('utf-8'))
            print(msg_queue() + str(messages_queue)) #print de mensagem recebida, recebe dele mesmo e do outro processo
        elif("ack" == data.decode("utf-8").split('(')[0]):
            ack_queue.append(data.decode('utf-8'))
            # print("\nacks")
            # print(ack_queue)
        else:
            # print('@@AAASOCORRO@@@')
            print(data.decode("utf-8").split('(')[0])
            print(msg_queue(relative_time, id) + str(messages_queue))

def send_m():
    s.sendto("connect".encode('utf-8'), n_address)
    while True:
        s.sendto(input("").encode('utf-8'), n_address)

def use_rc():
    print("\nPROCESSANDO EM ANDAMENTO\n")
    time.sleep(5)
    print("\nProcesso Terminado, enviando liberação.\n")
    s.sendto(("liberar").encode('utf-8'), n_address)

def send_to_all_processes(message):
    global relative_time
    relative_time += 1
    for process in process_network:
        s.sendto(('msg(' + message + '-' + str(relative_time) + '-' + str(id)).encode('utf-8'), ('localhost', process))

def send_ack_to_all_processes():
    global relative_time
    # print("Qtd menssagens: " + str(len(messages_queue)))
    for message in messages_queue:
        message_splitted = message.split('-')
        if (int(message_splitted[1] + message_splitted[2]) <= int((str(relative_time) + str(id)))): #compara tr.id do processo com da mensagem
            for process in process_network: #nao manda pra si
                if(process != port):
                    s.sendto(('ack(' + message).encode('utf-8'), ('localhost', process))


def check_if_can_execute():
    global score
    global relative_time
    # print("Comparando msgs e acks para executar")
    if(len(messages_queue) > 0 and len(ack_queue) > 0):
        if messages_queue[0].split('msg(')[1] == ack_queue[0].split('msg(')[1]:
            # print("Pode executar")
            # print(messages_queue[0].split('msg(')[1].split('-')[0])
            if("D100" == messages_queue[0].split('msg(')[1].split('-')[0]):
                print('\nDepósito + 100')
                # print(score)
                score += 100
            else:
                print('\nJuro + 1%')
                # print(score)
                score *= 1.01
            print('\nSaldo atual: ', score)
            relative_time += 1
            messages_queue.pop(0)
            ack_queue.pop(0)

def msg_queue():
    global relative_time, id
    return 'P' + str(id) + ' TR' + str(relative_time) + ' '

host = 'localhost'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, 0))

_, port = s.getsockname()

os.system('clear')

# print('\nPorta deste processo inicializado em:', port)
process_network = {port}

n_address = ('localhost', 4000)

if (int(sys.argv[1]) == 1):
    id = 1
    operation = 'D100'
else:
    id = 2
    operation = 'J1'

print("\nPROCESS START")

print(msg_queue())

t1 = threading.Thread(target=send_m)
t2 = threading.Thread(target=receive_m)

t1.start()
t2.start()

time.sleep(3)

send_to_all_processes(operation)

time.sleep(3)

print("\nEnviando acks")

send_ack_to_all_processes()

time.sleep(2)

check_if_can_execute()

time.sleep(2)

send_ack_to_all_processes()
print(msg_queue(), messages_queue)
print(msg_queue(), ack_queue)

time.sleep(2)

check_if_can_execute()
print(msg_queue(), messages_queue)
print(msg_queue(), ack_queue)

print('\nSaldo final: ', score)
# print(msg_queue(), messages_queue)
# print(msg_queue(), ack_queue)