import cv2
import numpy as np

def isolate_top_left_number(card_image):
    """
    Isolate and crop the number in the top-left corner of a card image.
    The resulting image will ensure the number touches one or more edges.
    
    :param card_image: 2D card image (numpy array)
    :return: Cropped image with the number touching one or more sides
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(card_image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray) 

    # Apply threshold to isolate the number region
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imshow("thresh" ,thresh)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours to find the number in the top-left corner
    top_left_number = None
    for contour in contours:
        # Get bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Check if the bounding box is in the top-left region
        if x < (card_image.shape[1] // 4) and y < card_image.shape[0] // 4:
            top_left_number = contour
            break
    
    if top_left_number is None:
        print("No number detected in the top-left corner!")
        return None

    # Get bounding box of the top-left number
    x, y, w, h = cv2.boundingRect(top_left_number)
    
    # Crop the number with padding to ensure it touches edges
    global cropped_number
    cropped_number = thresh[y:y+h, x:x+w]

    # Find contours of the cropped number to further trim it
    number_contours, _ = cv2.findContours(cropped_number, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if number_contours:
        x2, y2, w2, h2 = cv2.boundingRect(number_contours[0])
        cropped_number = cropped_number[y2:y2+h2, x2:x2+w2]

    return cropped_number

# Load a sample card image
card_image = cv2.imread(r"OpevCV_prat\Photos\7_of_D.jpg")
    
    # Isolate the number in the top-left corner
top_left_number_image = isolate_top_left_number(card_image)

if top_left_number_image is None:
    raise SyntaxError("Naa I aint doun that.")



# Display the result
cv2.imshow("Top Left Number", top_left_number_image)

cv2.imshow("Cropped Image", cropped_number)

cv2.waitKey(0)
cv2.destroyAllWindows()
