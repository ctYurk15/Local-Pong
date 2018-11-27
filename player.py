from socket import socket, gethostname
from threading import Thread
from pygame import *

#classes and methods
class Sprite:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap=image.load(filename)
    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

info = ''   #information from server
#loop of getting info from server
def get_info():
    while True:
        info= s.recv(1024).decode()
        print(info)
        if info != '':
            if info == '1UP':
                platform1.y -= 1
            elif info == '1DOWN':
                platform1.y += 1
            elif info == '2UP':
                platform2.y -= 1
            elif info == '2DOWN':
                platform2.y += 1

 
#sending info to server
def send_info(info, numb):
    msg = numb + info
    msg = bytes(msg, 'utf-8')
    s.send(msg)

#window
win = display.set_mode((800, 400))
display.set_caption(('Pong'))
screen = Surface((800, 400))

#objects
platform1 = Sprite(40, 140, 'platform1.png')
platform2 = Sprite(720, 140, 'platform2.png')

#connection
s = socket()
host = gethostname()
port = 9090
s.connect((host, port))

#getting a number
number = s.recv(1024).decode()
print(number)

#thread of getting info
Thread(None, get_info).start()

#game cycle
play = True
while play:
    time.delay(5)

    #events
    for e in event.get():
        if e == QUIT:
            play = False
            
     #keep track wich key pressed
    key_press = key.get_pressed()
    if number == '1':
        if key_press[K_UP] and platform1.y > 0:
            send_info('UP', number)
            platform1.y -= 1
        elif key_press[K_DOWN] and platform1.y < 260:
            send_info('DOWN', number)
            platform1.y += 1
    if number == '2':
        if key_press[K_UP] and platform2.y > 0:
            send_info('UP', number)
            platform2.y -= 1
        elif key_press[K_DOWN] and platform2.y < 260:
            send_info('DOWN', number)
            platform2.y += 1
            

     #render
    screen.fill((0, 89, 56))
    platform1.render()
    platform2.render()
    win.blit(screen, (0, 0))
    display.flip()

s.close()
