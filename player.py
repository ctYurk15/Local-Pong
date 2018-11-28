from socket import socket, gethostname
from threading import Thread
from pygame import *

#goals
goals = [0, 0]

#classes and methods
class Sprite:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap=image.load(filename)
    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

#collision
def collision(x1,y1,w1,h1,x2,y2,w2,h2):
    if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2):
        return True
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2):
        return True 
    elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2):
        return True 
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2):
        return True 
    else:
        return False

#loop of getting info from server
def get_info():
    while True:
        info= s.recv(1024).decode()
        if info != '':
            global ball_speed
            ball_speed = 1
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
    global ball_speed
    ball_speed = 1
    msg = numb + info
    msg = bytes(msg, 'utf-8')
    s.send(msg)

#getting a goal
def gave_a_goal(numb):
    global goals
    goals[numb] += 1
    print(goals[0], ':', goals[1])
    time.delay(1000)
    platform1.x = 40
    platform1.y = 140
    platform2.x = 720
    platform2.y = 140
    ball.x = 360
    ball.y = 160

#window
win = display.set_mode((800, 400))
display.set_caption(('Pong'))
screen = Surface((800, 400))

#objects
platform1 = Sprite(40, 140, 'platform1.png')
platform2 = Sprite(720, 140, 'platform2.png')
ball = Sprite(360, 160, 'ball.png')
ball_speed = 0
ball.right = True
ball.down = True

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

    #ball
    #up-down
    if ball.down == True:
        if ball.y < 360:
            ball.y += ball_speed
        else:
            ball.down = False
    else:
        if ball.y > 0:
            ball.y -= ball_speed
        else:
            ball.down = True
    #left-right
    if ball.right == True:
        if ball.x < 760:
            ball.x += ball_speed
        else:
            gave_a_goal(0)
    else:
        if ball.x > 0:
            ball.x -= ball_speed
        else:
            gave_a_goal(1)
    #collisions
    if collision(ball.x, ball.y, 40, 40, platform2.x, platform2.y, 40, 140) == True:
        ball.right = False
    if collision(ball.x, ball.y, 40, 40, platform1.x, platform1.y, 40, 140) == True:
        ball.right = True
        
            

     #render
    screen.fill((0, 89, 56))
    platform1.render()
    platform2.render()
    ball.render()
    win.blit(screen, (0, 0))
    display.flip()

i = input()
s.close()
