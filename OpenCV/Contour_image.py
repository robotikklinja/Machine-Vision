import cv2 as cv

# img = cv.imread('Photos/sowarm.jpg')
# cv.imshow('sowarm', img)

# grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow('graywarm', grayimg)

# Open the camrea
capture = cv.VideoCapture(0)

if not capture.isOpened():
    print("Error: Could not open camera.")
    exit()


while True:
    # Read all frames of the live video
    isTrue, frame = capture.read()
    # Show it into a frame
    cv.imshow('Videos', frame)
    
    # Turns the live video into a grayscale live video
    grayframe = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('Grayvid', grayframe)

    # Blur the image so we get less edges, useful to not let the pc die
    blur = cv.GaussianBlur(grayframe, (5,5), 0)
    cv.imshow('blurred', blur)

    # Threshold makes the pixels either black or white 
    ret, thresh = cv.threshold(blur, 175, 225, cv.THRESH_BINARY + cv.THRESH_OTSU)
    cv.imshow('threshold (otsu)', thresh)

    # canny is the thresholded frame but with contours. So it makes contours from the thresholded image
    canny = cv.Canny(thresh, 100, 200)
    contours, hierarchies = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    frame_copy = frame.copy() # Create a copy of the original frame to draw contours
    cv.drawContours(frame_copy, contours, -1, (0, 200, 0), 2)
    cv.imshow('Canny', canny)

    # If the key q is pressed destroy all windows
    if cv.waitKey(20) & 0xFF==ord('q'):
        break
    
capture.release()
cv.destroyAllWindows()