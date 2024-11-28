import cv2 as cv
import numpy as np


def isolate_top_left_number_and_suit(card_image): 
    """
    Isolate and crop the number and suit in the top-left corner of a card image.
    
    :param card_image: 2D card image (numpy array)
    :return: Tuple containing cropped images of the number and the suit
    """
    # Show the original image
    cv.imshow("Original Image", card_image)

    # Convert the image to grayscale
    gray = cv.cvtColor(card_image, cv.COLOR_BGR2GRAY)
    cv.imshow("Gray Image", gray)

    # Apply threshold to isolate the number and suit regions
    _, thresh = cv.threshold(gray, 128, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    cv.imshow("Threshold Image", thresh)

    # Find contours
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Filter contours to find the number and suit in the top-left corner
    regions = []
    for contour in contours:
        # Get bounding box for each contour 
        x, y, w, h = cv.boundingRect(contour)

        # Check if the bounding box is in the top-left region
        if x < (card_image.shape[1] // 10) and y < (card_image.shape[0] // 4):
            regions.append((x, y, w, h))

    if not regions:
        print("No number or suit detected in the top-left corner!")
        return None, None

    # Sort regions by their y-coordinate to distinguish number and suit
    regions = sorted(regions, key=lambda r: r[1])

    # Crop the number and suit regions with padding to ensure they touch edges
    cropped_number = None 
    cropped_suit = None

    if len(regions) > 0:
        x, y, w, h = regions[0]  # Assume the first region is the number
        cropped_number = thresh[y:y+h, x:x+w]

        # Further trim the cropped number region
        number_contours, _ = cv.findContours(cropped_number, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if number_contours:
            x2, y2, w2, h2 = cv.boundingRect(number_contours[0])
            cropped_number = cropped_number[y2:y2+h2, x2:x2+w2]

    if len(regions) > 1:
        x, y, w, h = regions[1]  # Assume the second region is the suit
        cropped_suit = thresh[y:y+h, x:x+w]

        # Further trim the cropped suit region
        suit_contours, _ = cv.findContours(cropped_suit, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if suit_contours:
            x2, y2, w2, h2 = cv.boundingRect(suit_contours[0])
            cropped_suit = cropped_suit[y2:y2+h2, x2:x2+w2]

    return cropped_number, cropped_suit 

# Load a sample card image
# card_image = cv2.imread(r"OpevCV_prat\Photos\HA.jpg")       # This one works
# card_image = cv2.imread(r"OpevCV_prat\Photos\7_of_D.jpg")  # This one don't

capture = cv.VideoCapture(1)

while True:
    # Set frame to be an image/frame of the video feed
    ifTrue, frame = capture.read() 

    # Find and make a square around the card/square
    # and show the results 
    top_left_number_image, top_left_suit_image = isolate_top_left_number_and_suit(frame) 
    
    # Show the results 
    cv.imshow("Top Left Number", top_left_number_image)
    cv.imshow("Top Left Suit", top_left_suit_image) 
    
    # Used to break from the loop
    if cv.waitKey(20) & 0xFF==ord('q'):
        break

# Stop capturing from the camera 
capture.release()

# Destroy the windows made
cv.destroyAllWindows()
