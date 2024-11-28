import cv2 as cv
import time


# Cards paths to A, 2, 3, ..., K
card_paths = (r"UR5_OpenCV_Cards\Card_Imgs\Ace.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Two.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Three.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Four.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Five.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Six.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Seven.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Eight.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Nine.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Ten.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Jack.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Queen.jpg", r"UR5_OpenCV_Cards\Card_Imgs\King.jpg")

# Cards paths to suts
card_suts = [r"UR5_OpenCV_Cards\Card_Imgs\Hearts.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Spades.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Diamonds.jpg", r"UR5_OpenCV_Cards\Card_Imgs\Clubs.jpg"] 
# Harts, Spades, Diamonds, Clubs in that order

# time.sleep(1)
# capture = cv.VideoCapture(0)

# while True:

#     isTrue, frame = capture.read()
#     cv.imshow("Start Window", frame)

    

#     if cv.waitKey(20) & 0xFF==ord('q'):
#         break

print(len(card_paths))
