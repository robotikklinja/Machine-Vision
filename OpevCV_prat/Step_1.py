"""
This code shall take a frame from a video feed (camera) 
and make a picture of the card and make a line .

This code is to experiment with and make the card stand.

Made by B.Stokke on 07.11.2024

Updated by:
B.Stokke on 11.11.2024
"""

import cv2 as cv
import numpy as np

#Function to rescale the frame of the image
def resize_nr(image, scale=0.75): 
    # There is no reson funciton wise why thre image.shape[1]*0 is there.
    # The only reson why it is there is so that changes is easy and for understanding of code.
    width = int(image.shape[1]*0 + 600) # When frame.shape is 1 we refer to the width
    height = int(image.shape[0]*0 + 400) # When frame.shape is 0 we refer to the height

    dimensions = (width,height) # Define it as dimensions

    return cv.resize(image, dimensions, interpolation=cv.INTER_AREA)

# A function that finds cards and makes a line around it
def find_card(img):
    img = resize_nr(img)
    # Make an image to black and white (including gray)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # blur the image to make shapes more clear by take away any details
    blurred = cv.GaussianBlur(gray, (5, 5), 0)

    # Highlights the edges in an image
    edges = cv.Canny(blurred, 50, 150)

    # Finds the contours in an image (shapes)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Make an array called cards
    cards = []
    for contour in contours: # looks for shapes that have 4 sides

        # Tolerance for how accurate the shape can be (2%)
        epsilon = 0.02 * cv.arcLength(contour, True) 
        
        # A list of points for the shape
        approx = cv.approxPolyDP(contour, epsilon, True)

        # If any shapes that have 4 corners (points), then add the points of the shape in cards 
        if len(approx) == 4 and cv.contourArea(approx) > 1000: # not too small shape
            cards.append(approx) # Add approx to the array cards 
        
    # Make a copy of the original image 
    copy_image = img.copy() 
    for card in cards: # Draw a line through the points to a shape, that has been added above
        cv.drawContours(copy_image, [card], -1, (0, 255, 0), 2) # the order is in BGR not RBG for the color
    cv.imshow("Detected Card", copy_image) 
    cv.imshow("Edges", edges)

    # Perspective transform to isolate each card 
    for i, card in enumerate(cards):
        # Get the bounding box coordinates for each card
        pts = card.reshape(4, 2)

        # Sort the points to order them as top-left, top-right, bottom-right, bottom-left
        # (Necessary for perspective transform to work properly)
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
    
        # Compute the width and height of the card (max)
        widthA = np.sqrt(((rect[2][0] - rect[3][0]) ** 2) + ((rect[2][1] - rect[3][1]) ** 2))
        widthB = np.sqrt(((rect[1][0] - rect[0][0]) ** 2) + ((rect[1][1] - rect[0][1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
    
        heightA = np.sqrt(((rect[1][0] - rect[2][0]) ** 2) + ((rect[1][1] - rect[2][1]) ** 2))
        heightB = np.sqrt(((rect[0][0] - rect[3][0]) ** 2) + ((rect[0][1] - rect[3][1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
    
        # Define the destination points for the "flattened" card
        dst_pts = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")
    
        # Compute the perspective transform matrix and apply it 
        M = cv.getPerspectiveTransform(rect, dst_pts)
        warped = cv.warpPerspective(img, M, (maxWidth, maxHeight))

        # Make the image stand (long side is vertical)
        if warped.shape[1] > warped.shape[0]: # Check if the width is longer than hight
            warped = cv.rotate(warped, cv.ROTATE_90_CLOCKWISE) # Rotate image (clockwise)

        # Display each card individually 
        cv.imshow(f"Card {i+1}", warped)    

# Video feed
capture = cv.VideoCapture(1)

# Constant loop*
while True:
    # Set frame to be an image/frame of the video feed 
    ifTrue, frame = capture.read()
    
    # Find and make a square around the card/square 
    # and show the results 
    find_card(frame)
    
    # Used to break from the loop
    if cv.waitKey(20) & 0xFF==ord('q'):
        break

# Stop capturing from the camera 
capture.release()

# Destroy the windows made
cv.destroyAllWindows()
