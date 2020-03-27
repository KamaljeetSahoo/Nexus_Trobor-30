# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 18:15:59 2020

@author: Kamaljeet
"""

import serial
import struct
import time
import cv2


ser = serial.Serial('COM6',9600)
time.sleep(0.2)
while(cv2.waitKey(25) & 0xFF != ord('q')):
    ser.write(b'L')