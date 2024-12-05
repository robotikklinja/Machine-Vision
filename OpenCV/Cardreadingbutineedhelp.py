import cv2 as cv
import numpy as np
import time

# Add a dictionary to store card windows
card_windows = {}

# Function to isolate the suit and the rank from each other
def rankandsuit(corner):

    #the height and width of the corner are defined as h and w
    h, w, _ = corner.shape

    # make the corner into a grayscale
    gray = cv.cvtColor(corner, cv.COLOR_BGR2GRAY)

    # round the height of the corner of the card to 10% and make it into a diff_h variable, so that the rank and suit are separated properly.
    diff_h = round(h * 0.1) # 10%

    # this is to divide the rank and the suit. It uses the rank 
    rank_height = (h//2) + diff_h

    # divide the grayscaled corner into the rank and the suit
    grayrank = gray[0:((h//2)+diff_h), 0:w] # ROI for Rank
    graysuit = gray[((h//2)+diff_h):h, 0:w] # ROI for Suit

    # # Get the coordinates of the Rank and Suit regions (for bounding boxes)
    # rank_x, rank_y, rank_w, rank_h = 0, 0, w, (h // 2) + diff_h
    # suit_x, suit_y, suit_w, suit_h = 0, (h // 2) + diff_h, w, h

    # # Draw bounding boxes around Rank and Suit
    # cv.rectangle(corner, (rank_x, rank_y), (rank_x + rank_w, rank_y + rank_h), (0, 255, 0), 2)  # Green bounding box for Rank
    # cv.rectangle(corner, (suit_x, suit_y), (suit_x + suit_w, suit_y + suit_h), (0, 0, 255), 2)  # Red bounding box for Suit

    # # Show the images with the bounding boxes
    # cv.imshow('Rank and Suit with Bounding Boxes', corner)

    # blur the images so that it dont got too much noise
    blurrank = cv.GaussianBlur(grayrank, (1,1), cv.BORDER_DEFAULT)
    blursuit = cv.GaussianBlur(graysuit, (1,1), cv.BORDER_DEFAULT)

    # turns the crayscaled images into an image full of edges
    R_edge = cv.Canny(blurrank, 50, 150)
    S_edge = cv.Canny(blursuit, 50, 150)

    # Find contours to help with the bounding of the rank and suit
    R_contour, _ = cv.findContours(R_edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    S_contour, _ = cv.findContours(S_edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    #Set a bounding boxx for both the rank and the suit of the card
    rank_x, rank_y, rank_w, rank_h = cv.boundingRect(R_contour[0])
    suit_x, suit_y, suit_w, suit_h = cv.boundingRect(S_contour[0])

    rank_img = corner[rank_y : rank_y + rank_h, rank_x : rank_x+ rank_w] # Rank img
    suit_img = corner[suit_y + rank_height : rank_height + suit_y + suit_h, suit_x : suit_x + suit_w] # Suit img

    cv.imshow('rankimg', rank_img)
    cv.imshow('suitimg', suit_img)  

    def rescaleFrame(frame, scale=5): #Function to rescale the frame of the window
        width = int(frame.shape[1] * scale) # when frame.shape is 1 we refer to the width
        height = int(frame.shape[0] * scale) # when frame.shape is 0 we refer to the height
        dimensions = (width, height) # define it as dimensions

        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    resized_rank_img = rescaleFrame(rank_img) # The new image is now called resized_rank_img
    cv.imshow('resized rank image', resized_rank_img) # show the resized image
    resized_suit_img = rescaleFrame(suit_img) # The new image is now called resized_suit_img
    cv.imshow('resized suit image', resized_suit_img) # show the resized image

    return rank_img, suit_img

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

    copy_image = img.copy()
    for card in cards:
        cv.drawContours(copy_image, [card], -1, (0, 255, 0), 2)
    cv.imshow("Detected Card", copy_image)

    current_card_windows = []  # Store currently visible card windows

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

        h_n, w_n = 4, 6.2
        h, w = warped.shape[0], warped.shape[1]
        n, v = h // h_n, w // w_n
        ROI = warped[0:int(n), 0:int(v)]

        card_window_name = f"Card {i+1}"
        current_card_windows.append(card_window_name)  # Store the card window name

        # Check if the window already exists or needs to be opened
        if card_window_name not in card_windows:
            cv.imshow(card_window_name, warped)  # Open the card window
            card_windows[card_window_name] = warped  # Store the window reference

        # Display the corner window
        cv.imshow("Corner", ROI)

        try:
            if ROI is not None and len(ROI) > 0:
                rankandsuit(ROI)
        except:
            pass

    # Close any windows for cards that are no longer visible
    for card_window_name in list(card_windows.keys()):
        if card_window_name not in current_card_windows:

            cv.destroyWindow(card_window_name)  # Close the window for the removed card
            del card_windows[card_window_name]  # Remove from the dictionary

#sjekke hvor lang tid som har gått siden kort ikke har blitt sett
# Hvis tid = for mye do delete window :(

# Video feed
capture = cv.VideoCapture(0)

while True:
    ret, frame = capture.read()

    if not ret:
        print("Failed to capture frame. Retrying...")
        continue

    try:
        find_card(frame)
    
    except Exception as e:
        print(f"Error during processing: {e}")
        continue

    if cv.waitKey(20) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()