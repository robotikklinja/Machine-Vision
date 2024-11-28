"""
This code shall take a frame from a video feed (camera) 
and make a picture of the card and make an outline of za card.

This code is to experiment with and make the card stand.

Made by B.Stokke on 07.11.2024

Updated by:
B.Stokke & V.Dalisay on 21.11.2024
"""

import cv2 as cv
import numpy as np

def rankandsuit(corner):
    # note: split them rank and suit
    # Make an image to black and white (including gray)
    gray = cv.cvtColor(corner, cv.COLOR_BGR2GRAY)

    # highlights the edges in an image
    _, thresh = cv.threshold(gray, 1, 255, cv.THRESH_BINARY)
    
    # 
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    # 
    contours = sorted(contours, key=cv.contourArea, reverse=True)[:2]
    
    # 
    contours = sorted(contours, key=lambda c: cv.boundingRect(c)[1])

    rank_roi = corner[:, :]

    # x is starting horizontal-coordinates, w is end horizontal coordinates
    rank_x, rank_y, rank_w, rank_h = cv.boundingRect[contours(0)] # rank
    suit_x, suit_y, suit_w, suit_h = cv.boundingRect[contours(1)] # suit

    rank_img = corner[rank_y:rank_y+rank_h, rank_x:rank_x+rank_w] 
    suit_img = corner[suit_y:suit_y+suit_h, suit_x:suit_x+suit_w] 
    
    # Highlights the edges in an image
    edges = cv.Canny(contours, 50, 150)

    # Finds the contours in an image (shapes)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Note make rank and suit roi to isolate them


    return rank_img, suit_img

    

# A function that finds cards and makes a line around it
def find_card(img):
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


        #note to self move this out
        # h_n is the ratio of the total height of the card to the height of the roi
        h_n = 3.9
        # w_n is the ratio of the total width of the card to the width of the roi
        w_n = 5.9
        global h
        # h is the height of the card
        h = warped.shape[0]
        # n is the height of the card divided by the ratio
        n = h//h_n
        global w
        # w is the width of the card
        w = warped.shape[1]
        # v is the width of the card divided by the ratio w_n
        v = w//w_n

        ROI = warped[0:int(n), 0:int(v)]  # Adjust size as needed
    
        # Display each card individually 
        cv.imshow(f"Card {i+1}", warped)
        
        # Display 
        cv.imshow("Corner", ROI)

        roi_copy = ROI.copy()




# Video feed
capture = cv.VideoCapture(0)

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
