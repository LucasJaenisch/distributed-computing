import socket
import threading
import sys
import os

#Set if the critical region is in use or not
global in_use
global win

in_use = False
win = False

table = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
queue = ['START']


def receive_m():
    while True:
        data, addr = s.recvfrom(1024)
        global n_address, in_use, win
        # print("\n", in_use)
        n_address = addr
        # print(data.decode('utf-8'), " recebido de: ", addr)

        if(not in_use):
            #bloquear se for o que acabou de jogar
            if(queue[-1] == addr[1]):
                s.sendto(("jajogou").encode('utf-8'), n_address)
            else:
                os.system('clear')
                if("j" == data.decode('utf-8') or "J" == data.decode('utf-8')):
                    print("\nExecutando jogada1...")
                    in_use = True
                    s.sendto(("aceito").encode('utf-8'), n_address)
                elif(len(queue) > 0):
                    print("\nExecutando jogada2...", queue[0])
                    s.sendto(("aceito").encode('utf-8'), ('localhost', queue[0]))
                    queue.pop(0)
                queue.append(addr[1])
        elif("liberar" == data.decode('utf-8').split('-')[0]):
            os.system('clear')
            in_use = False
            print("Jogada realizada na posição: ", data.decode('utf-8').split('-')[1])
            # print(data.decode('utf-8').split('-')[1])
            # print("\n@@@@@@@@", data.decode('utf-8').split('-')[2])
            if '1' == data.decode('utf-8').split('-')[2]:
                table[int(data.decode('utf-8').split('-')[1])-1] = 'X'
            else:
                table[int(data.decode('utf-8').split('-')[1])-1] = 'O'

            #VERIFICA VITORIA
            if table[0] == table[1] == table[2] and table[0] != ' ' or table[3] == table[4] == table[5] and table[3] != ' ' or table[6] == table[7] == table[8] and table[6] != ' ':
                win = True
            if table[0] == table[3] == table[6] and table[3] != ' ' or table[1] == table[4] == table[7] and table[1] != ' ' or table[2] == table[5] == table[8] and table[2] != ' ':
                win = True
            if table[0] == table[4] == table[8] and table[0] != ' ' or table[2] == table[4] == table[6] and table[2] != ' ':
                win = True

            if win == True:
                print("\nFIM DE JOGO MANDANDO PARA TODOS OS PROCESSOS")
                # s.sendto(("fim-"+addr[1]).encode('utf-8'), n_address)
                # print(("fim" + addr[1]).encode('utf-8'))
                s.sendto(("fim-" + str(addr[1])).encode('utf-8'), ('localhost', queue[1]))
                s.sendto(("fim-" + str(addr[1])).encode('utf-8'), ('localhost', queue[2]))
                

            # print("\nTabuleiro atualizado")
            draw_table()
            
            print("Ordem de jogadas: ", queue)

        else:
            s.sendto("esperar".encode('utf-8'), n_address)

def draw_table():
    print('\n'.join(map(" ".join, zip(*[iter(table)] * 3))))

host = 'localhost' 
port = 4000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

n_address = (('localhost', 4001))

print("Cordenador Inicializado.")
draw_table()

process_in_line = []

# t1 = threading.Thread(target=send_m)
t2 = threading.Thread(target=receive_m)

# t1.start()
t2.start()

# t1.join()
# t2.join()