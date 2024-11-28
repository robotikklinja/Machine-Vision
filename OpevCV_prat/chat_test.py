"""
Created 24.10.2024

@author: B.Stokke
"""

import cv2 as cv
import numpy as np


# Define card size and templates for matching
CARD_WIDTH, CARD_HEIGHT = 200, 300

templates = {}  # Load card templates for each rank (A, 2, 3, .., K)

# Find edges through greying the image bluring the image and finding relevent edges:
def preprocess_image(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) #
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    edged = cv.Canny(blur, 50, 150)
    return edged


def find_card_contours(edged):
    contours, _ = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    card_contours = []
    for contour in contours:
        if cv.contourArea(contour) > 1000:
            card_contours.append(contour)
    return card_contours


# Extracts and resizes the card
def get_card(image, contour):
    x, y, w, h = cv.boundingRect(contour)
    card = image[y:y + h, x:x + w]
    return cv.resize(card, (CARD_WIDTH, CARD_HEIGHT))

def match_card(card, templates):
    card_gray = cv.cvtColor(card, cv.COLOR_BGR2GRAY)
    best_match = None
    best_score = float('inf')
    
    for name, template in templates.items():
        template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(card_gray, template_gray, cv.TM_SQDIFF)
        _, score, _, _ = cv.minMaxLoc(result)
        
        # If the new prossesed card is better then the previous card store the new best
        if score < best_score: 
            best_score = score
            best_match = name

    return best_match # Return the best match between the card on borad and the reference cards

capture = cv.VideoCapture(0) # Set the cap to the image seen on the camera on the PC

while True:# Constant loop, only goes out when "break" in used.
    ret, frame = capture.read()
    if not ret:
        break

    edged = preprocess_image(frame)
    contours = find_card_contours(edged)

    for contour in contours:
        card = get_card(frame, contour)
        match = match_card(card, templates)
        x, y, w, h = cv.boundingRect(contour)
        cv.putText(frame, match, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv.imshow('Card Detection', frame) # Show the camera in a windoe called "Card Detection"

    if cv.waitKey(1) & 0xFF == ord('q'): # Wait for key "q" to be pressed
        break # Used to go out of the loop

capture.release()
cv.destroyAllWindows()
