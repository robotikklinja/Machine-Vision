"""
This code is going to resize an image so that it can be campared later.
There is a image witch has the correct dimensions and can be compared visually

To resize to the correct size you must add the width and the height separately 
All the refference images must be the same size and dimensions.

Since we use two different reference sizes, one for number and one for suit
there are two functions. 

Use of the worng function can happen and for unknown resize it's own function must be made.

Made by Vincent on 24.10.2024

Updated on:
01.11.2024 by B.Stokke & Vincent
"""

import cv2

# A random* image that are going to be resized
img2 = cv2.imread(r"OpevCV_prat\Card_Imgs\Clubs.jpg")
cv2.imshow("Visuel Check", img2)

# Get images from the directory "Photos/tanjiro.jpg", and define it as img
img = cv2.imread(r"OpevCV_prat\Photos\cat.jpg")
cv2.imshow('Orginal image', img) # put the picture in a window named "Original image"

#Function to rescale the frame of the image
def resize_nr(image, scale=0.75): 
    # There is no reson funciton wise why thre image.shape[1]*0 is there.
    # The only reson why it is there is so that changes is easy and for understanding of code.
    width = int(image.shape[1]*0 + 70) # When frame.shape is 1 we refer to the width
    height = int(image.shape[0]*0 + 125) # When frame.shape is 0 we refer to the height

    dimensions = (width,height) # Define it as dimensions

    return cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)

#Function to rescale the frame of the image
def resize_suit(image, scale=0.75): 
    width = int(image.shape[1]*0 + 70) # When frame.shape is 1 we refer to the width
    height = int(image.shape[0]*0 + 100) # When frame.shape is 0 we refer to the height

    dimensions = (width,height) # Define it as dimensions

    return cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)

resized_suit = resize_suit(img) # The new image is now called resized_image
cv2.imshow("image", resized_suit) # show the resized image
cv2.waitKey(0) # wait for a key to be pressed 