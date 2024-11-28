"""
This code is going to be a play ground to comapre two images 
using Absolute Difference. 

Made by B.Stokke on 13.11.2024
"""

import cv2 as cv
import numpy as np

def image_score(imageA, imageB):
    if imageA.shape != imageB.shape:
        raise ValueError("Images must have the same dimensions!")

# Load images in grayscale mode
Clubs = cv.imread(r'OpevCV_prat\Photos\Clubs.jpg', cv.IMREAD_GRAYSCALE)
cv.imshow("Image A", Clubs)

Dimaond = cv.imread(r'OpevCV_prat\Photos\Diamonds.jpg', cv.IMREAD_GRAYSCALE)
cv.imshow("Image B", Dimaond)

# Compute absolute difference
diff = cv.absdiff(Clubs, Dimaond)

# Optional: Display the difference
cv.imshow("Difference", diff)
cv.waitKey(0)
cv.destroyAllWindows()
