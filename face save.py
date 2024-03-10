# face save/ cropper
import cv2
import sys
import os
import time
os.system("sudo modprobe bcm2835-v4l2")
imagecount=1
startcapture=0

existpath="/home/pi/facesfolder/"
folder_name=input('Enter your identification name: ')
facesdirectorypath=existpath+folder_name

try:
    os.makedirs(facesdirectorypath)
except FileExistsError:
     print("Directory already exists")
     #Do something else or just pass

os.system("sudo chmod 777 /home/pi/facesfolder/*")

cascPath = "/home/pi/facecropper/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    ) 


    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #roi_color = frame[y:y + h, x:x + w]
        faces = frame[y:y + h, x:x + w]
        if imagecount!=10 and startcapture==1:
            storeface=facesdirectorypath+"/"+folder_name+"_"+str(imagecount)+".jpg"
            cv2.imwrite(storeface,faces)
            time.sleep(3)
            imagecount=imagecount+1
        else:
            if startcapture==1:
                startcapture=0
            #cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color) 

    # Display the resulting frame
    cv2.imshow('Video', frame)
    k=cv2.waitKey(1)
    if k==ord('s') or k== ord('S') :
        startcapture=1
    elif k== ord('q') or k==ord('Q'):
        break
        

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()


# face save/ cropper
import cv2
import sys
import os
import time
os.system("sudo modprobe bcm2835-v4l2")
imagecount=1
startcapture=0

existpath="/home/pi/facesfolder/"
folder_name=input('Enter your identification name: ')
facesdirectorypath=existpath+folder_name

try:
    os.makedirs(facesdirectorypath)
except FileExistsError:
     print("Directory already exists")
     #Do something else or just pass

os.system("sudo chmod 777 /home/pi/facesfolder/*")

cascPath = "/home/pi/facecropper/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    ) 


    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #roi_color = frame[y:y + h, x:x + w]
        faces = frame[y:y + h, x:x + w]
        if imagecount!=10 and startcapture==1:
            storeface=facesdirectorypath+"/"+folder_name+"_"+str(imagecount)+".jpg"
            cv2.imwrite(storeface,faces)
            time.sleep(3)
            imagecount=imagecount+1
        else:
            if startcapture==1:
                startcapture=0
            #cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color) 

    # Display the resulting frame
    cv2.imshow('Video', frame)
    k=cv2.waitKey(1)
    if k==ord('s') or k== ord('S') :
        startcapture=1
    elif k== ord('q') or k==ord('Q'):
        break
        

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()


