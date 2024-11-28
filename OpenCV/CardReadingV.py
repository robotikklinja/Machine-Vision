"""
This code shall take a frame from a video feed (camera) 
and make a picture of the card and make an outline of za card.

This code is to experiment with and make the card stand.

Made by B.Stokke on 07.11.2024

Updated by:
B.Stokke & V.Dalisay on 21.11.2024
V.Dalisay on 28.11.2024
"""
import cv2
import cv2 as cv
import numpy as np
import time

# This is just to start taking the time for how much time this code takes to run
start = time.time()

# Function to isolate the suit and the rank from each other
def rankandsuit(corner):
    # make the corner into a grayscale
    gray = cv.cvtColor(corner, cv.COLOR_BGR2GRAY)
    #the height and width of the corner are defined as h and w
    h, w = gray.shape


    diff_h = round(h * 0.1) # 10%
    RANK = gray[0:((h//2)+diff_h), 0:w] # ROI for Rank
    SUIT = gray[((h//2)+diff_h):h, 0:w] # ROI for Suit

    # Get the coordinates of the Rank and Suit regions (for bounding boxes)
    rank_x, rank_y, rank_w, rank_h = 0, 0, w, (h // 2) + diff_h
    suit_x, suit_y, suit_w, suit_h = 0, (h // 2) + diff_h, w, h

    # Draw bounding boxes around Rank and Suit
    cv.rectangle(corner, (rank_x, rank_y), (rank_x + rank_w, rank_y + rank_h), (0, 255, 0), 2)  # Green bounding box for Rank
    cv.rectangle(corner, (suit_x, suit_y), (suit_x + suit_w, suit_y + suit_h), (0, 0, 255), 2)  # Red bounding box for Suit

    # Show the images with the bounding boxes
    cv.imshow('Rank and Suit with Bounding Boxes', corner)
    cv.imshow('rankimg', RANK)
    cv.imshow('suitimg', SUIT)


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
        n, v = h//h_n,w//w_n

        ROI = warped[0:int(n), 0:int(v)]  # Adjust size as needed
    
        # Display each card individually 
        cv.imshow(f"Card {i+1}", warped)
        # Display the corner
        cv.imshow("Corner", ROI)

        if ROI is not None and len(ROI) > 0:
            rankandsuit(ROI)

# Video feed
capture = cv.VideoCapture(1)

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
    if cv2.waitKey(20) & 0xFF==ord('q'): 
        break

# Stop capturing from the camera 
capture.release()
# Destroy the windows made
cv.destroyAllWindows()


end = time.time()
ti = end - start

# Print the time it took fro the code to run until the end
print(ti)