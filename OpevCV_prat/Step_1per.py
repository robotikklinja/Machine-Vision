"""
This code shall simulate* an input frame from a video feed
and show a square around a card or cards and make a 2D image of the card 
that is shown in another window. 

It does this by first reading the video feed for anny shapes 
and looks for squares and makes a line around that square 

Made by B.Stokke on 08.11.2024
"""

import cv2 as cv
import numpy as np

# Load an image/frame 
image = cv.imread(r'OpevCV_prat\Photos\Heart_A.jpg') 
dimension = (200, 300)
image = cv.resize(image, dimension, interpolation=cv.INTER_AREA)

# Convert to grayscale 
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) 

# Apply Gaussian blur to reduce noise in the image 
blurred = cv.GaussianBlur(gray, (5, 5), 0) 

# Use Canny edge detection to find edges 
edges = cv.Canny(blurred, 50, 150) 

# Find contours in the edge-detected image 
contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) 

# Filter contours to identify the card/squares 
cards = [] 
for contour in contours: 
    # Approximate the contour to a polygon 
    epsilon = 0.02 * cv.arcLength(contour, True) 
    approx = cv.approxPolyDP(contour, epsilon, True) 
    
    # Check if the approximated contour has four points (suggesting a rectangle) 
    # and if it has a large enough area (to filter out small noise) 
    if len(approx) == 4 and cv.contourArea(approx) > 1000: 
        cards.append(approx) 

# Draw the detected card/square on the original image
output_image = image.copy()
for card in cards:
    # Green outline for each detected card
    cv.drawContours(output_image, [card], -1, (0, 255, 0), 2) 

# Display the result
cv.imshow("Detected Cards", output_image)

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
    
    # Compute the width and height of the card
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
    warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))
    
    # Display each card individually 
    cv.imshow(f"Card {i+1}", warped)
    cv.waitKey(0)

cv.destroyAllWindows()
