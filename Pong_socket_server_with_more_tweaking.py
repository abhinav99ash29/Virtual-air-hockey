import pygame
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


paddle_left_y = 0
paddle_right_y = 0

##
# Socket Params
# 
## Server IP
HOST = '192.168.43.98'
PORT = 4000
CHUNK=1024

x_thresh = 20
y_thresh = 50


##
# Receive utility function
#
def rec():
    a = []
    while True:
        d = client.recv(1)
        d = d.decode('utf-8')
        
        if d == '@':
            break
        else:
            a.append(d)
    
    a = int(float(str(''.join(a))))
    
    return a       

##
# Receiving Data over socket
#
def receive():
    
    global paddle_left_y
    global paddle_right_y
    PADDLE_HEIGHT = 100
    HEIGHT = 720

    while True:
#         try:
        data = (client.recv(CHUNK)).decode('utf-8')
        if data=='left':
            client.send('s'.encode())
            paddle_left_y = rec()
            
            if paddle_left_y < y_thresh:
                paddle_left_y = y_thresh/2
            if paddle_left_y > (HEIGHT - PADDLE_HEIGHT - y_thresh):
                paddle_left_y = HEIGHT - PADDLE_HEIGHT - y_thresh/2-5    
            
    
        elif data == 'right':
            client.send('s'.encode())
            paddle_right_y = rec()    
            
            if paddle_right_y < y_thresh:
                paddle_right_y = y_thresh/2
            if paddle_right_y > (HEIGHT - PADDLE_HEIGHT - y_thresh):
                paddle_right_y = HEIGHT - PADDLE_HEIGHT - y_thresh/2-5    
                    
#         except:
#             print('Connection Failure !')
#             break    



def game():

    global paddle_left_y
    global paddle_right_y
    
        ##
    # Game mode
    #

    pygame.init()
    WIDTH = 1366
    HEIGHT = 720
    SCREEN_SIZE = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen = pygame.display.set_mode(SCREEN_SIZE , pygame.RESIZABLE)
    
     
    class Background(pygame.sprite.Sprite):
        def __init__(self, image_file, location):
            pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
            self.image = pygame.image.load(image_file)
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = location
            
    BackGround = Background('background.png', [0,0])      
        
    pygame.display.set_caption('Air-Hockey')
    clock = pygame.time.Clock()
    pygame.key.set_repeat(50, 50)
    pygame.init()
    FSC = False
    x_thresh = 20
    y_thresh = 28
    
    
    
    ##
    # Game consts
    #
    FONT = pygame.font.Font(None, 120)
    FONT1 = pygame.font.Font(None, 30)
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0 ,0, 255)
    light_blue = (0,100,200)
    GRAY  = (100, 100, 100)
    MODE_PLAY = 1
    MODE_QUIT = 0
    Game = 'stop'
    FRAME_RATE = 120
    
    ##
    # Game Vars
    #
    PLAY_AREA_COLOR = (120,50,120)
    PLAY_AREA_WIDTH = 50
    PLAY_AREA_LEFT_X = 0
    PLAY_AREA_RIGHT_X = WIDTH - PLAY_AREA_WIDTH
    PLAY_AREA_LEFT_Y = 0
    PLAY_AREA_RIGHT_Y = 0
    PLAY_AREA_HEIGHT = HEIGHT
    score_left = 0
    score_right = 0
    current_mode = MODE_PLAY
    BALL_SPEED = 25
    pos_x = int(0.5 * WIDTH)   
    speed_x = BALL_SPEED
    pos_y = int(0.5 * HEIGHT)
    speed_y = BALL_SPEED
    BALL_COLOR = WHITE
    BALL_RADIUS = 18
    PADDLE_SPEED = 10
    PADDLE_HEIGHT = 80
    PADDLE_WIDTH = 25
    PADDLE_LEFT_COLOR = WHITE
    PADDLE_RIGHT_COLOR = WHITE
    PADDLE_LEFT_X = int(0.5*PADDLE_WIDTH) + x_thresh
    PADDLE_RIGHT_X = WIDTH - int(0.5*PADDLE_WIDTH) - PADDLE_WIDTH - x_thresh
    paddle_left_y = int(0.5 * HEIGHT - 0.5 * PADDLE_HEIGHT)
    paddle_right_y = paddle_left_y
    
    
    ##
    # Game loop
    #
    while current_mode == MODE_PLAY:
        ##
        # Handle keyboard
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                current_mode = MODE_QUIT
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_mode = MODE_QUIT
    
        keysPressed = pygame.key.get_pressed()
        if keysPressed[pygame.K_UP]:
            paddle_right_y = paddle_right_y - PADDLE_SPEED
            if paddle_right_y < y_thresh:
                paddle_right_y = y_thresh
        elif keysPressed[pygame.K_DOWN]:
            paddle_right_y = paddle_right_y + PADDLE_SPEED
            if paddle_right_y > (HEIGHT - PADDLE_HEIGHT - y_thresh):
                paddle_right_y = HEIGHT - PADDLE_HEIGHT - y_thresh/2-19
        if keysPressed[pygame.K_a]:
            paddle_left_y = paddle_left_y - PADDLE_SPEED
            if paddle_left_y < y_thresh:
                paddle_left_y = y_thresh
        elif keysPressed[pygame.K_z]:
            paddle_left_y = paddle_left_y + PADDLE_SPEED
            if paddle_left_y > (HEIGHT - PADDLE_HEIGHT - y_thresh):
                paddle_left_y = HEIGHT - PADDLE_HEIGHT - y_thresh/2-19
        elif keysPressed[pygame.K_F11]:
            if(FSC):
                screen = pygame.display.set_mode(SCREEN_SIZE , pygame.RESIZABLE)
                FSC=False
            else:
                screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
                FSC=True
        elif keysPressed[pygame.K_F1]:
            if(Game!='over'):
                Game='start'
                score_left = 0
                score_right = 0
        elif keysPressed[pygame.K_F2]:
            Game='stop'
            score_left = 0
            score_right = 0    
            
                
            
    
        ##
        # Draw arena and score
        #
    #     screen.fill(BLACK)
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
    #     pygame.draw.line(screen, GRAY, [int(0.5 * WIDTH), 0], [int(0.5 * WIDTH), HEIGHT], 1)
        text = FONT.render("%2s  %2s" % (str(score_left), str(score_right)), 5, light_blue)
        textpos = text.get_rect(center = (WIDTH/2 - 10, 60))
        screen.blit(text, textpos)
        text1 = FONT1.render("F1 : Play", 2, (0,120,120))
        textpos1 = text.get_rect(center=(WIDTH/2 - 400, 100))
        screen.blit(text1, textpos1)
        text1 = FONT1.render("F2 : Restart", 2, (0,120,120))
        textpos1 = text.get_rect(center=(WIDTH/2 - 400, 150))
        screen.blit(text1, textpos1)
        text1 = FONT1.render("F11 : FullScreen", 2, (0,120,120))
        textpos1 = text.get_rect(center=(WIDTH/2 - 400, 200))
        screen.blit(text1, textpos1)
        text1 = FONT1.render("Esc : Exit", 2, (0,120,120))
        textpos1 = text.get_rect(center=(WIDTH/2 - 400, 250))
        screen.blit(text1, textpos1)
    
        ##
        # Draw paddles
        #
        pygame.draw.rect(screen, PADDLE_LEFT_COLOR, (PADDLE_LEFT_X, paddle_left_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, PADDLE_RIGHT_COLOR, (PADDLE_RIGHT_X, paddle_right_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
        ##
        # Draw play area
        #
    #     pygame.draw.rect(screen, PLAY_AREA_COLOR, (PLAY_AREA_LEFT_X, PLAY_AREA_LEFT_Y, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT))
    #     pygame.draw.rect(screen, PLAY_AREA_COLOR, (PLAY_AREA_RIGHT_X, PLAY_AREA_RIGHT_Y, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT))
        
    
        ##
        # Move ball and update scores
        #
    
        if(score_right==100 or score_left==100):
            Game='over'
    
    
        if(Game=='over'):
            FONT2 = pygame.font.Font(None, 80)
            text2 = FONT2.render("Game Over", 2, (200,0,0))
            textpos2 = text.get_rect(centerx=WIDTH/2-88,centery=HEIGHT/2)
            screen.blit(text2, textpos2)
            FONT2 = pygame.font.Font(None, 50)
            a=0
            if(score_right>score_left):
                a=1
            if(a==1):
                text2 = FONT2.render("You Lose                    You Win", 2, (200,0,0))
                textpos2 = text.get_rect(centerx=WIDTH/2-140, centery=HEIGHT/2+120)
                screen.blit(text2, textpos2)
            if(a==0):
                text2 = FONT2.render("You Win                    You Lose", 2, (200,0,0))
                textpos2 = text.get_rect(centerx=WIDTH/2-140, centery=HEIGHT/2+120)
                screen.blit(text2, textpos2)    
                
            
        else: 
            if(Game=='start'):
                r = BALL_RADIUS
                pos_x = pos_x + speed_x
                
                if pos_x > WIDTH - x_thresh - 13:
                    if pos_y >= 120 and pos_y<=600:
                        if pos_y > (0.5 * HEIGHT):
                            speed_y = abs(speed_y)
                        else:
                            speed_y = -abs(speed_y)
                        pos_x = int(0.5 * WIDTH)
                        pos_y = int(0.5 * HEIGHT)
                        score_left += 1
                    else:    
                        pos_x = WIDTH - x_thresh - r - 20
                        speed_x = -speed_x
                        
                        
                elif pos_x < x_thresh+20:
                    if pos_y >= 120 and pos_y <= 600:
                        if pos_y > (0.5 * HEIGHT):
                            speed_y = abs(speed_y)
                        else:
                            speed_y = -abs(speed_y)
                        pos_x = int(0.5 * WIDTH)
                        pos_y = int(0.5 * HEIGHT)
                        score_right += 1
                    else:    
                        pos_x = x_thresh+20
                        speed_x = abs(speed_x)
                        
                pos_y = pos_y + speed_y
                
                if pos_y + r > HEIGHT - y_thresh:
                    speed_y = -speed_y
                elif pos_y - r < y_thresh:
                    speed_y = abs(speed_y)
                    
                
                if pos_x <= (PADDLE_LEFT_X + PADDLE_WIDTH)+r and pos_y >= paddle_left_y and pos_y <= (paddle_left_y + PADDLE_HEIGHT):
                    pos_x = PADDLE_LEFT_X + PADDLE_WIDTH + r
                    speed_x = abs(speed_x)
                elif pos_x >= PADDLE_RIGHT_X-r and pos_y >= paddle_right_y and pos_y <= (paddle_right_y + PADDLE_HEIGHT):
                    pos_x = PADDLE_RIGHT_X-r
                    speed_x = -speed_x    
    
            if(Game=='stop'):
                paddle_left_y = int(0.5 * HEIGHT - 0.5 * PADDLE_HEIGHT)
                paddle_right_y = paddle_left_y
                pos_x = int(0.5 * WIDTH)
                pos_y = int(0.5 * HEIGHT)
                
            pygame.draw.circle(screen, BALL_COLOR, [pos_x, pos_y], BALL_RADIUS)
    
            ##
            # Bounce ball off paddles
            #
    
    
        ##
        # Tick-tock
        #
        pygame.display.update()
        clock.tick(FRAME_RATE)
    
    pygame.quit()


##
# Creating Server Object to connect with the Detector
#
server = socket(family=AF_INET, type=SOCK_STREAM)
try:
    server.bind((HOST, PORT))
except OSError:
    print("Server Busy")

server.listen()
print("Waiting for Detector...")


client, addr = server.accept()

print('Detector Connected !')

print('Starting detector data Reception...')

t2 = Thread(target = receive)
t2.start()

print('Data Reception Started !')


print('Starting the Game...')
##
# Starting Game loop
#
t1 = Thread(target = game)
t1.start()
print('Game Started !')


