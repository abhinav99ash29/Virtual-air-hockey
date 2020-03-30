from utils import detector_utils as detector_utils
import cv2
import tensorflow as tf
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM

##
# Server IP
#
HOST = '192.168.157.233'#'192.168.157.233'
PORT = 4000
CHUNK = 1024


def map_val(top, bottom):
##
# Mapping parameters
#
    present_ht = int((top+bottom)/2)
    ht = 480
    HEIGHT = 720
    map_min = 30
    map_max = 450
    if present_ht < 20:
        return int(1)
    elif present_ht>450:
        return int(720)
    else:
        return int((present_ht*(HEIGHT))/(map_max-map_min))

    
    
    



def send_paddle_coordinates(side,y):
    y = str(y).encode()
    client.send(side.encode())
    data = (client.recv(CHUNK)).decode('utf-8')
    if data == 's':
        client.send(y)
        client.send('@'.encode())
        
    
    

def detector():

    ##
    # Game params
    #
    
    HEIGHT = 720
    paddle_left_y = 360
    paddle_right_y = 360
    PADDLE_HEIGHT = 150
        
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

    
    wd = 640
    ht = 480
    
    cv2.namedWindow('Left Hand', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Right Hand', cv2.WINDOW_NORMAL)
    while True:
#         try:
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
        detector_utils.draw_box_on_image(num_hands_detect, score_thresh,
                                         scoresl, boxesl, w, h,
                                         image_l)
        boxesr, scoresr = detector_utils.detect_objects(image_r,
                                                      detection_graph, sess)
        detector_utils.draw_box_on_image(num_hands_detect, score_thresh,
                                         scoresr, boxesr, w, h,
                                         image_r)
        cv2.imshow('Left Hand',
        cv2.cvtColor(image_l, cv2.COLOR_RGB2BGR))
        cv2.imshow('Right Hand',
        cv2.cvtColor(image_r, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(25) & 0xFF == 27:
            cv2.destroyAllWindows()
            client.close()
            break
        for i in range(num_hands_detect):
            if (scoresl[i] > score_thresh):
                (left, right, top,bottom) = (boxesl[i][1] * w, boxesl[i][3] * w,
                                              boxesl[i][0] * h, boxesl[i][2] * h)
                
                #paddle_left_y = int(((top+bottom)/2)* (HEIGHT/ht))

                paddle_left_y = map_val(top,bottom)
                
                if paddle_left_y < 0:
                    paddle_left_y = 0

                if paddle_left_y > (HEIGHT - PADDLE_HEIGHT/2):
                    paddle_left_y = HEIGHT - PADDLE_HEIGHT/2   
                try:    
                    print('Sending Left paddle coordinates...')
                    send_paddle_coordinates('left', paddle_left_y)  
                    print('Sent !')   
                except:
                    pass    
                    
##                print(int((top+bottom)/2 * (HEIGHT/ht)))
                
            if (scoresr[i] > score_thresh):
                (left, right, top,bottom) = (boxesr[i][1] * w, boxesr[i][3] * w,
                                              boxesr[i][0] * h, boxesr[i][2] * h)
                
                #paddle_right_y = int(((top+bottom)/2)* (HEIGHT/ht))

                paddle_right_y = map_val(top,bottom)
                
                if paddle_right_y > (HEIGHT - PADDLE_HEIGHT/2):
                    paddle_right_y = HEIGHT - PADDLE_HEIGHT/2
                if paddle_right_y < 0:
                    paddle_right_y = 0; 
                try:    
                    print('Sending Rigth paddle coordinates...')
                    send_paddle_coordinates('right', paddle_right_y)  
                    print('Sent !')              
                except:    
                    pass
##                print(int((top+bottom)/2 * (HEIGHT/ht)))
               
#         except:
#             print('Connection Failure !')
#             break            

# Creating client object to send data to the game

client = socket(family=AF_INET, type=SOCK_STREAM)

try:
    print('Connecting to Game...')
    client.connect((HOST, PORT))
    print('Game Connected !')
    print('Starting the Detector...')
    t1 = Thread(target = detector)
    t1.start()
    print('Detector Started !')
except:
    print('Connection Failure !')




