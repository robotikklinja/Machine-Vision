"""
This code shall take a frame from a video feed (camera) 
and make a picture of the card and make an outline of za card.

This code is to experiment with and make the card stand.

Made by B.Stokke on 07.11.2024

Updated by:
B.Stokke & V.Dalisay on 21.11.2024
V.Dalisay on 28.11.2024
V.Dalisay on 05.11.2024
"""

import cv2 as cv
import numpy as np
import time

# This is just to start taking the time for how much time this code takes to run
start = time.time()

# Function to isolate the suit and the rank from each other
def rankandsuit(corner):

    #the height and width of the corner are defined as h and w
    h, w, _ = corner.shape

    # make the corner into a grayscale
    gray = cv.cvtColor(corner, cv.COLOR_BGR2GRAY)

    # round the height of the corner of the card to 10% and make it into a diff_h variable, so that the rank and suit are separated properly.
    diff_h = round(h * 0.1) # 10%

    # this is to divide the rank and the suit. It uses the rank 
    rank_height = (h//2) + diff_h

    # divide the grayscaled corner into the rank and the suit
    grayrank = gray[0:((h//2)+diff_h), 0:w] # ROI for Rank
    graysuit = gray[((h//2)+diff_h):h, 0:w] # ROI for Suit

    # # Get the coordinates of the Rank and Suit regions (for bounding boxes)
    # rank_x, rank_y, rank_w, rank_h = 0, 0, w, (h // 2) + diff_h
    # suit_x, suit_y, suit_w, suit_h = 0, (h // 2) + diff_h, w, h

    # # Draw bounding boxes around Rank and Suit
    # cv.rectangle(corner, (rank_x, rank_y), (rank_x + rank_w, rank_y + rank_h), (0, 255, 0), 2)  # Green bounding box for Rank
    # cv.rectangle(corner, (suit_x, suit_y), (suit_x + suit_w, suit_y + suit_h), (0, 0, 255), 2)  # Red bounding box for Suit

    # # Show the images with the bounding boxes
    # cv.imshow('Rank and Suit with Bounding Boxes', corner)

    # blur the images so that it dont got too much noise
    blurrank = cv.GaussianBlur(grayrank, (1,1), cv.BORDER_DEFAULT)
    blursuit = cv.GaussianBlur(graysuit, (1,1), cv.BORDER_DEFAULT)

    # turns the crayscaled images into an image full of edges
    R_edge = cv.Canny(blurrank, 50, 150)
    S_edge = cv.Canny(blursuit, 50, 150)

    # Find contours to help with the bounding of the rank and suit
    R_contour, _ = cv.findContours(R_edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    S_contour, _ = cv.findContours(S_edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    #Set a bounding boxx for both the rank and the suit of the card
    rank_x, rank_y, rank_w, rank_h = cv.boundingRect(R_contour[0])
    suit_x, suit_y, suit_w, suit_h = cv.boundingRect(S_contour[0])

    rank_img = corner[rank_y : rank_y + rank_h, rank_x : rank_x+ rank_w] # Rank img
    suit_img = corner[suit_y + rank_height : rank_height + suit_y + suit_h, suit_x : suit_x + suit_w] # Suit img

    cv.imshow('rankimg', rank_img)
    cv.imshow('suitimg', suit_img)  

    def rescaleFrame(frame, scale=5): #Function to rescale the frame of the window
        width = int(frame.shape[1] * scale) # when frame.shape is 1 we refer to the width
        height = int(frame.shape[0] * scale) # when frame.shape is 0 we refer to the height
        dimensions = (width, height) # define it as dimensions

        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    resized_rank_img = rescaleFrame(rank_img) # The new image is now called resized_rank_img
    cv.imshow('resized rank image', resized_rank_img) # show the resized image
    resized_suit_img = rescaleFrame(suit_img) # The new image is now called resized_suit_img
    cv.imshow('resized suit image', resized_suit_img) # show the resized image

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
        
    # # if card are not forund then return nothing (feilsøking)
    # if not cards:
    #     print("No cards detected")
        
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

        # h_n is the ratio of the total height of the card to the height of the roi
        # w_n is the ratio of the total width of the card to the width of the roi
        h_n, w_n = 4, 6.2
        # h is the height of the card. w is the width of the card
        h, w = warped.shape[0], warped.shape[1]
        # n is the height of the card divided by the ratio. v is the width of the card divided by the ratio w_n
        n, v = h//h_n, w//w_n

        ROI = warped[0:int(n), 0:int(v)]  # Adjust size as needed
    
        # Display each card individually 
        cv.imshow(f"Card {i+1}", warped)
        # Display the corner
        cv.imshow("Corner", ROI)
    try:
        if ROI is not None and len(ROI) > 0:
            rankandsuit(ROI)
    except:
        pass

# Video feed
capture = cv.VideoCapture(0)

# Constant loop*
while True:
    # Set frame to be an image/frame of the video feed
    ret, frame = capture.read()

    # if no frame is detected it retries
    if not ret:
        print("Failed to capture frame. Retrying...")
        continue  # Skip this iteration and continue capturing       

    try:
        # Tries to find and make a square around the card/square
        find_card(frame)
    
    # I low key do not know what this does
    except Exception as e:
        print(f"Error during processing: {e}")
        continue  # Skip this frame and continue with the next
    
    # Break from the while-loop
    if cv.waitKey(20) & 0xFF==ord('q'): 
        break

# Stop capturing from the camera 
capture.release()
# Destroy the windows made
cv.destroyAllWindows()


end = time.time()
ti = end - start
# Print the time it took fro the code to run until the end
print(ti)