import cv2 as cv
import numpy as np

blank = np.zeros((500, 500, 3), dtype="uint8")
cv.imshow("Blank", blank)

# blank[200:300, 300:400] = 0, 255, 255 #color in RGB
# cv.imshow("Green", blank)

cv.rectangle(blank, (175, 175), (blank.shape[0]//2, blank.shape[1]//2), (0,255,0), thickness=2)
cv.imshow("Rec", blank)

cv.waitKey(0)


