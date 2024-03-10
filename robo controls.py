import os
import argparse
import cv2
import numpy as np
import sys
import RPi.GPIO as GPIO
import os
import time
from random import *
import threading
from time import sleep
import time
import requests
import time
import math
import datetime
import cv2




def connect():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False
    



url ='http://raspberrypi.microembeddedtech.com/queryconnect.php'
selectsqlquery="SELECT `command`, `mode` FROM `msrfacerobo` WHERE 1"




GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 21
GPIO_ECHO = 20
buzzerpin=26

m1=17
m2=18
m3=27
m4=22




GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(buzzerpin,GPIO.OUT)


GPIO.output(buzzerpin,0)

GPIO.setup(m1, GPIO.OUT) 
GPIO.setup(m2, GPIO.OUT)  
GPIO.setup(m3, GPIO.OUT)  
GPIO.setup(m4, GPIO.OUT)





distancestr="0"
intdist=0




def stoprobo():
    print("=== STOP ===")
    GPIO.output(m1,GPIO.LOW)
    GPIO.output(m2,GPIO.LOW)
    GPIO.output(m3,GPIO.LOW)
    GPIO.output(m4,GPIO.LOW)
    
def forwardrobo():
    print("=== FORWARD ===")
    GPIO.output(m1,GPIO.LOW)
    GPIO.output(m2,GPIO.HIGH)
    GPIO.output(m3,GPIO.LOW)
    GPIO.output(m4,GPIO.HIGH)
    
def backwardrobo():
    print("=== BACKWARD  ===")
    GPIO.output(m1,GPIO.HIGH)
    GPIO.output(m2,GPIO.LOW)
    GPIO.output(m3,GPIO.HIGH)
    GPIO.output(m4,GPIO.LOW)
    
def rightrobo():
    print("=== RIGHT ===")
    GPIO.output(m1,GPIO.HIGH)
    GPIO.output(m2,GPIO.LOW)
    GPIO.output(m3,GPIO.LOW)
    GPIO.output(m4,GPIO.LOW)
  
  
    
def leftrobo():
    print("=== LEFT ===")
    GPIO.output(m1,GPIO.LOW)
    GPIO.output(m2,GPIO.LOW)
    GPIO.output(m3,GPIO.HIGH)
    GPIO.output(m4,GPIO.LOW)
    

def buzzering():
    GPIO.output(buzzerpin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzerpin,GPIO.LOW)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def getdatafromdb():
    global distance
    global distancestr,intdist
  
    while True:
        myobj = {'query':selectsqlquery ,'key': 'querykey',}
        z = requests.post(url, data = myobj)
        print(z.text)  #<class 'str'>
        stringtext=z.text
        #print("\n")
        #print(stringtext)
        splittext = stringtext.split("\n")
        del splittext[0]
        del splittext[-1]
        print(splittext)
        opercmdstr=splittext[0]
        opertext = opercmdstr.split(",")
        
        #print("&&&&&& opertext:",opertext)
        opercmd=opertext[0]
        modecmd=opertext[1]
        print("ROBO COMMAND:",opercmd)
        print("MODE COMMAND:",modecmd)
        

        modecmdint=int(modecmd)
        if modecmdint==0:
            if opercmd=="1":
                forwardrobo()
            elif opercmd=="2":
                backwardrobo()
            elif opercmd=="3":
                rightrobo()
            elif opercmd=="4":
                leftrobo() 
            elif opercmd=="5":
                stoprobo()

        elif modecmdint==1 :
            print("------ AUTO MODE ----\n")
            if intdist < 20:
                forwardrobo()
            else:   
                stoprobo()
                time.sleep(2)
                backwardrobo()
                time.sleep(3)
                stoprobo()
                time.sleep(2)
                rightrobo()
                time.sleep(4)
                stoprobo()
                time.sleep(2)
                forwardrobo()
                time.sleep(4)
                stoprobo()
                time.sleep(2)
                leftrobo()
                time.sleep(4)
                stoprobo()
                time.sleep(2)
           
        else:
            stoprobo()

      

        time.sleep(1)
    
def sensorscan():
    global distance
    global distancestr,intdist
    while True:
        #print("**********************")
        dist = distance()
        print ("Measured Distance = %.1f cm" % dist)
        
        intdist=int(dist)
        distancestr=str(intdist)

        if intdist < 20:
            print("-- OBSCTABLE DETECTED ---")
            buzzering()
        
        time.sleep(2)
     

# def camscan():

#     global distance
#     vid = cv2.VideoCapture(0)
#     vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
#     ##############################################
#     while True:
#         ret, frame = vid.read()
#         cv2.imshow('frame', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     vid.release()
#     cv2.destroyAllWindows


    
if __name__ =="__main__":  
    robocontrol=threading.Thread(target=getdatafromdb)
    irsense=threading.Thread(target=sensorscan)
    #camview=threading.Thread(target=camscan)
    robocontrol.start()
    #camview.start()
    irsense.start()
    
