import cv2 as cv    


corner = cv.imread(r'OpenCV\Photos\2_Cc.jpg', cv.COLOR_BGR2GRAY)

h, w, _ = corner.shape
diff_h = round(h * 0.1) # 10%

ROI_RANK = corner[(h//2):(w//2), h:w]
# Make an image to black and white (including gray) 
# gray = cv.cvtColor(ROI_RANK, cv.COLOR_BGR2GRAY) 
 
# Highlights the edges in an image 
_, thresh = cv.threshold(ROI_RANK, 50, 255, cv.THRESH_BINARY) 
 
 # Finds the contours in an image (shapes)
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Sort contours by area (largest to smallest) and keep the largest two
contours = sorted(contours, key=cv.contourArea, reverse=True)[:2] 

# Ensure the rank is above the suit by sorting by vertical position
contours = sorted(contours, key=lambda c: cv.boundingRect(c)[1])

# Extract bounding boxes 
rank_x, rank_y, rank_w, rank_h = cv.boundingRect(contours[0])  # Rank 
# suit_x, suit_y, suit_w, suit_h = cv.boundingRect(contours[1])  # Suit 

# Crop the rank and suit areas 
rank_img = corner[rank_y:rank_y+rank_h, rank_x:rank_x+rank_w] # Rand Image
# suit_img = corner[suit_y:suit_y+suit_h, suit_x:suit_x+suit_w] # Suit Image