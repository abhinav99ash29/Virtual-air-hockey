#License MIT 2016 Ahmad Retha

import pygame
import cv2
import tensorflow as tf
from utils import detector_utils as detector_utils
from threading import Thread

##
# Global vars for y positions of paddles

HEIGHT = 720
paddle_left_y = 0
paddle_right_y = 0
PADDLE_HEIGHT = 0







def detector():

    global paddle_left_y
    global paddle_right_y
    global HEIGHT
    global PADDLE_HEIGHT

    ##
    # Hand detector setup
    #
    score_thresh = 0.7
    fps = 10
    video_source = 0
    width = 640
    height = 480
    display = 1

    cap = cv2.VideoCapture(video_source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    im_width, im_height = (cap.get(3), cap.get(4))

    detection_graph, sess = detector_utils.load_inference_graph()

    # max number of hands we want to detect/track
    num_hands_detect = 2

    
    wd = 50
    ht = 50
    
##    cv2.namedWindow('Left Hand', cv2.WINDOW_NORMAL)
##    cv2.namedWindow('Right Hand', cv2.WINDOW_NORMAL)
    while True:
        ret, image_np = cap.read()
        image_np = cv2.resize(image_np, (wd,ht))
        image_np = cv2.flip(image_np, 1)
        try:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        except:
            print("Error converting to RGB")
     

        
        width_cutoff = int(wd/2)
        image_l = image_np[:, :width_cutoff]
        image_r = image_np[:, width_cutoff:]

        w,h = int(wd/2),ht

        boxesl, scoresl = detector_utils.detect_objects(image_l,
                                                      detection_graph, sess)
##        detector_utils.draw_box_on_image(num_hands_detect, score_thresh,
##                                         scoresl, boxesl, w, h,
##                                         image_l)
        boxesr, scoresr = detector_utils.detect_objects(image_r,
                                                      detection_graph, sess)
##        detector_utils.draw_box_on_image(num_hands_detect, score_thresh,
##                                         scoresr, boxesr, w, h,
##                                         image_r)
##        cv2.imshow('Left Hand',
##        cv2.cvtColor(image_l, cv2.COLOR_RGB2BGR))
##        cv2.imshow('Right Hand',
##        cv2.cvtColor(image_r, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(25) & 0xFF == 27:
            cv2.destroyAllWindows()
            break
        for i in range(num_hands_detect):
            if (scoresl[i] > score_thresh):
                (left, right, top,bottom) = (boxesl[i][1] * w, boxesl[i][3] * w,
                                              boxesl[i][0] * h, boxesl[i][2] * h)
                
                paddle_left_y = int(((top+bottom)/2)* (HEIGHT/ht))
                
                if paddle_left_y < 0:
                    paddle_left_y = 0

                if paddle_left_y > (HEIGHT - PADDLE_HEIGHT/2):
                    paddle_left_y = HEIGHT - PADDLE_HEIGHT/2    
                    
##                print(int((top+bottom)/2 * (HEIGHT/ht)))
                
            if (scoresr[i] > score_thresh):
                (left, right, top,bottom) = (boxesr[i][1] * w, boxesr[i][3] * w,
                                              boxesr[i][0] * h, boxesr[i][2] * h)
                
                paddle_right_y = int(((top+bottom)/2)* (HEIGHT/ht))
                if paddle_right_y > (HEIGHT - PADDLE_HEIGHT/2):
                    paddle_right_y = HEIGHT - PADDLE_HEIGHT/2
                if paddle_right_y < 0:
                    paddle_right_y = 0;    
##                print(int((top+bottom)/2 * (HEIGHT/ht)))



def game():

    global paddle_left_y
    global paddle_right_y
    global HEIGHT
    global PADDLE_HEIGHT
        ##
    # Game mode
    #

    WIDTH = 1366
    
    SCREEN_SIZE = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen = pygame.display.set_mode(SCREEN_SIZE , pygame.RESIZABLE)
    pygame.display.set_caption('Pong')
    clock = pygame.time.Clock()
    pygame.key.set_repeat(50, 50)
    pygame.init()
    FSC = False

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
    GRAY  = (100, 100, 100)
    MODE_PLAY = 1
    MODE_QUIT = 0
    Game = 'stop'
    FRAME_RATE = 500 ## Change the frame rate
    GAME_OVER = 1000

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
    BALL_SPEED = 3
    pos_x = int(0.5 * WIDTH) 
    speed_x = BALL_SPEED
    pos_y = int(0.5 * HEIGHT)
    speed_y = BALL_SPEED
    BALL_COLOR = WHITE
    BALL_RADIUS = 18
    PADDLE_SPEED = 3
    PADDLE_HEIGHT = 150
    PADDLE_WIDTH = 20
    PADDLE_LEFT_COLOR = WHITE
    PADDLE_RIGHT_COLOR = WHITE
    PADDLE_LEFT_X = int(0.5*PADDLE_WIDTH) + PLAY_AREA_WIDTH
    PADDLE_RIGHT_X = WIDTH - int(0.5*PADDLE_WIDTH) - PADDLE_WIDTH - PLAY_AREA_WIDTH
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
            if paddle_right_y < 0:
                paddle_right_y = 0;
        elif keysPressed[pygame.K_DOWN]:
            paddle_right_y = paddle_right_y + PADDLE_SPEED
            if paddle_right_y > (HEIGHT - PADDLE_HEIGHT):
                paddle_right_y = HEIGHT - PADDLE_HEIGHT
        if keysPressed[pygame.K_a]:
            paddle_left_y = paddle_left_y - PADDLE_SPEED
            if paddle_left_y < 0:
                paddle_left_y = 0
        elif keysPressed[pygame.K_z]:
            paddle_left_y = paddle_left_y + PADDLE_SPEED
            if paddle_left_y > (HEIGHT - PADDLE_HEIGHT):
                paddle_left_y = HEIGHT - PADDLE_HEIGHT
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
        # Image frame acquisition
        #
        
         
            

        ##
        # Draw arena and score
        #
        screen.fill(BLACK)
        pygame.draw.line(screen, GRAY, [int(0.5 * WIDTH), 0], [int(0.5 * WIDTH), HEIGHT], 1)
        text = FONT.render("%2s:%2s" % (str(score_left), str(score_right)), 5, GRAY)
        textpos = text.get_rect(centerx=WIDTH/2)
        screen.blit(text, textpos)
        text1 = FONT1.render("F1 : Play", 2, (0,100,100))
        textpos1 = text.get_rect(center=(WIDTH/2 - 400, 100))
        screen.blit(text1, textpos1)
        text1 = FONT1.render("F2 : Restart", 2, (0,100,100))
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
        pygame.draw.rect(screen, PLAY_AREA_COLOR, (PLAY_AREA_LEFT_X, PLAY_AREA_LEFT_Y, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT))
        pygame.draw.rect(screen, PLAY_AREA_COLOR, (PLAY_AREA_RIGHT_X, PLAY_AREA_RIGHT_Y, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT))
        

        ##
        # Move ball and update scores
        #

        if(score_right==GAME_OVER or score_left==GAME_OVER):
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
                pos_x = pos_x + speed_x
                if pos_x > WIDTH - PLAY_AREA_WIDTH:
                    if pos_y > (0.5 * HEIGHT):
                        speed_y = abs(speed_y)
                    else:
                        speed_y = -abs(speed_y)
                    pos_x = int(0.5 * WIDTH)
                    pos_y = int(0.5 * HEIGHT)
                    score_left += 1
                elif pos_x < PLAY_AREA_WIDTH:
                    if pos_y > (0.5 * HEIGHT):
                        speed_y = abs(speed_y)
                    else:
                        speed_y = -abs(speed_y)
                    pos_x = int(0.5 * WIDTH)
                    pos_y = int(0.5 * HEIGHT)
                    score_right += 1
                pos_y = pos_y + speed_y
                if pos_y > HEIGHT:
                    speed_y = -speed_y
                elif pos_y < 0:
                    speed_y = abs(speed_y)

            if(Game=='stop'):
                paddle_left_y = int(0.5 * HEIGHT - 0.5 * PADDLE_HEIGHT)
                paddle_right_y = paddle_left_y
                pos_x = int(0.5 * WIDTH)
                pos_y = int(0.5 * HEIGHT)
                
            pygame.draw.circle(screen, BALL_COLOR, [pos_x, pos_y], BALL_RADIUS)

            ##
            # Bounce ball off paddles
            #
            r = BALL_RADIUS
            if pos_x <= (PADDLE_LEFT_X + PADDLE_WIDTH)+r and pos_y >= paddle_left_y and pos_y <= (paddle_left_y + PADDLE_HEIGHT):
                pos_x = PADDLE_LEFT_X + PADDLE_WIDTH + r
                speed_x = abs(speed_x)
            elif pos_x >= PADDLE_RIGHT_X-r and pos_y >= paddle_right_y and pos_y <= (paddle_right_y + PADDLE_HEIGHT):
                pos_x = PADDLE_RIGHT_X-r
                speed_x = -speed_x

        ##
        # Tick-tock
        #
        pygame.display.update()
        clock.tick(FRAME_RATE)

    pygame.quit()



##
# Starting Game loop
#
t2 = Thread(target = game)
t2.start()

##
# Starting hand detection
#
t1 = Thread(target = detector)
t1.start()


    
