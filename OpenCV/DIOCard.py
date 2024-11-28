import cv2
import numpy as np

# Load image
img = cv2.imread(r'Photos/dos.jpg')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Apply binary thresholding
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Define a ROI: Let's assume the rank and suit are at the top-left corner
x, y, w, h = 50, 50, 100, 150  # You can adjust these values based on your card's layout

# Crop the region from the original image
roi = img[y:y+h, x:x+w]

# Find contours in the thresholded image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Loop over contours and filter based on area or shape (optional)
for contour in contours:
    # Approximate the contour to a polygon
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    # You can filter out small or irrelevant contours based on area or shape
    if cv2.contourArea(contour) > 100:
        # Draw the contour (you could also crop this region)
        cv2.drawContours(roi, [approx], -1, (0, 255, 0), 3)

cv2.imshow('Rank and Suit ROI', roi)
cv2.waitKey(0)
cv2.destroyAllWindows()