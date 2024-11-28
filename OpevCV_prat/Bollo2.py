import cv2

# Load the image
image = cv2.imread(r'OpevCV_prat\Photos\2_Cc.jpg', cv2.IMREAD_GRAYSCALE)

# Get dimensions 
h, w = image.shape

diff_h = h * 0.1 # 10%
diff_h = round(diff_h)

RANK = image[0:((h//2)+diff_h), 0:w] # ROI for Rank

# SUIT = image[((h//2)+diff_h):h, 0:w] # ROI for Suit

# Convert to grayscale (if not already)
# gray = cv2.cvtColor(RANK, cv2.COLOR_BGR2GRAY)

# Apply threshold or edge detection
_, thresh = cv2.threshold(RANK, 1, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Assuming you want the largest contour
contour = max(contours, key=cv2.contourArea)

# Get the bounding box of the object
x, y, w, h = cv2.boundingRect(contour)

# Crop the image 
cropped_image = RANK[y:y+h, x:x+w]


# Display 
cv2.imshow('OG Image', image)
cv2.imshow('Rank', RANK) 
# cv2.imshow('Suit', SUIT) 

cv2.waitKey(0)
cv2.destroyAllWindows()