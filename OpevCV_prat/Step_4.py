from skimage.metrics import structural_similarity as ssim
import cv2 as cv
import time

best_score = float(0)

suit_path = [r"OpevCV_prat\Card_Imgs\Hearts.jpg", r"OpevCV_prat\Card_Imgs\Spades.jpg", r"OpevCV_prat\Card_Imgs\Diamonds.jpg", r"OpevCV_prat\Card_Imgs\Clubs.jpg"]

image = r"OpevCV_prat\Card_Imgs\Spades.jpg"

# Load the two images
img1 = cv.imread(image, cv.IMREAD_GRAYSCALE)

try:
    for i in range(len(suit_path)):
        # Compute SSIM between the two images
        img2 = cv.imread(suit_path[i], cv.IMREAD_GRAYSCALE)
        score, diff = ssim(img1, img2, full=True)


        if score > best_score:
            best_score = score
    
    # Output the similarity score
    best_score_p = int(best_score * 100) 
    print(f"SSIM Score: {best_score_p}%")
except:
    # Ensure the images have the same dimensions
    if img1.shape != img2.shape:
        print("Images must have the same dimensions.")
    else:
        print("You, no smart! (wiht an asian accent)")

capture = cv.VideoCapture(0)

while True:
    ifTrue, frame = capture.read()

    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("gray", frame)

    frame = cv.GaussianBlur(frame, (3,3), cv.BORDER_DEFAULT)
    cv.imshow("Blur Image", frame)

    #frame = cv.Canny(frame, 125, 175)
    thresholded_image = cv.threshold(frame, 127, 255, cv.THRESH_BINARY)
    cv.imshow("Canny", frame)

    frame = cv.Canny(frame, 125, 175)
    cv.imshow("Video", frame)
    
    if cv.waitKey(20) & 0xFF==ord('q'):
        break

capture.release()

cv.destroyAllWindows

