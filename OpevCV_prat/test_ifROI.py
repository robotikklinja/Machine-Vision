"""

Conclusion:
If the image is gray it only gives 2 vals, but when it is "normal" it gives 3

If I don't know I can make and use a function that output the height and width no mater what. 

"""

import cv2 as cv

def shape(image):
    try:
        h, w = image.shape
    except:
        h, w, _ = image.shape
    return h, w

img = cv.imread(r"OpevCV_prat\Photos\cat.jpg")
cv.imshow("OG", img)

h, w, _ = img.shape
ROI = img[0:h//2, 0:w]

gray = cv.cvtColor(ROI, cv.COLOR_BGR2GRAY)


h2, w2 = shape(gray) 
# h3, w3 = shape(ROI)
RANK = ROI[0:h2, 0:w2//2]


cv.imshow("ROI", ROI)
cv.imshow("gray", gray)
cv.imshow("Rank", RANK)

cv.waitKey(0)
cv.destroyAllWindows()
