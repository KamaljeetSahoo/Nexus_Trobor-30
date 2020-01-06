# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 12:56:28 2020

@author: Kamaljeet
"""
import numpy as np
import cv2

cap = cv2.VideoCapture(1)

a,b = 320,480

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    edged = cv2.Canny(gray, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    cY_dict = {}

    for c in contours:
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
            cv2.circle(frame, (a,b), 5, (255, 0 ,0), -1)
            #cv2.line(frame, (a,b), (cX, cY), (0,0,255), 4)
            cv2.line(frame, (a,b), (320, 0), (0,255,0), 4)
        else:
            cX, cY = 0, 0
            
        cY_dict[cX]=cY
        maxcX = max(cY_dict.keys(), key=(lambda k: cY_dict[k]))
        maxcY=cY_dict[maxcX]
        
        #maxcY=max(cY_list)
        cv2.line(frame, (a,b), (maxcX, maxcY), (0,255,255), 4)
        
        #print("thikthak",cY)
        
        
    #print("baharila")
    cY_list=[] 

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()