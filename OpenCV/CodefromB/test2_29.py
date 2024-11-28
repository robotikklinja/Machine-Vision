from skimage.metrics import structural_similarity as ssim
import cv2 as cv


"""
code for vincent to review :)
"""

best_score = float(0)

suit_path = [r"OpevCV_prat\Card_Imgs\Hearts.jpg", r"OpevCV_prat\Card_Imgs\Spades.jpg", r"OpevCV_prat\Card_Imgs\Diamonds.jpg", r"OpevCV_prat\Card_Imgs\Clubs.jpg"]

image = r"OpevCV_prat\Card_Imgs\Hearts.jpg"

# Load the two images
img1 = cv.imread(image, cv.IMREAD_GRAYSCALE)

try:
    for i in range(len(suit_path)):
        # Compute SSIM between the two images
        img2 = cv.imread(suit_path[i], cv.IMREAD_GRAYSCALE)
        score, diff = ssim(img1, img2, full=True)

        if score > best_score:
            score = best_score
    
    # Output the similarity score
    print("SSIM Score:", score)
    

except:
    # Ensure the images have the same dimensions
    if img1.shape != img2.shape:
        print("Images must have the same dimensions.")
    else:
        print("You, no smart! (wiht an asian accent)")
