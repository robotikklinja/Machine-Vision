from itertools import combinations
import random

"""
Values:
nr = nr (10 = 10, 4 = 4)
10 of Diamonds is 16
2 of Spades is 15
A is 14, but 1 on board
J is 11
Q is 12
K is 13

Points:         Totall
A = 1           (4)
2S = 1          (1)
Most Cards = 1  (1)
Swep = 1        (None)
Sisten = 1      (1)
10D = 2         (2)
Most Spades = 2 (2)
Max             (11)

Average point for Spades are 2/13 (0.15)

Tactics:
Know what the op has in hand in the lats round of play
    - By knowing what cards have been played and what is in my hand.
Knowing what the op can have by looking what is being played/not played
    - By using probability and logic*
Knowing when to play aggressively and not
    - idk , the fast way is to use an AI 
    OR
    - Using a score to see when to be aggressive.
        There should be another score for the board so that a combantion of the scores
        can give a better choese for the player.


How to get info:
The deck has 52 cards
The first 4 in known at the start, so they should get poped out of the deck left.

Another 4 is in my hand, so they get poped as well.

The op alos has 4 cards in there hand, so None should be poped because it is unknow
after knowing the cards through play they can be poped so that the deck updated.

In the last round at the start the amount of cards left in the deck is 4 but those cards are in op's hand

So those can be poped out of the deck, so for the last round a number of conditions must be made like:
    - The amount of cards in the deck is 0.
    - I don't have any card left.
    - It is my turn.

    After all conditions are made one can clam the game if over and make the turn to a None.

Pre ditremend O/I's for hands:
    Example hand:
        10H , 10S, 10D, 10C # all the 10's in a deck
        Here the 10S should be placed down first because if the op would pick it up
        and we would have to pick up the other cards in my hand the one we don't want the second most is 10S
        the one we don't want at all is the 10D because it is worth the most, but if we place it down we have
        to pick it up after no matter what

    The output would be:
        10S # 10S first
        10C # 10C or 10H, dosen't matter
        10H # 10C or 10H, dosen't matter
        10D # last so that we don't get it*

"""



# Add 4 random cards in board that is not Ace, 2 of Spades or 10 of Diamonds
def distribute_to_board():
    # Make a copy of the deck
    board_deck = deck[:] # [:] is in place because any changes in the copy doesn't change deck

    # These cards can't be on the board in the start of the game
    # Remove all Aces:
    board_deck.remove("AH") 
    board_deck.remove("AS")
    board_deck.remove("AD")
    board_deck.remove("AC")

    # Remove  2 of Spades 
    board_deck.remove("2S") 

    # Remove 10 of Diamonds 
    board_deck.remove("10D") 

    # Add 4 random cards in board from the deck
    for _ in range(4): # loop 4 times
        random_card = random.randint(0, len(board_deck)-1) # Choose a random card from the deck
        board.append(board_deck[random_card]) # Add the random card to the board
        deck.remove(deck[random_card]) # remove the card that are placed down from the deck

# Distributes 4 random cards to each player from a given list of items.
def distribute_to_players(amount_players):
    """
    Args:
        players (list): List of player identifiers (e.g., names, IDs).
        items (list): List of items to be distributed.
    
    Returns:
        dict: A dictionary with players as keys and their assigned items as values.
    """

    if not amount_players: # If there are no players to give cards too
        raise ValueError("Players list cannot be empty.")
    elif len(deck) < 4 * len(amount_players): # If there are not enuff cards to distribute
        raise ValueError("Not enough items to distribute evenly.")
    
    player_items = {}
    for player in amount_players:  # Iterate over each player
        player_items[player] = []  # Initialize an empty list for this player's items

        for _ in range(4):  # Each player gets 4 items
            random_card = random.randint(0, len(deck) - 1)  # Choose a random card from the deck

            player_items[player].append(deck[random_card])  # Assign the item

            deck.pop(random_card)  # Remove the item from the list
            # deck.remove(deck[random_card]) # the same 

    # return the 
    return player_items

# Gives 4 random cards to my_hand and to op_hand from the deck
def distribute_2_players(): # Asume the number of players are 2
    # Add 4 random cards to my_hand from the deck
    for _ in range(4): # loop 4 times
        random_card = random.randint(0, len(deck)-1) # Choose a random card from the deck
        my_hand.append(deck[random_card]) # Add the random card to my_hand
        deck.remove(deck[random_card]) # remove the card that are placed down from the deck

    # Add 4 random cards to op_hand from the deck
    for _ in range(4): # loop 4 times
        random_card = random.randint(0, len(deck)-1) # Choose a random card from the deck
        op_hand.append(deck[random_card]) # Add the random card to op_hand
        deck.remove(deck[random_card]) # remove the card that are placed down from the deck

# Gives out the numbers that can't be placed without picking up something
def combos_short(array):
    # Initialize a set to store sums (sets automatically avoid duplicates)
    valid_sums = set()

    # Iterate over all possible numbers of elements to combine (1 to 4)
    for r in range(1, len(array) + 1):
        # Generate all combinations of length r
        for combination in combinations(array, r):
            # Calculate the sum of the combination
            total = sum(combination)
            # Check if the sum is less than or equal to 16
            if total <= 16:
                valid_sums.add(total)

    # Convert the set to a sorted list
    valid_sums = sorted(valid_sums)

    return valid_sums

# Gives out the combantions that are on the board
def combos(array):
    # Initialize a set to store sums (sets automatically avoid duplicates)
    valid_sums = set()

    # Iterate over all possible numbers of elements to combine (1 to 4)
    for r in range(1, len(array) + 1):
        # Generate all combinations of length r
        for combination in combinations(array, r):
            # Calculate the sum of the combination
            total = sum(combination)
            # Check if the sum is less than or equal to 16
            if total <= 16:
                valid_sums.add(total)

    # Convert the set to a sorted list
    valid_sums = sorted(valid_sums)
    # Return the list of combinations that 
    return valid_sums



array_x = [2, 3, 4, 5] # an array for testing

example_hand = ["2"+"Spades", "5"+"Diamond", "2"+"Clubs", "A"+"Clubs"]
example_hand_nr = [15, 5, 2, 14] # example hand in numbers

# The Amount of players playing
players = 2 # make it easy at first (2)


deck = [
'A'+'H', '2'+'H', '3'+'H', '4'+'H', '5'+'H', '6'+'H', '7'+'H', '8'+'H', '9'+'H', '10'+'H', 'J'+'H', 'Q'+'H', 'K'+'H',
'A'+'S', '2'+'S', '3'+'S', '4'+'S', '5'+'S', '6'+'S', '7'+'S', '8'+'S', '9'+'S', '10'+'S', 'J'+'S', 'Q'+'S', 'K'+'S', 
'A'+'D', '2'+'D', '3'+'D', '4'+'D', '5'+'D', '6'+'D', '7'+'D', '8'+'D', '9'+'D', '10'+'D', 'J'+'D', 'Q'+'D', 'K'+'D',
'A'+'C', '2'+'C', '3'+'C', '4'+'C', '5'+'C', '6'+'C', '7'+'C', '8'+'C', '9'+'C', '10'+'C', 'J'+'C', 'Q'+'C', 'K'+'C',
]

# Says if the turn is mine or not
turn = True # # An int value should be used if players > 2

my_hand = [] # My hand 
my_points = 0 # The amount of points I have

op_hand = [] # The op's hand
op_points = 0 # The amount of points the op has

# The can that are on the board
board = []

# Deal the cards the board
distribute_to_board()

# Algorithm for KrypCasino:
while True:

    # Deal the cards to the 2 players
    distribute_2_players()

    # If it is my turn 
    if turn:
        if len(deck) == 4:
            pass

        # if we are in the last round of play 
        if len(deck) == 0:
            if len(my_hand) and len(op_hand) == 0:
                print("The game is over. Time to start counting points ...")
            

        elif len(my_hand) == 1: # there is only one card left in hand
            print(f"I place down {my_hand[0]}") # place down the last card in hand
        else:
            if "10D" in my_hand:
                print("I place down 10 of Diamond")
                my_hand.remove("10D") # "10"+"D" = "10D"
                board.append("10D") # Add 10D on board

        trun = False # always change the turn after
        
    # if it is the op's turn        
    elif not turn:
        pass # the same as my turn, but change from my_hand to op_hand
    else: # this mean there are no more card to be played
        print("The game is over")
        break # break the loop



