import cv2 as cv

#Function to rescale the frame of the image
def resize_nr(image, scale=0.75): 
    # There is no reson funciton wise why thre image.shape[1]*0 is there.
    # The only reson why it is there is so that changes is easy and for understanding of code.
    width = int(image.shape[1]*0 + 300) # When frame.shape is 1 we refer to the width
    height = int(image.shape[0]*0 + 300) # When frame.shape is 0 we refer to the height

    dimensions = (width,height) # Define it as dimensions

    return cv.resize(image, dimensions, interpolation=cv.INTER_AREA) 

# Load the image 
image = cv.imread(r"OpevCV_prat\Photos\cat.jpg")
image = resize_nr(image)
cv.imshow("Orginal image", image)

# Define the size of the corner to cut out (100x100) 
start_width = 100
end_width = 200

start_height = 100
end_height = 200

# Cut out the top-left corner
top_left_corner = image[start_height:end_height+start_height, start_width:end_width+start_width]

# Save or display the result
cv.imshow("Top Left Corner", top_left_corner)
cv.waitKey(0)
cv.destroyAllWindows()
