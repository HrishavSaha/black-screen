#Import Statements
import cv2
import numpy as np
import keyboard

#Initialising Camera Object
VC = cv2.VideoCapture(0)

#Reading background image and resizing it
bg = cv2.imread('bg.jpg')
bg = cv2.resize(bg, (1280, 720))

#Main Loop
while True:
    #Capturing and Reading each frame
    ret, frame = VC.read()
    #Flipping the frame on the vertical axis
    frame = np.flip(frame, 1)
    #Converting the frame's colorspace from BGR to HSV
    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #Initialising colour bounds for masking
    lblack = np.array([30,30,0])
    ublack = np.array([104,153,70])
    #Initialising the mask 
    #(using frame_hsv results in choppy masking, but it's good at NOT masking black foreground elements)
    #(using frame results in smooth masking, but it also masks black foreground elements almost entirely. Hence, its code block is commented)
    mask = cv2.inRange(frame_hsv,lblack,ublack)
    #mask = cv2.inRange(frame,lblack,ublack)
    #Creating the mask
    res = cv2.bitwise_and(frame,frame,mask=mask)
    #Subtracting the mask from the frame, providing us with the masked frame
    masked_frame = frame - res
    #Finally creating the processed frame by replacing the masked frame with background image where it's black
    processed_frame = np.where(masked_frame==0, bg, masked_frame)

    #Showing video output
    cv2.imshow('frame', processed_frame)
    cv2.waitKey(1)

    #Terminating the process if user presses Escape key
    if keyboard.is_pressed('esc'):
        VC.release()
        cv2.destroyAllWindows()
        break