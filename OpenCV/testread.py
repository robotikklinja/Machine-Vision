import cv2 as cv

# img = cv.imread('Photos/cat.jpg')

# cv.imshow('This is a window that displays a cat', img)

# Recording videos

capture = cv.VideoCapture('Videos/neverup.mp4')

while True:
    isTrue, frame = capture.read()
    cv.imshow('Videos', frame)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break
    
capture.release()
cv.destroyAllWindows()