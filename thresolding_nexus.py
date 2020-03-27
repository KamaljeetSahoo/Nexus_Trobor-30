# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 16:00:33 2020

@author: HP
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
import imutils
import math
import serial
import time
a,b = 320,480

def nothing(val):
    pass

ser = serial.Serial('COM7',9600, timeout=1)


cap = cv2.VideoCapture(1)
#cap = cv2.VideoCapture(1)


cv2.namedWindow('color')
cv2.createTrackbar('h','color',36,255,nothing)
cv2.createTrackbar('s','color',174,255,nothing)
cv2.createTrackbar('v','color',32,255,nothing)
cv2.createTrackbar('H','color',76,255 ,nothing)
cv2.createTrackbar('S','color',212,255,nothing)
cv2.createTrackbar('V','color',196,255,nothing)

kernel = np.ones((10,10), np.uint8)

while(True):
    ret, img = cap.read()
    #cv2.imshow("org",img)
   
    
    img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #cv2.imshow("org1",img)
    img=cv2.resize(img,(700,460))
    img=cv2.GaussianBlur(img,(15,15),0)
    #cv2.imshow("org2",img)
    img2=cv2.resize(img,(700,460))
    img2=cv2.GaussianBlur(img,(5,5),0)
    img2=cv2.cvtColor(img2,cv2.COLOR_HSV2BGR)
    
    h=cv2.getTrackbarPos('h','color')
    s=cv2.getTrackbarPos('s','color')
    v=cv2.getTrackbarPos('v','color')
    H=cv2.getTrackbarPos('H','color')
    S=cv2.getTrackbarPos('S','color')
    V=cv2.getTrackbarPos('V','color')
    lower=np.array([h,s,v])
    higher=np.array([H,S,V])
    
    
    mask=cv2.inRange(img,lower,higher)

    color=cv2.bitwise_and(img,img,mask=mask)
    color1=cv2.cvtColor(color,cv2.COLOR_BGR2GRAY)
    
    dilation = cv2.dilate(color1, kernel, iterations=1)
    
    cnts,_=cv2.findContours(dilation.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #cnts=imutils.grab_contours(cnts)
    cv2.drawContours(img2,cnts,-1,(255,255,0),10)
    
    cY_dict = {}
    
    for c in cnts:
        #cnts1=cnts[c]
        M = cv2.moments(c)
    
        if M['m00']==0:
            pass
        else :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(img2,(cx,cy),7,(255,255,0),-1)
            cv2.drawContours(img2, [c], -1, (0, 255, 0), 2)
            cv2.circle(img2, (cx, cy), 7, (255, 255, 255), -1)
            cv2.circle(img2, (a,b), 5, (255, 0 ,0), -1)
            #cv2.line(img2, (a,b), (cx, cy), (0,0,255), 4)
            cv2.line(img2, (a,b), (320, 0), (0,255,0), 4)
            
        cY_dict[cx]=cy
        maxcX = max(cY_dict.keys(), key=(lambda k: cY_dict[k]))
        maxcY=cY_dict[maxcX]
        
        #maxcY=max(cY_list)
        cv2.line(img2, (a,b), (maxcX, maxcY), (0,255,255), 4)
        
        tanA=(maxcX-a)/(maxcY-b)
        tanB=(320-a)/(0-b)
        TAN=(tanA-tanB)/(1+(tanA*tanB))
        angle=-(((math.atan(TAN))*180)/3.14)
        print("angle",angle)
        
        if(int(angle) in range(-5,5)):
            ser.write(b'F')
            print("forward")
        elif(int(angle) in range(-45,-5)):
            ser.write(b'A')
            print("forward_left")
        elif(int(angle) in range(-90,-45)):
            ser.write(b'L')
            print("left")
        elif(int(angle) in range(5,45)):
            ser.write(b'B')
            print("forward_right" )
        elif(int(angle) in range(45,90)):
            ser.write(b'R')
            print("right")
        else:
            ser.write(b'S')
            print("stop")
            
        
            
            
    #cv2.imshow("color",np.hstack([color,img2]))
    cv2.imshow("color",img2)
    #c
    #cv2.imshow("color",img)
    if cv2.waitKey(24)==27:
        break
    
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
