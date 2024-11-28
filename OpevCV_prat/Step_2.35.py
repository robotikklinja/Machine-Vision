"""
This code shall take a frame from a video feed (camera) 
and make a picture of the card and make a line .


Made by B.Stokke on 07.11.2024

Updated by:
B.Stokke on 11.11.2024
"""

import cv2 as cv
import numpy as np

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
    
        # Display each card individually 
        cv.imshow(f"Card {i+1}", card_image)
    # Return None if nothing happens (so code doesn't crash)
    cropped_number = None 
    cropped_suit = None 

    # If there are cards in view (the image card_image is use alot here so the code crashes when there are no card/s on in view)
    if len(cards) != 0: 
        gray_card = cv.cvtColor(card_image, cv.COLOR_BGR2GRAY) 

        _, thresh_card = cv.threshold(gray_card, 128, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        cv.imshow("thresh card", thresh_card)

        contours_card, _ = cv.findContours(thresh_card, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        regions = [] 
        for contour in contours:
            # Get bounding box for each contour
            x, y, w, h = cv.boundingRect(contour) 

            # Check if the bounding box is in the top-left region
            if x < (card_image.shape[1] // 8) and y < (card_image.shape[0] // 4):
                regions.append((x, y, w, h))

            if not regions:
                # print("None")
                return None, None

        # Sort regions by their y-coordinate to distinguish number and suit
        regions = sorted(regions, key=lambda r: r[1])


        if len(regions) > 0:
            x, y, w, h = regions[0]  # Assume the first region is the number
            cropped_number = thresh_card[y:y+h, x:x+w]

            # Further trim the cropped number region
            number_contours, _ = cv.findContours(cropped_number, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            if number_contours:
                x2, y2, w2, h2 = cv.boundingRect(number_contours[0])
                cropped_number = cropped_number[y2:y2+h2, x2:x2+w2]

        if len(regions) > 1:
            x, y, w, h = regions[1]  # Assume the second region is the suit
            cropped_suit = thresh_card[y:y+h, x:x+w]

            # Further trim the cropped suit region
            suit_contours, _ = cv.findContours(cropped_suit, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            if suit_contours:
                x2, y2, w2, h2 = cv.boundingRect(suit_contours[0])
                cropped_suit = cropped_suit[y2:y2+h2, x2:x2+w2]

    return cropped_number, cropped_suit

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
