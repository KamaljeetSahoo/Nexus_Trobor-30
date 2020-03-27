# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 22:32:50 2020

@author: Kamaljeet
"""

import serial
import cv2
import numpy as np
import math

a,b = 320,480
global angle

def nothing(val):
    pass

cv2.namedWindow('circles')
cv2.createTrackbar('h','circles',36,255,nothing)
cv2.createTrackbar('s','circles',165,255,nothing)
cv2.createTrackbar('v','circles',25,255,nothing)
cv2.createTrackbar('H','circles',70,255 ,nothing)
cv2.createTrackbar('S','circles',255,255,nothing)
cv2.createTrackbar('V','circles',255,255,nothing)



def circle_detection(img_c):
    
    kernel = np.ones((10,10), np.uint8)

    
    #start of thresholding of cicles
    img_c = cv2.cvtColor(img_c,cv2.COLOR_BGR2HSV)
    img_c=cv2.GaussianBlur(img_c,(15,15),0)
    
    h=cv2.getTrackbarPos('h','circles')
    s=cv2.getTrackbarPos('s','circles')
    v=cv2.getTrackbarPos('v','circles')
    H=cv2.getTrackbarPos('H','circles')
    S=cv2.getTrackbarPos('S','circles')
    V=cv2.getTrackbarPos('V','circles')
    lower = np.array([h,s,v])
    higher = np.array([H,S,V])
    
    mask=cv2.inRange(img_c,lower,higher)
    
    color=cv2.bitwise_and(img_c,img_c,mask=mask)
    
    
    #start of dilation of image to detect circles
    color1=cv2.cvtColor(color,cv2.COLOR_BGR2GRAY)
    
    dilation = cv2.dilate(color1, kernel, iterations=1)
    
    cnts,_=cv2.findContours(dilation.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    cv2.drawContours(color1,cnts,-1,(255,255,0),10)
    
    cY_dict = {}
    
    for c in cnts:
        #cnts1=cnts[c]
        M = cv2.moments(c)
    
        if M['m00']==0:
            pass
        else :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(color1,(cx,cy),7,(255,255,0),-1)
            #cv2.drawContours(img2, [c], -1, (0, 255, 0), 2)
            #cv2.circle(img2, (cx, cy), 7, (255, 255, 255), -1)
            cv2.circle(color1, (a,b), 5, (255, 0 ,0), -1)
            #cv2.line(img2, (a,b), (cx, cy), (0,0,255), 4)
            cv2.line(color1, (a,b), (320, 0), (0,255,0), 4)
            
        cY_dict[cx]=cy
        maxcX = max(cY_dict.keys(), key=(lambda k: cY_dict[k]))
        maxcY=cY_dict[maxcX]
        
        #maxcY=max(cY_list)
        cv2.line(color1, (a,b), (maxcX, maxcY), (0,255,255), 4)
        if((maxcY-b) == 0):
            pass
        else:
            tanA=(maxcX-a)/(maxcY-b)
            tanB=(320-a)/(0-b)
            TAN=(tanA-tanB)/(1+(tanA*tanB))
            angle=-(((math.atan(TAN))*180)/3.14)
            print("angle",angle)
    
        cv2.imshow("final", color1)
    
    

    
    
    
    
cap = cv2.VideoCapture("C:\\Users\\Kamaljeet\\Desktop\\Raj\\Nexus\\WIN_20200116_12_21_35_Pro.mp4")   
while(True):
    ret, frame = cap.read()
    
    circle_detection(frame)
    
    cv2.imshow('frame',frame)
    if cv2.waitKey(24) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()