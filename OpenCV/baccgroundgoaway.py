import cvzone
import cv2 as cv
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import mediapipe

vid = cv.VideoCapture(0)
vid.set(3,400)
vid.set(4,250)

segmentor = SelfiSegmentation()

# Constant loop*
while True:
    # Set frame to be an image/frame of the video feed
    ifTrue, frame = vid.read()
    jotaro = segmentor.removeBG(frame, (0,255,0), cutThreshold=0.6)
    cv.imshow("dio", jotaro)

    # Used to break from the loop
    if cv.waitKey(20) & 0xFF==ord('q'):
        break

# Stop capturing from the camera 
vid.release()
# Destroy the windows made
cv.destroyAllWindows()
