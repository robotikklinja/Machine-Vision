import cv2 as cv
import numpy as np
import time

def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

time.sleep(1)
capture = cv.VideoCapture(0)

blank = np.zeros((500, 500), dtype="uint8")
#cv.imshow("Blank", blank)

img = cv.imread("OpevCV_prat\Photos\cat.jpg")
cv.imshow("Cat", img)



while True:
    isTrue, frame = capture.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("gray", frame)

    # frame = cv.GaussianBlur(frame, (3,3), cv.BORDER_DEFAULT)
    # cv.imshow("Blur Image", frame)

    #frame = cv.Canny(frame, 125, 175)
    thresholded_image = cv.threshold(frame, 127, 255, cv.THRESH_BINARY)
    cv.imshow("Canny", frame)

    frame = cv.Canny(frame, 125, 175)
    cv.imshow("Video", frame)
    
    if cv.waitKey(20) & 0xFF==ord('q'):
        break

capture.release()

cv.destroyAllWindows
