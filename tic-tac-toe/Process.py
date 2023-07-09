import socket
import threading
import sys
import os

# movement = []

def receive_m():
    while True:
        data, addr = s.recvfrom(1024)
        global n_address
        n_address = addr
        if("aceito" == data.decode('utf-8')):
            os.system('clear')
            movement = input("\nDigite a posição para jogar entre 1 á 9:")
            # while():
                # print("loop")
                # if(True):
                #if se nao for uma posicao valida joga de novo
                    #print("\nPosição não é válida, tente jogar em outra posição.")
                    # break
            # print("\nsaiu")
            # movement = input('')
            # print(type(movement))
            # print('liberar-' + movement)
            s.sendto(('liberar-' + movement + '-' + str(id)).encode('utf-8'), n_address)
            print("\njogada registrada")
            # print("\nTabuleiro")
        elif("esperar" == data.decode('utf-8')):
            print("\nAguarde sua vez de jogar!")
        elif("fim" == data.decode('utf-8').split('-')[0]):
            print("\nFIM DE JOGO:")
            if(port == int(data.decode('utf-8').split('-')[1])):
                print("Você VENCEU! :D")
            else:
                print("Você PERDEU! :(")
        elif("jajogou" == data.decode('utf-8')):
            print("\nVocê já jogou! Aguarde o outro jogador para continuar.")

def send_m():
    while True:
        action = input("")
        if(action == "j"):
            s.sendto('j'.encode('utf-8'), n_address)
        # else:
            # print("?")

host = 'localhost' 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, 0))

_, port = s.getsockname()
print('Porta deste processo:', port)

n_address = (('localhost', 4000))

if (int(sys.argv[1]) == 1):
    id = 1
else:
    id = 2

print("\n", id)

print("Par inicializado.")

t1 = threading.Thread(target=send_m)
t2 = threading.Thread(target=receive_m)

t1.start()
t2.start()

t1.join()
t2.join()