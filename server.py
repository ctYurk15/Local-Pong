from socket import socket, gethostname
from threading import Thread

#players list
players = []

#sending information to players
def send_info(information):
    global players
    if information[0] == '1':
        information = bytes(information, 'utf-8')
        players[1].send(information)
    elif information[0] == '2':
        information = bytes(information, 'utf-8')
        players[0].send(information)
    

#acccept connection and works with them
def connected_player(player_socket, addr):
    print('New connection from {}'.format(addr))
    if len(players) == 0:
        send_number('1', player_socket)
    elif len(players) == 1:
       send_number('2', player_socket)
    players.append(player_socket)
    while True:
        info = player_socket.recv(1024).decode()
        print(info)
        send_info(info)
    player_socket.close()

#sending a number
def send_number(number, player):
    number = bytes(number, 'utf-8')
    player.send(number)

    

#starting a server
s = socket()
host = gethostname()
port = 9090
s.bind((host, port))
s.listen(2)
print('Server Started succesfully...')

#server loop
while True:
    c, addr = s.accept()
    Thread(None, connected_player, args=(c, addr)).start()

s.close()
