
"""

This code shall be a sum of all related code for a signal code project.

The code is going to do everything so that reference to other .py files are 
not in place because I don't know how to do that. 

Made by B.Stokke on 28.11.2024
"""

import cv2 
import cv2 as cv
import numpy as np


# Converts number in array suits to str
def nr_SUIT_SUIT(nr_suit):
    SUIT = {
        0: "Harts",
        1: "Spades",
        2: "Diamonds",
        3: "Clubs"
    }
    return SUIT

# Converts number in array ranks to str
def nr_RANK_RANK(nr_rank):
    RANK = {
        0: "Ace",
        1: "Two",
        2: "Three",
        3: "Four",
        4: "Five",
        5: "Six",
        6: "Seven",
        7: "Eight",
        8: "Nine",
        9: "Ten",
        10: "Jack",
        11: "Queen",
        12: "King"
    }
    return RANK

# For general resize of things
def resize_to_ref(image, ref_image): 
    width = int(image.shape[1]*0 + ref_image)
    hight = int(image.shape[0]*0 + ref_image)

    dimensions = (width, hight) 

    return cv.resize(image, dimensions, interpolation=cv.INTER_AREA)

# For general resize of things
def resize(image, x_dim, y_dim): 
    width = int(image.shape[1]*0 + x_dim)
    hight = int(image.shape[0]*0 + y_dim)

    dimensions = (width, hight)

    return cv.resize(image, dimensions, interpolation=cv.INTER_AREA)

# Function to rescale the frame of the image
def resize_rank(image, scale=0.75): 
    # There is no reson funciton wise why thre image.shape[1]*0 is there.
    # The only reson why it is there is so that changes is easy and for understanding of code.
    width = int(image.shape[1]*0 + 70) # When frame.shape is 1 we refer to the width
    height = int(image.shape[0]*0 + 125) # When frame.shape is 0 we refer to the height

    dimensions = (width,height) # Define it as dimensions 

    return cv.resize(image, dimensions, interpolation=cv.INTER_AREA)

#Function to rescale the frame of the image
def resize_suit(image, scale=0.75): 
    width = int(image.shape[1]*0 + 70) # When frame.shape is 1 we refer to the width
    height = int(image.shape[0]*0 + 100) # When frame.shape is 0 we refer to the height

    dimensions = (width,height) # Define it as dimensions

    return cv.resize(image, dimensions, interpolation=cv.INTER_AREA)

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
 
        # h_n is the ratio of the total height of the card to the height of the roi mesured (manualy)
        h_n = 3.9 # This isn't good and other methods should be used

        # w_n is the ratio of the total width of the card to the width of the roi mesured (manualy)
        w_n = 5.9 # This isn't good and other methods should be used

        h = warped.shape[0] # Height of the 2D image of the card
        w = warped.shape[1] # Width of the 2D image of the card

        n = round(h/h_n) # n is the height of the ROI in this case
        v = round(w/w_n) # v is the witdh of the ROI in this case
    
        ROI = warped[0:int(n), 0:int(v)]  # Define the ROI & adding "int()" just in case.

        # Display each card individually and numbering the cards using "i"
        cv.imshow(f"Card {i+1}", warped)   
 
        # Display the ROI and numbering the ROI of the card usign "i"
        cv.imshow(f"ROI {i+1}", ROI) 

    # Don't call on the ROI if there are none.
    if len(cards) != 0: 
        rank_image = splitt_img(ROI) 

        # Display the rank of the card
        cv.imshow("Rank", rank_image)

# Returns an image of rank and an image of suit 
def splitt_img(corner):

    height, width = corner.shape

    # There should be a better method to adjust the areal between ROI of rank and suit
    ROI_diff = round(height * 0.1) # guess 10%

    # Define the ROI for Rank in the image "corner"
    ROI_RANK = corner[0:((height//2) + ROI_diff), 0:width]

    ROI_SUIT = corner[((height//2) + ROI_diff): height, 0:width]

    # Make an image to black and white (including gray) 
    # gray = cv.cvtColor(ROI_RANK, cv.COLOR_BGR2GRAY) 
 
    # Highlights the edges in an image 
    _, thresh = cv.threshold(ROI_RANK, 50, 255, cv.THRESH_BINARY) 
 
    # Finds the contours in an image (shapes)
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) 

    # Sort contours by area (largest to smallest) and keep the largest two
    contours = sorted(contours, key=cv.contourArea, reverse=True)[:2] 

    # Ensure the rank is above the suit by sorting by vertical position
    contours = sorted(contours, key=lambda c: cv.boundingRect(c)[1])

    # Extract bounding boxes 
    rank_x, rank_y, rank_w, rank_h = cv.boundingRect(contours[0])  # Rank 
    # suit_x, suit_y, suit_w, suit_h = cv.boundingRect(contours[1])  # Suit 

    # Crop the rank and suit areas 
    rank_img = corner[rank_y:rank_y+rank_h, rank_x:rank_x+rank_w] # Rand Image
    # suit_img = corner[suit_y:suit_y+suit_h, suit_x:suit_x+suit_w] # Suit Image

    return rank_img


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