import numpy as np
import cv2

def resize(image, x_dim, y_dim):
    width = int(image.shape[1]*0 + x_dim)
    hight = int(image.shape[0]*0 + y_dim)

    dimensions = (width, hight) 

    return cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)

def image_similarity_score(imageA, imageB):
    # Ensure the images are the same size
    if imageA.shape != imageB.shape:
        raise ValueError("Images must have the same dimensions") 
    
    # Calculate the absolute difference between the two images
    diff = cv2.absdiff(imageA, imageB)
    
    # Convert the difference to float and normalize it
    diff_float = diff.astype("float") / 255  # Normalize difference to range 0-1
    diff_score = np.mean(diff_float)  # Mean of all pixel differences in the range 0-1
    
    # Calculate similarity as (1 - diff_score) * 100 to get a percentage
    similarity_score = (1 - diff_score) * 100
    
    return similarity_score

ref = cv2.imread(r'OpevCV_prat\Card_Imgs\Two.jpg') 
cv2.imshow("2", ref)

# Load the image in grayscale
image = cv2.imread(r'OpevCV_prat\Photos\2_Cc.jpg', cv2.IMREAD_GRAYSCALE)

# Get dimensions
h, w = image.shape
diff_h = round(h * 0.1)  # 10% of the height

# Define the Region of Interest (ROI)
RANK = image[0:((h // 2) + diff_h), 0:w]  # Crop the top half with a bit more

# Apply Canny edge detection to find edges
edges = cv2.Canny(RANK, threshold1=50, threshold2=150)
cv2.imshow("some", edges)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour by area
contour = max(contours, key=cv2.contourArea)

# Get the bounding box for the largest contour
x, y, bbox_w, bbox_h = cv2.boundingRect(contour)

# Crop the image using the bounding box
cropped_image = RANK[y:y+bbox_h, x:x+bbox_w]

cropped_image = resize(cropped_image, 70, 125) 
    
# Display the images
cv2.imshow('Original Image', image)
cv2.imshow('Edges', edges)
cv2.imshow('Cropped Image', cropped_image)
cv2.rectangle(RANK, (x, y), (x+bbox_w, y+bbox_h), (255, 255, 255), 2)
cv2.imshow('Bounding Box', RANK)

# Load image in grayscale modefor simplicity 
# card_image_nr = cv.imread(r"OpevCV_prat\Card_Imgs\Ace.jpg", cv2.IMREAD_GRAYSCALE)

# An array of paths to the reference images of numbers
reference_paths_nr = [r"OpevCV_prat\Card_Imgs\Ace.jpg", r"OpevCV_prat\Card_Imgs\Two.jpg", r"OpevCV_prat\Card_Imgs\Three.jpg", r"OpevCV_prat\Card_Imgs\Four.jpg", r"OpevCV_prat\Card_Imgs\Five.jpg", r"OpevCV_prat\Card_Imgs\Six.jpg", r"OpevCV_prat\Card_Imgs\Seven.jpg", r"OpevCV_prat\Card_Imgs\Eight.jpg", r"OpevCV_prat\Card_Imgs\Nine.jpg", r"OpevCV_prat\Card_Imgs\Ten.jpg", r"OpevCV_prat\Card_Imgs\Jack.jpg", r"OpevCV_prat\Card_Imgs\Queen.jpg", r"OpevCV_prat\Card_Imgs\King.jpg"]

# grayed = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(cropped_image, 50, 255, cv2.THRESH_BINARY)


best_score_nr = 0
nr_nr = -1
for i in range(len(reference_paths_nr)):
    # Set reference_image to the str of relativ path
    nr_path = reference_paths_nr[i]

    # load image for reference path and grayscale the image to be sure/safe
    image_i_nr = cv2.imread(nr_path, cv2.IMREAD_GRAYSCALE)

    # Set sim_score to be the score between one of the ref and an img
    sim_score_nr = image_similarity_score(image_i_nr, cropped_image)

    # best_score is allways teh Best score: 
    if best_score_nr < sim_score_nr:
        inn = i 
        best_score_nr = sim_score_nr



# nr = nr_symbol_to_symbol(nr_nr)

# Print the best score and what suit it is
print(f"Similarity of nr: {best_score_nr:.2f}%", inn)

cv2.waitKey(0)
cv2.destroyAllWindows()

