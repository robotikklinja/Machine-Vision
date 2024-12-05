import cv2
import cv2 as cv
import numpy as np
import time

# This is just to start taking the time for how much time this code takes to run
start = time.time()

# Function to isolate the suit and the rank from each other
def rankandsuit(corner):
    # Convert the image to grayscale
    gray = cv.cvtColor(corner, cv.COLOR_BGR2GRAY)
    h, w = gray.shape

    # Calculate the region for the rank (top part of the card)
    diff_h = round(h * 0.1)  # You can adjust this if the rank area is larger or smaller
    RANK = gray[0:((h // 2) + diff_h), 0:w]  # The rank area is typically the top half

    # Define the coordinates for the rank bounding box
    rank_x, rank_y, rank_w, rank_h = 0, 0, w, (h // 2) + diff_h

    # Draw the box only around the rank area (no suit area included)
    cv.rectangle(corner, (rank_x, rank_y), (rank_x + rank_w, rank_y + rank_h), (0, 255, 0), 2)  # Green box

    # Optionally display the rank region (you can hide this in production)
    cv.imshow('Rank', RANK)
    cv.imshow('Card with Rank Box', corner)

def find_card(img):
    # Convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Blur to enhance edges
    blurred = cv.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edges = cv.Canny(blurred, 50, 150)

    # Find contours (shapes)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # List to store potential card contours
    cards = []
    for contour in contours:
        epsilon = 0.02 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4 and cv.contourArea(approx) > 1000:  # Filter by area
            cards.append(approx)
        
    # Make a copy of the original image to draw contours
    copy_image = img.copy()
    for card in cards:
        cv.drawContours(copy_image, [card], -1, (0, 255, 0), 2)  # Draw contour of card
    cv.imshow("Detected Card", copy_image)

    for i, card in enumerate(cards):
        pts = card.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # Calculate the width and height of the card
        widthA = np.sqrt(((rect[2][0] - rect[3][0]) ** 2) + ((rect[2][1] - rect[3][1]) ** 2))
        widthB = np.sqrt(((rect[1][0] - rect[0][0]) ** 2) + ((rect[1][1] - rect[0][1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((rect[1][0] - rect[2][0]) ** 2) + ((rect[1][1] - rect[2][1]) ** 2))
        heightB = np.sqrt(((rect[0][0] - rect[3][0]) ** 2) + ((rect[0][1] - rect[3][1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst_pts = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv.getPerspectiveTransform(rect, dst_pts)
        warped = cv.warpPerspective(img, M, (maxWidth, maxHeight))

        if warped.shape[1] > warped.shape[0]:
            warped = cv.rotate(warped, cv.ROTATE_90_CLOCKWISE)  # Make the card stand

        # Define the region for rank extraction (top-left corner)
        h, w = warped.shape[0], warped.shape[1]
        n, v = h // 4, w // 6  # Adjust size for rank extraction
        ROI = warped[0:int(n), 0:int(v)]  # Extract rank area (you can adjust this)

        # Display the card and the rank-only box
        cv.imshow(f"Card {i+1}", warped)

        # Draw the box around the rank region
        rank_x, rank_y = 10, 10  # Define position for the box (adjust as necessary)
        box_width, box_height = 60, 30  # Define the box size for the rank
        cv.rectangle(warped, (rank_x, rank_y), (rank_x + box_width, rank_y + box_height), (0, 0, 255), 2)  # Red box

        # Show the result with the rank-only box
        cv.imshow(f"Card with Rank Box {i+1}", warped)

        # Optionally, show the corner
        if ROI is not None and len(ROI) > 0:
            rankandsuit(ROI)


def find_card(img):
    # Convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Blur to enhance edges
    blurred = cv.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edges = cv.Canny(blurred, 50, 150)

    # Find contours (shapes)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # List to store potential card contours
    cards = []
    for contour in contours:
        epsilon = 0.02 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4 and cv.contourArea(approx) > 1000:  # Filter by area
            cards.append(approx)
        
    # Make a copy of the original image to draw contours
    copy_image = img.copy()
    for card in cards:
        cv.drawContours(copy_image, [card], -1, (0, 255, 0), 2)  # Draw contour of card
    cv.imshow("Detected Card", copy_image)

    for i, card in enumerate(cards):
        pts = card.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # Calculate the width and height of the card
        widthA = np.sqrt(((rect[2][0] - rect[3][0]) ** 2) + ((rect[2][1] - rect[3][1]) ** 2))
        widthB = np.sqrt(((rect[1][0] - rect[0][0]) ** 2) + ((rect[1][1] - rect[0][1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((rect[1][0] - rect[2][0]) ** 2) + ((rect[1][1] - rect[2][1]) ** 2))
        heightB = np.sqrt(((rect[0][0] - rect[3][0]) ** 2) + ((rect[0][1] - rect[3][1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst_pts = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv.getPerspectiveTransform(rect, dst_pts)
        warped = cv.warpPerspective(img, M, (maxWidth, maxHeight))

        if warped.shape[1] > warped.shape[0]:
            warped = cv.rotate(warped, cv.ROTATE_90_CLOCKWISE)  # Make the card stand

        # Define the region for rank extraction (top-left corner)
        h, w = warped.shape[0], warped.shape[1]
        n, v = h // 4, w // 6  # Adjust size for rank extraction
        ROI = warped[0:int(n), 0:int(v)]  # Extract rank area (you may adjust this)

        # Display each card
        cv.imshow(f"Card {i+1}", warped)

        # Draw a box around the rank area (without text)
        rank_x, rank_y = 10, 10  # Define position for the box
        box_width, box_height = 60, 30  # Define box size for the rank
        cv.rectangle(warped, (rank_x, rank_y), (rank_x + box_width, rank_y + box_height), (0, 0, 255), 2)  # Red box

        # Show the result with the box around the rank
        cv.imshow(f"Card with Rank Box {i+1}", warped)

        # Optionally, show the corner
        if ROI is not None and len(ROI) > 0:
            rankandsuit(ROI)

# Video feed
capture = cv.VideoCapture(0)

# Constant loop*
while True:
    # Set frame to be an image/frame of the video feed
    ret, frame = capture.read()

    # if no frame is detected it retries
    if not ret:
        print("Failed to capture frame. Retrying...")
        continue  # Skip this iteration and continue capturing       

    try:
        # Tries to find and make a square around the card/square
        find_card(frame)
    
    # I low key do not know what this does
    except Exception as e:
        print(f"Error during processing: {e}")
        continue  # Skip this frame and continue with the next
    
    # Break from the while-loop
    if cv2.waitKey(20) & 0xFF==ord('q'): 
        break

# Stop capturing from the camera 
capture.release()
# Destroy the windows made
cv.destroyAllWindows()

end = time.time()
ti = end - start

# Print the time it took fro the code to run until the end
print(ti)