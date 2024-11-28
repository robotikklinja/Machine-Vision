"""

This code is going to resize an image so that it can be campared later.
There is a image witch has the correct dimensions and can be compared visually

To resize to the correct size you must add the width and the height separately 
All the refference images must be the same size and dimensions.

Made by Vincent on 24.10.2024
"""

import cv2 as cv

# A random* image that are going to be resized
cardimg = cv.imread(r"Photos\tanjiro.jpg")
cv.imshow("Visuel Check", cardimg)

# Get images from the directory "Photos/tanjiro.jpg", and define it as img
suitimg = cv.imread(r"Photos\cat.jpg")
cv.imshow('Orginal image', suitimg) # put the picture in a window named "Original Image"

#Function to rescale the frame of the window
def rescaleNumber(image): 
    width = int(70) # When frame.shape is 1 we refer to the width
    height = int(125) # When frame.shape is 0 we refer to the height

    dimensions = (width,height) # Define it as dimensions

    return cv.resize(image, dimensions, interpolation=cv.INTER_AREA)

def rescaleSuit(image):
    width = int(70)
    height = int(120)

    dimensions = (width, height)
    return cv.resize(image, dimensions, interpolation=cv.INTER_AREA)

resized_number = rescaleNumber(cardimg) # The new image is now called resized_image
resized_suit = rescaleSuit(suitimg)

cv.imshow("NewNr", resized_number) # show the resized image

cv.imshow("NewSuit", resized_suit)

cv.waitKey(0) # wait for a key to be pressed 