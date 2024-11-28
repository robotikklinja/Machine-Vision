"""
This code shall take a frame from a video feed (camera) 
and make a picture of the card in the frame.

Made by B.Stokke on 07.11.2024
"""

import cv2 as cv
import numpy as np

def find_card(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    blurred = cv.GaussianBlur(gray, (5, 5), 0)

    edges = cv.Canny(blurred, 50, 150)

    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    cards = []
    for contour in contours:

        epsilon = 0.02 * cv.arcLength(contour, True)

        approx = cv.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4 and cv.contourArea(approx) > 1000:
            cards.append(approx)
    
    output_image = img.copy()
    for card in cards:
        cv.drawContours(output_image, [card], -1, (255, 0, 0), 2)
    
    copy_img = img.copy()
    for card in cards:
        cv.drawContours(copy_img, [card], -1, (0, 255, 0), 2)# Color isn't RGB, but BGR

    cv.imshow("Detected Card", copy_img)


# Example of a frame
image = cv.imread(r'OpevCV_prat\WIN_20241107_10_24_40_Pro.jpg')

# Show the result
find_card(image)
cv.waitKey(0)
cv.destroyAllWindows()
