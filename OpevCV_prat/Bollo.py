import cv2 as cv
import numpy as np

def splitt_img2(corner):

    ROI = corner[(corner.shape[1]//2):(corner.shape[0]//2), corner.shape[1]:corner.shape[0]]

    # Make an image to black and white (including gray) 
    gray = cv.cvtColor(ROI, cv.COLOR_BGR2GRAY)
 
    # Highlights the edges in an image
    _, thresh = cv.threshold(gray, 50, 255, cv.THRESH_BINARY) 
 
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

def splitt_img(corner):

    # Make an image to black and white (including gray)
    gray = cv.cvtColor(corner, cv.COLOR_BGR2GRAY)
    cv.imshow("gray", gray)
 
    # Highlights the edges in an image
    _, thresh = cv.threshold(gray, 50, 255, cv.THRESH_BINARY) 
    cv.imshow("thresh", thresh)
 
    # Finds the contours in an image (shapes)
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Sort contours by area (largest to smallest) and keep the largest two 
    contours = sorted(contours, key=cv.contourArea, reverse=True)[:2]

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)

        aspect_raio = w / h
        if aspect_raio < 1:
            rank_x, rank_y, rank_w, rank_h = x, y, w, h
            break
        else:
            print("Rank not found.")
            return

    # Crop the rank and suit areas 
    rank_img = corner[rank_y:rank_y+rank_h, rank_x:rank_x+rank_w] # Rand Image
    # suit_img = corner[suit_y:suit_y+suit_h, suit_x:suit_x+suit_w] # Suit Image

    return rank_img

path = r"OpevCV_prat\Photos\2_Cc.jpg"

img = cv.imread(path)

rank = splitt_img2(img)

print(img.shape[1], img.shape[0], rank.shape[1], rank.shape[0])

cv.imshow("ori", img)
cv.imshow("rank", rank)

cv.waitKey(0)
cv.destroyAllWindows()