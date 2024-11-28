#This code was to test for splitting the rank and the suit from each other


import cv2 as cv

corner = cv.imread(r'Photos\2_Cc.jpg', cv.IMREAD_GRAYSCALE)

h, w = corner.shape
diff_h = round(h * 0.1) # 10%

RANK = corner[0:((h//2)+diff_h), 0:w] # ROI for Rank
SUIT = corner[((h//2)+diff_h):h, 0:w] # ROI for Suit

cv.imshow('rankimg', RANK)
cv.imshow('suitimg', SUIT)
cv.waitKey(0)
cv.destroyAllWindows()