"""
This code shall take a frame from a video feed (camera) 
and make a picture of the card and make a line .


Made by B.Stokke on 07.11.2024

Updated by:
B.Stokke on 11.11.2024
"""

import cv2 as cv
import numpy as np

def extract_rank_and_suit(card_image):
    """
    Extract the rank and suit from the card image using predefined ROIs.
    """
    # Convert card image to grayscale
    gray_card = cv.cvtColor(card_image, cv.COLOR_BGR2GRAY)
    
    # Threshold to make it binary for easier ROI extraction
    _, thresh = cv.threshold(gray_card, 127, 255, cv.THRESH_BINARY_INV)
    
    # Define ROI positions for rank and suit (adjust these values based on your card layout)
    h, w = card_image.shape[:2] 
    rank_roi = thresh[:int(0.4 * h), :int(0.3 * w)]  # Top-left corner for rank
    suit_roi = thresh[int(0.4 * h):int(0.6 * h), :int(0.3 * w)]  # Below rank for suit
    
    # Display the extracted rank and suit for debugging 
    cv.imshow("Rank", rank_roi)
    cv.imshow("Suit", suit_roi) 

    # Return the ROIs (you can integrate OCR or image matching here later)
    return rank_roi, suit_roi

def find_card(img):
    # Make an image to black and white (including gray)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.imshow("gray", gray)

    # blur the image to make shapes more clear by take away any details
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    # cv.imshow("blurred", blurred)

    # Highlights the edges in an image
    edges = cv.Canny(blurred, 50, 150)
    cv.imshow("edges", edges) 

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
        card_image = cv.warpPerspective(img, M, (maxWidth, maxHeight))
    
        # Extract and display rank and suit
        rank_roi, suit_roi = extract_rank_and_suit(card_image)

        # Display each card individually 
        cv.imshow(f"Card {i+1}", card_image)


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
