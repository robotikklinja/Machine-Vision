import cv2 as cv
import numpy as np

def find_rank_region(corner):
    # Convert the image to grayscale
    gray = cv.cvtColor(corner, cv.COLOR_BGR2GRAY)

    # Apply thresholding to isolate text-like regions
    _, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV)

    # Find contours in the thresholded image
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Look for contours in the top portion of the image (the rank is typically located here)
    rank_contours = []
    h, w = gray.shape
    for contour in contours:
        # Filter out small contours (ignoring noise and irrelevant shapes)
        if cv.contourArea(contour) > 500:  # Area threshold can be adjusted
            # Get the bounding box for each contour
            x, y, w_c, h_c = cv.boundingRect(contour)

            # Focus only on the upper part of the card (where the rank is located)
            if y < h // 2:  # Assuming rank is in the upper half of the card
                rank_contours.append((x, y, w_c, h_c))

    # If rank contours are found, draw a box around the largest one (likely the rank)
    if rank_contours:
        # Sort by area to find the most likely rank region
        rank_contours = sorted(rank_contours, key=lambda x: x[2]*x[3], reverse=True)
        x, y, w_c, h_c = rank_contours[0]  # Get the largest contour (likely the rank)
        return x, y, w_c, h_c
    else:
        return None

def find_card(img):
    # Convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Blur to enhance edges
    blurred = cv.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edges = cv.Canny(blurred, 50, 150)

    # Find contours (shapes)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    cards = []
    for contour in contours:
        epsilon = 0.02 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4 and cv.contourArea(approx) > 1000:
            cards.append(approx)

    copy_image = img.copy()
    for card in cards:
        cv.drawContours(copy_image, [card], -1, (0, 255, 0), 2)
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
            warped = cv.rotate(warped, cv.ROTATE_90_CLOCKWISE)

        # Now dynamically find the rank region (bounding box)
        rank_box = find_rank_region(warped)
        if rank_box:
            x, y, w_c, h_c = rank_box
            cv.rectangle(warped, (x, y), (x + w_c, y + h_c), (0, 0, 255), 2)  # Draw red box around the rank

        cv.imshow(f"Card with Rank Box {i+1}", warped)
        
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