#!/usr/bin/python3

# import the necessary packages
import imutils
from imutils import paths
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import pickle
import time
import cv2
import os
import RPi.GPIO as GPIO
import time
from bisect import bisect_left
from datetime import datetime
import sys
import time
import random
import telepot


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#buzzerpin=11

#GPIO.setup(buzzerpin,GPIO.OUT)
#GPIO.output(buzzerpin,GPIO.LOW)

#BUZZER
#def buzzeron():
        #GPIO.output(buzzerpin,GPIO.HIGH)

#def buzzeroff():
        #GPIO.output(buzzerpin,GPIO.LOW)
        
sendm=0
prevname=""
imagesent=0

chat_id=1355785588
bot = telepot.Bot('6989135850:AAGv2zHbLI2vaezGv364E7ek2FtpfKYWKQc')



os.system("sudo chmod uga+rw -R /home/pi/facesfolder")

print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images('/home/pi/facesfolder'))

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
    # extract the person name from the image path
    print("[INFO] processing image {}/{}".format(i + 1,
        len(imagePaths)))
    name = imagePath.split(os.path.sep)[-2]

    # load the input image and convert it from RGB (OpenCV ordering)
    # to dlib ordering (RGB)
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb,
        model='hog')

    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)

    # loop over the encodings
    for encoding in encodings:
        # add each encoding + name to our set of known names and
        # encodings
        knownEncodings.append(encoding)
        knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open('/home/pi/facerecog/encodings.pickle', "wb")
f.write(pickle.dumps(data))
f.close()


print("[INFO] loading encodings + face detector...")
data = pickle.loads(open('/home/pi/facerecog/encodings.pickle', "rb").read())
detector = cv2.CascadeClassifier('/home/pi/facerecog/haarcascade_frontalface_default.xml')

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()



# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to 500px (to speedup processing)
        frame = vs.read()
       
        
        # convert the input frame from (1) BGR to grayscale (for face
        # detection) and (2) from BGR to RGB (for face recognition)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        # OpenCV returns bounding box coordinates in (x, y, w, h) order
        # but we need them in (top, right, bottom, left) order, so we
        # need to do a bit of reordering
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)
            
            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom),
                (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 0), 2)
            print(" RECOGNIZED ", name);
            if name=="Unknown":
                print("+++++ STRANGER DETECTED ++++++")
                if imagesent==1:
                    imagesent=0
                #readtext="THE PERSON IS STRANGER"
                #os.system("echo '" + readtext + "' | festival --tts")
                #espeak(readtext)
                prevname=name
            else:
                
                print(name)
                readtextr="THE PERSON AHEAD OF YOUR IS "+ name
                print(readtextr)
                if imagesent==0:
                    imagesent=1
                    dt_string="1111"
                   
                    msgtobesend= dt_string
                    cv2.imwrite("/home/pi/detectedimage.jpg",frame)
                    bot.sendPhoto(chat_id=chat_id, photo=open('/home/pi/detectedimage.jpg', 'rb'))
                    bot.sendMessage(chat_id=chat_id,text=msgtobesend)
                #os.system("echo '" + readtextr + "' | festival --tts")
                #espeak(readtextr)
                prevname=name
                
                       
        # display the image to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        # update the FPS counter
        fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

