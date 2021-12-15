import numpy as np
import cv2
import os
import time
import picamera

import RPi.GPIO as GPIO
from PCA9685 import PCA9685

pwm = PCA9685()
pwm.setPWMFreq(50)

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

current_PAN  = 90
current_TILT = 20
pwm.setRotationAngle(1, 180) #PAN    
pwm.setRotationAngle(0, current_TILT) #TILT

x=230
y=110


while True:
    ret, img = cap.read()
    #img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20,20)
    )
    for (x,y,w,h) in faces:
        print(x,y,w,h)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
            
        if x in range(220,240):
            time.sleep(0.0001)
        elif x> 240:
            pwm.setRotationAngle(1, current_PAN) #PAN
            current_PAN=current_PAN-2
            time.sleep(0.0001) 
        elif x<220:
            pwm.setRotationAngle(1, current_PAN) #PAN 
            current_PAN=current_PAN+2
            time.sleep(0.0001)
            
                
        if y in range(60,140):
            time.sleep(0.0001)
        elif y> 140:
            pwm.setRotationAngle(0, current_TILT) #PAN
            current_TILT=current_TILT+2
            time.sleep(0.0001) 
        elif y<60:
            pwm.setRotationAngle(0, current_TILT) #PAN 
            current_TILT=current_TILT-2
            time.sleep(0.01)
        
    cv2.imshow('video',img)
    
    
    
    
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
cap.release()
cv2.destroyAllWindows()
