import cv2 as cv

# Get images from the directory "Photos/tanjiro.jpg", and define it as img
img = cv.imread('Photos/tanjiro.jpg') 
# cv.imshow('Tanjiro', img) # put the picture in a window named "Tanjiro"
cv.imshow('Original', img)

def rescaleFrame(frame, scale=0.75): #Function to rescale the frame of the window
    width = int(frame.shape[1] * scale) # when frame.shape is 1 we refer to the width
    height = int(frame.shape[0] * scale) # when frame.shape is 0 we refer to the height
    dimensions = (width,height) # define it as dimensions

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

resized_image = rescaleFrame(img) # The new image is now called resized_image
cv.imshow('image', resized_image) # show the resized image
cv.waitKey(0)

# Get video from the directory "Videos/neverup.mp4", and define it as capture
capture = cv.VideoCapture('Videos/neverup.mp4')


# while True:
#     isTrue, frame = capture.read() # Read whatever is in the video as frame

#     frame_resized = rescaleFrame(frame) #resize the video using the rescaleFrame function
#     cv.imshow('Videos', frame)
#     cv.imshow('Video Resized', frame_resized)

#     if cv.waitKey(20) & 0xFF==ord('d'):
#         break
    
# capture.release()
# cv.destroyAllWindows()
