# This code was used to learn about the basic OpenCV functions

import cv2 as cv
import numpy as np

# read from an image in a relative path
img = cv.imread('Photos/sowarm.jpg')
cv.imshow('sowarm', img) # Display it

blank = np.zeros(img.shape[:2], dtype='uint8')
cv.imshow('Blank', blank)

# Use cvtColor to change the color palette of the image to a grayscale color palette
grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('graywarm', grayimg) # Display it

# # Blur the image so we get less edges, useful to not let the pc die
# blur = cv.GaussianBlur(grayimg, (5,5), cv.BORDER_DEFAULT)
# cv.imshow('blurred', blur)

# # Use cv.Canny to show specified kinds of edges. Here we use a range from 125 to 175
# canny = cv.Canny(blur, 125, 175)
# cv.imshow('Blurred edges', canny) # Display image but with only edges

# Thresholding of an image means that a shade of gray that is lighter than x will be blank, 0, and darker will be white, 255
ret, thresh = cv.threshold(grayimg, 80, 255, cv.THRESH_BINARY)
cv.imshow('threshold', thresh)
# Hierarchies are used when there are more shapes inide a shape
# RETR_something is used to specify which contours to extract.
    # TREE returns everything, with hierarchies.
    # LIST returns everything without any hierarchies. (no parent or child edges)
# CHAIN_APPROX_SIMPLE (idk tbh)
contours, hierarchies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
# The contours are in an array, so display how many contours there are displayed
print(f'{len(contours)} contour(s) found:')

cv.waitKey(0)