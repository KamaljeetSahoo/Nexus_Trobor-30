# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 20:22:45 2020

@author: Kamaljeet
"""

import serial, time
arduino = serial.Serial('COM7', 9600, timeout=.1)
time.sleep(1) #give the connection a second to settle

while True:
    arduino.write(b"qwerty")
    data = arduino.readline()
    