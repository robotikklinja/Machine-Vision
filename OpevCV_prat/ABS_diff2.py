import cv2 as cv
import numpy as np

def image_similarity_score(imageA, imageB):
    # Ensure the images are the same size
    if imageA.shape != imageB.shape:
        raise ValueError("Images must have the same dimensions") 
    
    # Calculate the absolute difference between the two images
    diff = cv.absdiff(imageA, imageB)
    
    # Convert the difference to float and normalize it
    diff_float = diff.astype("float") / 255  # Normalize difference to range 0-1
    diff_score = np.mean(diff_float)  # Mean of all pixel differences in the range 0-1
    
    # Calculate similarity as (1 - diff_score) * 100 to get a percentage
    similarity_score = (1 - diff_score) * 100 
    
    return similarity_score

def nr_suit_to_suit(suit):
    # Check what suit it is:
    if suit == 0: # Checks for Hearts
        suit = "Hearts"
    elif suit == 1: # Check for Spades
        suit = "Spades"
    elif suit == 2: # Checks for Diamonds
        suit = "Diamonds"
    elif suit == 3: # Checks for Clubs
        suit = "Clubs"
    return suit

def nr_symbol_to_symbol(number_nr):
    int(number_nr) 
    # Check what suit it is:
    if number_nr == 0: # Check for Ace 
        number_nr = "A"
    elif number_nr > 10: # Check for J->K
        if number_nr == 11:
            number = "J"
        elif number_nr == 12:
            number = "Q"
        elif number_nr == 13:
            number = "K"
    else:
        number = number_nr + 1 # if number_nr = 3 -> number = 4 
    return number 



# # Load images in grayscale mode for simplicity
# card_image_suit = cv.imread(r'OpevCV_prat\Photos\Clubs.jpg', cv.IMREAD_GRAYSCALE)

# # An array of paths to the reference images of suits
# reference_paths_suit = [r"OpevCV_prat\Photos\Hearts.jpg", r"OpevCV_prat\Photos\Spades.jpg", r"OpevCV_prat\Photos\Diamonds.jpg", r"OpevCV_prat\Photos\Clubs.jpg"]

# # set best_score to the worst score possible
# best_score_suit = 0
# suit_nr = None
# # Check the score between all reference images and the image and give out the best score
# for i in range(len(reference_paths_suit)):
#     # Set reference_image to the str of relativ path
#     suit_path = reference_paths_suit[i]

#     # load image for reference path and grayscale the image to be sure/safe 
#     image_i_suit = cv.imread(suit_path, cv.IMREAD_GRAYSCALE)

#     # Set sim_score to be the score between one of the ref and an img
#     sim_score_suit = image_similarity_score(image_i_suit, card_image_suit)

#     # best_score is allways teh Best score: 
#     if best_score_suit < sim_score_suit:
#         suit_nr = i
#         best_score_suit = sim_score_suit

# suit = nr_suit_to_suit(suit_nr)

# # Print the best score and what suit it is
# print(f"Similarity of Suit: {best_score_suit:.2f}%", suit)



# Load image in grayscale modefor simplicity 
card_image_nr = cv.imread(r"OpevCV_prat\Card_Imgs\Ace.jpg", cv.IMREAD_GRAYSCALE)

# An array of paths to the reference images of numbers
reference_paths_nr = [r"OpevCV_prat\Card_Imgs\Ace.jpg", r"OpevCV_prat\Card_Imgs\Two.jpg", r"OpevCV_prat\Card_Imgs\Three.jpg", r"OpevCV_prat\Card_Imgs\Four.jpg", r"OpevCV_prat\Card_Imgs\Five.jpg", r"OpevCV_prat\Card_Imgs\Six.jpg", r"OpevCV_prat\Card_Imgs\Seven.jpg", r"OpevCV_prat\Card_Imgs\Eight.jpg", r"OpevCV_prat\Card_Imgs\Nine.jpg", r"OpevCV_prat\Card_Imgs\Ten.jpg", r"OpevCV_prat\Card_Imgs\Jack.jpg", r"OpevCV_prat\Card_Imgs\Queen.jpg", r"OpevCV_prat\Card_Imgs\King.jpg"]

best_score_nr = 0
nr_nr = -1
for i in range(len(reference_paths_nr)):
    # Set reference_image to the str of relativ path
    nr_path = reference_paths_nr[i]

    # load image for reference path and grayscale the image to be sure/safe
    image_i_nr = cv.imread(nr_path, cv.IMREAD_GRAYSCALE)

    # Set sim_score to be the score between one of the ref and an img
    sim_score_nr = image_similarity_score(image_i_nr, card_image_nr)

    # best_score is allways teh Best score: 
    if best_score_nr < sim_score_nr:
        inn = i 
        best_score_nr = sim_score_nr



# nr = nr_symbol_to_symbol(nr_nr)

# Print the best score and what suit it is
print(f"Similarity of nr: {best_score_nr:.2f}%", inn)