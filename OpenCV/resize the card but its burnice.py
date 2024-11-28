import cv2 as cv
import time

# time.sleep(1)
# capture = cv.VideoCapture(0)

# while True:
#     isTrue, frame = capture.read()
#     cv.imshow('Videos', frame)

#     if cv.waitKey(20) & 0xFF==ord('d'):
#         break
    
# capture.release()
# cv.destroyAllWindows()


image = cv.imread(r"Photos\sowarm.jpg", cv.IMREAD_GRAYSCALE)

def rescaleFrame(frame): #Function to rescale the frame of the window
    width = int(frame.shape[1]*0 + 70) # when frame.shape is 1 we refer to the width
    height = int(frame.shape[0]*0 + 125) # when frame.shape is 0 we refer to the height
    dimensions = (width,height) # define it as dimensions

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

resized_image = rescaleFrame(image) # The new image is now called resized_image
cv.imshow('image', resized_image) # show the resized image
cv.waitKey(0)