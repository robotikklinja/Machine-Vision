"""
This code if going to input data images and convert them into
images that is better for the use I am going to do with them.

There are 4 images of each card and there is 52 different cards (not including JOKER)
Therefore it is 208 images + the 4 for JOKER

I start with an array that I'm going to process to get a 2D* image
from the images in the array input.

Made by: B.Stokke on 30.01.2025
Updated on:

06.02.2025 by B.Stokke
13.03.2025 by B.Stokke
"""


import cv2
import numpy as np
import os

def get_folder_name(fold_count):
    folder_name = {
        1: "processed_10Cs",
        2: "processed_2Cs",
        3: "processed_3Cs",
        4: "processed_4Cs",
        5: "processed_5Cs",
        6: "processed_6Cs",
        7: "processed_7Cs",
        8: "processed_8Cs",
        9: "processed_9Cs",
        10: "processed_ACs",
        11: "processed_JCs",
        12: "processed_KCs",
        13: "processed_QCs",
        14: "processed_10Ds",
        15: "processed_2Ds",
        16: "processed_3Ds",
        17: "processed_4Ds",
        18: "processed_5Ds",
        19: "processed_6Ds",
        20: "processed_7Ds",
        21: "processed_8Ds",
        22: "processed_9Ds",
        23: "processed_ADs",
        24: "processed_JDs",
        25: "processed_KDs",
        26: "processed_QDs",
        27: "processed_10Hs",
        28: "processed_2Hs",
        29: "processed_3Hs",
        30: "processed_4Hs",
        31: "processed_5Hs",
        32: "processed_6Hs",
        33: "processed_7Hs",
        34: "processed_8Hs",
        35: "processed_9Hs",
        36: "processed_AHs",
        37: "processed_JHs",
        38: "processed_KHs",
        39: "processed_QHs",
        40: "processed_10Ss",
        41: "processed_2Ss",
        42: "processed_3Ss",
        43: "processed_4Ss",
        44: "processed_5Ss",
        45: "processed_6Ss",
        46: "processed_7Ss",
        47: "processed_8Ss",
        48: "processed_9Ss",
        49: "processed_ASs",
        50: "processed_JSs",
        51: "processed_KSs",
        52: "processed_QSs"}
    return  folder_name.get(fold_count, "Error in get_folder_name function")

# A function that finds cards and makes a line around it
def process(OG_img, ref_path):
    # cv2.imshow("OG iamge", img)
    
    # Get the OG height and width of the image
    height, width, _ = OG_img.shape 
    # there might be a problem with the "_". Take it a way if the 
    # image has no color. If not it needs to be there to prevent an error

    img = OG_img.copy()
    
    PROCESS_HEIGHT = 300 # set the processed height
    PROCESS_WIDTH = 500 # set the processed width

    if "003" in ref_path: # uf the image has a weird background

        # ROI of the processed image if the image has a "003" in the path name
        ROI = OG_img[500:2100, 1200:2500]
        # cv2.imshow("ROI", ROI)
        img = ROI.copy()

    # Resize the image so that I can udnerstand what happens in the process
    img = cv2.resize(img, (PROCESS_WIDTH, PROCESS_HEIGHT))
    cv2.imshow("image", img) # shoe the image "img"

    # Make an image to black and white (including gray)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray", gray)

    # blur the image to make shapes more clear by take away any details
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # cv2.imshow("Blur", blurred)

    # Highlights the edges in an image
    edges = cv2.Canny(blurred, 50, 150)
    cv2.imshow("Edges", edges)

    # Finds the contours in an image (shapes)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Make an array called cards
    cards = []
    for contour in contours:  # looks for shapes that have 4 sides (cards)

        # Tolerance for how accurate the shape can be 2% (camera is not perfect)
        epsilon = 0.02 * cv2.arcLength(contour, True)

        # A list of points for the shape 
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # If any shapes that have 4 corners (points), then add the points of the shape in cards
        if len(approx) == 4 and cv2.contourArea(approx) > 1000:  # not too small shape
            cards.append(approx)  # Add approx to the array cards

    # Make a copy of the original image
    copy_image = img.copy()
    for card in cards:  # Draw a line through the points to a shape, that has been added above
        cv2.drawContours(copy_image, [card], -1, (0, 255, 0), 2)  # the order is in BGR
        cv2.imshow("card", copy_image)

    # Perspective transform to isolate each card
    if not contours: # Check if the list of contours are empty
        for i, card in enumerate(cards):
            # Get the bounding box coordinates for each card
            pts = card.reshape(4, 2)

            # Sort the points to order them as top-left, top-right, bottom-right, bottom-left
            # (Necessary for perspective transform to work properly)
            rect = np.zeros((4, 2), dtype="float32")
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]

            # Compute the width and height of the card (max)
            widthA = np.sqrt(((rect[2][0] - rect[3][0]) ** 2) + ((rect[2][1] - rect[3][1]) ** 2))
            widthB = np.sqrt(((rect[1][0] - rect[0][0]) ** 2) + ((rect[1][1] - rect[0][1]) ** 2))
            maxWidth = max(int(widthA), int(widthB))

            heightA = np.sqrt(((rect[1][0] - rect[2][0]) ** 2) + ((rect[1][1] - rect[2][1]) ** 2))
            heightB = np.sqrt(((rect[0][0] - rect[3][0]) ** 2) + ((rect[0][1] - rect[3][1]) ** 2))
            maxHeight = max(int(heightA), int(heightB))

            # Define the destination points for the "flattened" card
            dst_pts = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype="float32")

            # Compute the perspective transform matrix and apply it
            M = cv2.getPerspectiveTransform(rect, dst_pts)
            warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))

            # Make the image stand (long side is vertical)
            if warped.shape[1] < warped.shape[0]:  # Check if the width is longer than hight
                warped = cv2.rotate(warped, cv2.ROTATE_90_CLOCKWISE)  # Rotate image (clockwise)

            # cv2.imshow(f"Card", warped)
            # return warped
        try:
            cv2.imshow("Warped", warped)
            return warped
        except:
            print("the image is not gOOd :(")
            return None
    
        # Image that have been porcessed, it is now 2D and standing

# an array with all the relative paths for the images that are going to be prossesed (not the joker/wild)
images = [
    r"OpevCV_prat\playing-cards-master\img\cards-[C0]-001.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C0]-002.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C0]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C2]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C2]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C2]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C3]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C3]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C3]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C4]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C4]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C4]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C5]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C5]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C5]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C6]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C6]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C6]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C7]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C7]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C7]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C8]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C8]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C8]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C9]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C9]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C9]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CA]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CA]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CA]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CJ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CJ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CJ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CK]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CK]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CK]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CQ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CQ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CQ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D0]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D0]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D0]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D2]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D2]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D2]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D3]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D3]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D3]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D4]-001.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[D4]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D4]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D5]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D5]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D5]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D6]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D6]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D6]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D7]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D7]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D7]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D8]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D8]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D8]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D9]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D9]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D9]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DA]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DA]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DA]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DJ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DJ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DJ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DK]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DK]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DK]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DQ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DQ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DQ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H0]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H0]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H0]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H2]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H2]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H2]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H3]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H3]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H3]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H4]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H4]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H4]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H5]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H5]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H5]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H6]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H6]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H6]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H7]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H7]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H7]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H8]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H8]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H8]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H9]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H9]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H9]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HA]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HA]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HA]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HJ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HJ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HJ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HK]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HK]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HK]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HQ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HQ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HQ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S0]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S0]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S0]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S2]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S2]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S2]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S3]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S3]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S3]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S4]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S4]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S4]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S5]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S5]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S5]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S6]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S6]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S6]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S7]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S7]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S7]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S8]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S8]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S8]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S9]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S9]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S9]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SA]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SA]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SA]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SJ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SJ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SJ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SK]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SK]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SK]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SQ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SQ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SQ]-004.jpg"]

try_images = [r"OpevCV_prat\playing-cards-master\img\cards-[C4]-001.jpg", r"OpevCV_prat\playing-cards-master\img\cards-[C0]-002.jpg", r"OpevCV_prat\playing-cards-master\img\cards-[C0]-003.jpg"]
immg = [r"OpevCV_prat\playing-cards-master\img\cards-[C4]-003.jpg"] #OpevCV_prat\Photos\cat.jpg
# OpevCV_prat\playing-cards-master\img\cards-[C4]-003.jpg
# OpevCV_prat\playing-cards-master\img\cards-[C2]-003.jpg

# Define output directory and create it if it doesn't exist
main_folder = "processed_images"
if not os.path.exists(main_folder):
    os.makedirs(main_folder)


if True:
    output_folder_10C = "processed_10Cs"
    if not os.path.exists(output_folder_10C):
        os.makedirs(os.path.join(main_folder, output_folder_10C), exist_ok=True)

    output_folder_2C = "processed_2Cs"
    if not os.path.exists(output_folder_2C):
        os.makedirs(os.path.join(main_folder, output_folder_2C), exist_ok=True)

    output_folder_3C = "processed_3Cs"
    if not os.path.exists(output_folder_3C):
        os.makedirs(os.path.join(main_folder, output_folder_3C), exist_ok=True)
    
    output_folder_4C = "processed_4Cs"
    if not os.path.exists(output_folder_4C):
        os.makedirs(os.path.join(main_folder, output_folder_4C), exist_ok=True)
    
    output_folder_5C = "processed_5Cs"
    if not os.path.exists(output_folder_5C):
        os.makedirs(os.path.join(main_folder, output_folder_5C), exist_ok=True)
    
    output_folder_6C = "processed_6Cs"
    if not os.path.exists(output_folder_6C):
        os.makedirs(os.path.join(main_folder, output_folder_6C), exist_ok=True)

    output_folder_7C = "processed_7Cs"
    if not os.path.exists(output_folder_7C):
        os.makedirs(os.path.join(main_folder, output_folder_7C), exist_ok=True)
    
    output_folder_8C = "processed_8Cs"
    if not os.path.exists(output_folder_8C):
        os.makedirs(os.path.join(main_folder, output_folder_8C), exist_ok=True)
    
    output_folder_9C = "processed_9Cs"
    if not os.path.exists(output_folder_9C):
        os.makedirs(os.path.join(main_folder, output_folder_9C), exist_ok=True)
    
    output_folder_AC = "processed_ACs"
    if not os.path.exists(output_folder_AC):
        os.makedirs(os.path.join(main_folder, output_folder_AC), exist_ok=True)
    
    output_folder_JC = "processed_JCs"
    if not os.path.exists(output_folder_JC):
        os.makedirs(os.path.join(main_folder, output_folder_JC), exist_ok=True)
    
    output_folder_KC = "processed_KCs"
    if not os.path.exists(output_folder_KC):
        os.makedirs(os.path.join(main_folder, output_folder_KC), exist_ok=True)

    output_folder_QC = "processed_QCs"
    if not os.path.exists(output_folder_QC):
        os.makedirs(os.path.join(main_folder, output_folder_QC), exist_ok=True)

    output_folder_10D = "processed_10Ds"
    if not os.path.exists(output_folder_10D):
        os.makedirs(os.path.join(main_folder, output_folder_10D), exist_ok=True)

    output_folder_2D = "processed_2Ds"
    if not os.path.exists(output_folder_2D):
        os.makedirs(os.path.join(main_folder, output_folder_2D), exist_ok=True)
    
    output_folder_3D = "processed_3Ds"
    if not os.path.exists(output_folder_3D):
        os.makedirs(os.path.join(main_folder, output_folder_3D), exist_ok=True)
    
    output_folder_4D = "processed_4Ds"
    if not os.path.exists(output_folder_4D):
        os.makedirs(os.path.join(main_folder, output_folder_4D), exist_ok=True)
    
    output_folder_5D = "processed_5Ds"
    if not os.path.exists(output_folder_5D):
        os.makedirs(os.path.join(main_folder, output_folder_5D), exist_ok=True)
    
    output_folder_6D = "processed_6Ds"
    if not os.path.exists(output_folder_6D):
        os.makedirs(os.path.join(main_folder, output_folder_6D), exist_ok=True)

    output_folder_7D = "processed_7Ds"
    if not os.path.exists(output_folder_7D):
        os.makedirs(os.path.join(main_folder, output_folder_7D), exist_ok=True)
    
    output_folder_8D = "processed_8Ds"
    if not os.path.exists(output_folder_8D):
        os.makedirs(os.path.join(main_folder, output_folder_8D), exist_ok=True)
    
    output_folder_9D = "processed_9Ds"
    if not os.path.exists(output_folder_9D):
        os.makedirs(os.path.join(main_folder, output_folder_9D), exist_ok=True)
    
    output_folder_AD = "processed_ADs"
    if not os.path.exists(output_folder_AD):
        os.makedirs(os.path.join(main_folder, output_folder_AD), exist_ok=True)
    
    output_folder_JD = "processed_JDs"
    if not os.path.exists(output_folder_JD):
        os.makedirs(os.path.join(main_folder, output_folder_JD), exist_ok=True)
    
    output_folder_KD = "processed_KDs"
    if not os.path.exists(output_folder_KD):
        os.makedirs(os.path.join(main_folder, output_folder_KD), exist_ok=True)

    output_folder_QD = "processed_QDs"
    if not os.path.exists(output_folder_QD):
        os.makedirs(os.path.join(main_folder, output_folder_QD), exist_ok=True)
    
    output_folder_10H = "processed_10Hs"
    if not os.path.exists(output_folder_10H):
        os.makedirs(os.path.join(main_folder, output_folder_10H), exist_ok=True)

    output_folder_2H = "processed_2Hs"
    if not os.path.exists(output_folder_2H):
        os.makedirs(os.path.join(main_folder, output_folder_2H), exist_ok=True)
    
    output_folder_3H = "processed_3Hs"
    if not os.path.exists(output_folder_3H):
        os.makedirs(os.path.join(main_folder, output_folder_3H), exist_ok=True)
    
    output_folder_4H = "processed_4Hs"
    if not os.path.exists(output_folder_4H):
        os.makedirs(os.path.join(main_folder, output_folder_4H), exist_ok=True)
    
    output_folder_5H = "processed_5Hs"
    if not os.path.exists(output_folder_5H):
        os.makedirs(os.path.join(main_folder, output_folder_5H), exist_ok=True)
    
    output_folder_6H = "processed_6Hs"
    if not os.path.exists(output_folder_6H):
        os.makedirs(os.path.join(main_folder, output_folder_6H), exist_ok=True)

    output_folder_7H = "processed_7Hs"
    if not os.path.exists(output_folder_7H):
        os.makedirs(os.path.join(main_folder, output_folder_7H), exist_ok=True)
    
    output_folder_8H = "processed_8Hs"
    if not os.path.exists(output_folder_8H):
        os.makedirs(os.path.join(main_folder, output_folder_8H), exist_ok=True)
    
    output_folder_9H = "processed_9Hs"
    if not os.path.exists(output_folder_9H):
        os.makedirs(os.path.join(main_folder, output_folder_9H), exist_ok=True)
    
    output_folder_AH = "processed_AHs"
    if not os.path.exists(output_folder_AH):
        os.makedirs(os.path.join(main_folder, output_folder_AH), exist_ok=True)
    
    output_folder_JH = "processed_JHs"
    if not os.path.exists(output_folder_JH):
        os.makedirs(os.path.join(main_folder, output_folder_JH), exist_ok=True)
    
    output_folder_KH = "processed_KHs"
    if not os.path.exists(output_folder_KH):
        os.makedirs(os.path.join(main_folder, output_folder_KH), exist_ok=True)

    output_folder_QH = "processed_QHs"
    if not os.path.exists(output_folder_QH):
        os.makedirs(os.path.join(main_folder, output_folder_QH), exist_ok=True)
    
    output_folder_10S = "processed_10Ss"
    if not os.path.exists(output_folder_10S):
        os.makedirs(os.path.join(main_folder, output_folder_10S), exist_ok=True)

    output_folder_2S = "processed_2Ss"
    if not os.path.exists(output_folder_2S):
        os.makedirs(os.path.join(main_folder, output_folder_2S), exist_ok=True)
    
    output_folder_3S = "processed_3Ss"
    if not os.path.exists(output_folder_3S):
        os.makedirs(os.path.join(main_folder, output_folder_3S), exist_ok=True)
    
    output_folder_4S = "processed_4Ss"
    if not os.path.exists(output_folder_4S):
        os.makedirs(os.path.join(main_folder, output_folder_4S), exist_ok=True)
    
    output_folder_5S = "processed_5Ss"
    if not os.path.exists(output_folder_5S):
        os.makedirs(os.path.join(main_folder, output_folder_5S), exist_ok=True)
    
    output_folder_6S = "processed_6Ss"
    if not os.path.exists(output_folder_6S):
        os.makedirs(os.path.join(main_folder, output_folder_6S), exist_ok=True)

    output_folder_7S = "processed_7Ss"
    if not os.path.exists(output_folder_7S):
        os.makedirs(os.path.join(main_folder, output_folder_7S), exist_ok=True)
    
    output_folder_8S = "processed_8Ss"
    if not os.path.exists(output_folder_8S):
        os.makedirs(os.path.join(main_folder, output_folder_8S), exist_ok=True)
    
    output_folder_9S = "processed_9Ss"
    if not os.path.exists(output_folder_9S):
        os.makedirs(os.path.join(main_folder, output_folder_9S), exist_ok=True)
    
    output_folder_AS = "processed_ASs"
    if not os.path.exists(output_folder_AS):
        os.makedirs(os.path.join(main_folder, output_folder_AS), exist_ok=True)
    
    output_folder_JS = "processed_JSs"
    if not os.path.exists(output_folder_JS):
        os.makedirs(os.path.join(main_folder, output_folder_JS), exist_ok=True)
    
    output_folder_KS = "processed_KSs"
    if not os.path.exists(output_folder_KS):
        os.makedirs(os.path.join(main_folder, output_folder_KS), exist_ok=True)

    output_folder_QS = "processed_QSs"
    if not os.path.exists(output_folder_QS):
        os.makedirs(os.path.join(main_folder, output_folder_QS), exist_ok=True)

# Loop through the images and process them
for image_path in immg:

    # Load the image that is going to be used
    image = cv2.imread(image_path)

    # Skip the loop if there is something wrong with the image*
    if image is None:
        print(f"Error: Could not read the image at {image_path}. Skipping.")
        raise FileNotFoundError

    # get the 2D* card from the image
    processed_image = process(image, image_path)
    # cv2.imshow("Proc_IM", processed_image)

    # get the name of the future file (idk)
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    output_filename = f"{name}_processed{ext}" # this is the name of the future* file

    os.makedirs(main_folder, exist_ok=True)  # Ensure the folder exists

    output_path = os.path.join(main_folder, output_filename)
    # cv2.imwrite(output_path, processed_image)

print("Done, :)") # say that the program is done.

cv2.waitKey(0) # holds the windows in plase for some reason.
cv2.destroyAllWindows() # read the name
