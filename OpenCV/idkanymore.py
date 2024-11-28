import cv2
import cvzone
import numpy as np

def find_cards_and_remove_background(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the image to remove noise and make shapes clearer
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edges image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # List to store detected cards
    cards = []

    # Loop through all contours
    for contour in contours:
        epsilon = 0.05 * cv2.arcLength(contour, True)  # Tolerance for approximating shape
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # If the contour has 4 points (quadrilateral), it may be a card
        if len(approx) == 4 and cv2.contourArea(approx) > 1000:
            cards.append(approx)

    # Create a mask to remove the background
    mask = np.zeros_like(frame)  # Start with a black mask (same size as frame)

    # Fill the detected card contours on the mask with white
    for card in cards:
        cv2.drawContours(mask, [card], -1, (255, 255, 255), -1)  # -1 fills the contour

    # Bitwise AND to isolate the card from the frame using the mask
    result = cv2.bitwise_and(frame, mask)

    # Optionally, fill the background with a specific color (e.g., white)
    result[mask == 0] = (255, 255, 255)  # Background becomes white

    # Display the mask and result
    cv2.imshow("Mask", mask)
    cv2.imshow("Isolated Cards", result)

    return result, cards  # Return the isolated cards image and the contours
