# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 20:20:23 2020

@author: Kamaljeet
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



cap = cv2.VideoCapture(1)
#cap = cv2.VideoCapture(1)


cv2.namedWindow('color')
cv2.createTrackbar('h','color',35,255,nothing)
cv2.createTrackbar('s','color',25,255,nothing)
cv2.createTrackbar('v','color',0,255,nothing)
cv2.createTrackbar('H','color',61,255 ,nothing)
cv2.createTrackbar('S','color',177,255,nothing)
cv2.createTrackbar('V','color',33,255,nothing)

kernel = np.ones((10,10), np.uint8)

while(True):
    ret, img = cap.read()
    #cv2.imshow("org",img)
   
    
    img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #cv2.imshow("org1",img)
    #img=cv2.resize(img,(700,460))
    img=cv2.GaussianBlur(img,(5,5),0)
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
    #cv2.drawContours(img2,cnts,-1,(255,255,0),2)
    
    
    for c in cnts:
        approx = cv2.approxPolyDP(c, 0.08* cv2.arcLength(c, True), True)
        #cnts1=cnts[c]
        M = cv2.moments(c)
        
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        print(len(approx))
        if len(approx) == 3:
            #ser.write(b'L')
            print("left")
        elif len(approx) == 4:
            #ser.write(b'R')
            print("right")
            #x1 ,y1, w, h = cv2.boundingRect(approx)
            #aspectRatio = float(w)/h
            #print(aspectRatio)
            #if aspectRatio >= 0.95 and aspectRatio <= 1.05:
            #    cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 200))
            #else:
            #    cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 200))
        #elif len(approx) == 5:
        #    cv2.putText(img, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 200))
        #elif len(approx) == 10:
        #    cv2.putText(img, "Star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 200))
        #else:
         #   cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 200))
                
                
        if M['m00']==0:
            pass
        else :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            if (cv2.contourArea(c)>10000):
                cv2.circle(img2,(cx,cy),7,(255,255,0),-1)
                cv2.drawContours(img2, [approx], -1, (0, 255, 0), 2)
                cv2.circle(img2, (cx, cy), 7, (255, 255, 255), -1)
                cv2.circle(img2, (a,b), 5, (255, 0 ,0), -1)
                #cv2.line(img2, (a,b), (cx, cy), (0,0,255), 4)
                #cv2.line(img2, (a,b), (320, 0), (0,255,0), 4)
            else:
                pass
            
        
        
            
            
    #cv2.imshow("color",np.hstack([color,img2]))
    cv2.imshow("color",img2)
    #c
    #cv2.imshow("color",img)
    if cv2.waitKey(24)==27:
        break
    
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
