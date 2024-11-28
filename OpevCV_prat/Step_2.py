import cv2 as cv

capture = cv.VideoCapture(0)

while True:
    ifTrue, frame = capture.read()

    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("gray", frame)

    frame = cv.GaussianBlur(frame, (3,3), cv.BORDER_DEFAULT)
    cv.imshow("Blur Image", frame)

    #frame = cv.Canny(frame, 125, 175)
    thresholded_image = cv.threshold(frame, 127, 255, cv.THRESH_BINARY)
    cv.imshow("Canny", frame)

    frame = cv.Canny(frame, 125, 175)
    cv.imshow("Video", frame)
    
    if cv.waitKey(20) & 0xFF==ord('q'):
        break

capture.release()

cv.destroyAllWindows

