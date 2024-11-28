import cv2 as cv

img = cv.imread(r"OpevCV_prat/Photos/Diamonds.jpg")
cv.imshow("Original Image nr.1", img)

img2 = cv.imread(r"OpevCV_prat\Photos\Clubs.jpg")
cv.imshow("Image nr.2", img2)



gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("Gray" ,gray)

blur = cv.GaussianBlur(img, (7,7), cv.BORDER_DEFAULT)
cv.imshow("Blured Image", blur)

canny = cv.Canny(blur, 125, 175)
cv.imshow("Canny", canny)

dilate = cv.dilate(canny, (7, 7), iterations=1) 
cv.imshow("Dilate", dilate)



cv.waitKey(0)