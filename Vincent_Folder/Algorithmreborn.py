"""
This code is supposed to be an CPU for the card game KrypKasino.
This is supposed to be coded to take inputs from the OpenCV program made by B.Stokke.
For now (12.12.2024) it is getting inputs locally.

As of (13.02.2025) it will use an algorithm instead. Further changes to be made.

Made by V.Dalisay on 12.12.2024
"""

import numpy as np
from collections import defaultdict
import copy # to create a copy of the game state to simulate moves
import time
import itertools

# Since the input comes as a string, a king of hearts will be inputted as a KH. The first character being the rank, K, and the second character being the suit, H.
# This class makes it so that it identifies the input as a card.
class Cardrule:
    # Dictionaries for the values of the cards depending on whether they are in the hand or on the table
    table_rank_values = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13
    }

    hand_rank_values = {
        "A": 14, # Aces have a value of 14 in the player's hand
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        # "2S": 15, # The 2 of spades has a value of 15 in the player's hand
        # "10D": 16 # The 10 of diamonds has a value of 16
    }
    special_hand_values = {
        "2S": 15,
        "10D": 16
    }
    
    # This function makes it so that every input is broken down into the rank and suit.
    def __init__(self, card_string):
        self.rank = card_string[:-1]  # Everything except the last character represents the rank
        self.suit = card_string[-1]   # The last character of the string inputted is the suit
        self.location = None  # Where the card is placed (e.g., 'hand', 'table')

    def __str__(self):
        # Convert the numbers and suit in the input to actual names so its more comprehensible
        rank_names = {
            "A": "Ace",
            "2": "Two",
            "3": "Three",
            "4": "Four",
            "5": "Five",
            "6": "Six",
            "7": "Seven",
            "8": "Eight",
            "9": "Nine",
            "10": "Ten",
            "J": "Jack",
            "Q": "Queen",
            "K": "King"
        }
        
        suit_names = {
            "S": "Spades",
            "D": "Diamonds",
            "C": "Clubs",
            "H": "Hearts"
        }
        
        # Get the rank and suit name from the dictionary, or return an error if the rank and/or suit is invalid
        rank_name = rank_names.get(self.rank, "Invalid rank")
        suit_name = suit_names.get(self.suit, "Invalid suit")
        
        # Return the human-readable form
        return f"{rank_name} of {suit_name}"
    
    # def __repr__(self):
    #     return f"{self.rank}{self.suit}"  # Used for debugging or precise representations

    # Function used to determine a card's value based on its location (hand or table).
    def get_value(self):
        # Return card value based on location
        if self.location == "table":
            return self.table_rank_values.get(self.rank, 0)  # Use table values
        elif self.location == "hand":
            card_key = f"{self.rank}{self.suit}"  # Combine rank and suit for special cases
            # Check for special hand values first, then default to hand rank values
            return self.special_hand_values.get(card_key, self.hand_rank_values.get(self.rank, 0))
        return 0  # Default value if location is not defined

# This class is used to define what cards the CPU has in its "hand"
class Hand:
    def __init__(self):
        self.cards = []  # This will store Card objects

    # Function to add cards into the hand
    def add_card(self, card_string):
        # Adds one or more card strings to the hand.
        if isinstance(card_string, list):
            # If the input is a list of cards, add all cards in the list
            for card in card_string:
                self.cards.append(Cardrule(card))
        else:
            # If it's a single card string, add that one card
            self.cards.append(Cardrule(card_string))

        # Raise an error if the robot has recieved too many cards under the dealing process
        if len(self.cards) > 4:
            raise SyntaxError("Too many cards in hand")
        
    def set_location(self):
        # Set the location for each card in the hand (in this case the hand).
        for card in self.cards:
            card.location = "hand"
    
    def __str__(self):
        # Use the str method for printing the hand (human-readable format)
        return ", ".join(str(card) for card in self.cards)
    
    def __iter__(self):
        # This makes the Hand object iterable, by returning its cards list.
        return iter(self.cards)
        
    # def __repr__(self):
    #     # Use the repr method for debugging or more precise representation
    #     return f', '.join(repr(card) for card in self.cards)


class Table:
    def __init__(self):
        self.cards = []  # This will store Card objects

    def add_card(self, card_string):
        # Add one or more card strings to the hand.
        if isinstance(card_string, list):
            # If the input is a list, add all cards in the list
            for card in card_string:
                self.cards.append(Cardrule(card))
        else:
            # If it's a single card string, add that one card
            self.cards.append(Cardrule(card_string))
        
    def set_location(self):
        # Set the location for each card in the hand (in this case the table).
        for card in self.cards:
            card.location = "table"
    
    def __str__(self):
        # Use the str method for printing the hand (human-readable format)
        return ", ".join(str(card) for card in self.cards)

    # def __repr__(self):
    #     # Use the repr method for debugging or more precise representation
    #     return f', '.join(repr(card) for card in self.cards)

class KrypKasinoAlgorithm:
    def __init__(self, hand, table):
        self.hand = hand  # List of cards in the hand of the CPU (list of Card objects)
        self.table = table  # List of cards on the table
        self.claimed_cards = []  # Array of the cards claimed by the CPU.
        self.points = 0 # The points that the CPU has

    def get_state(self):
        # Represent the game state as a numerical feature vector
        state = [
            # Hand features
            len(self.hand.cards), 
            # Table features
            len(self.table.cards),
            # Sum of card values in hand
            sum(card.get_value() for card in self.hand.cards), 
            # Sum of card values on table
            sum(card.get_value() for card in self.table.cards),
            # Check for potential captures (e.g., cards with the same rank on the table)
            1 if any(card.rank in [c.rank for c in self.table.cards] for card in self.hand.cards) else 0
        ]
        return state
    
    def best_move(self):
        # Used to define what card to play
        best_play = None
        # Used to compare points from other cards played.
        best_score = float('inf')
        # To see what combination is the best
        best_combination = None

# This function is to be used to simulate the game so that the algorithm knows what card to play.
# Therefore i will return best_play for use.

        for playcard in (self.hand.cards):
            # Simulate the game state by making a deep copy of both the cards in the hand and the cards in the table.
            simulate_hand = copy.deepcopy(self.hand)
            simulate_table = copy.deepcopy(self.table)

            # For every card from the hand check if
            for i, card in enumerate(simulate_hand.cards):
                if card.rank == playcard.rank and card.suit == playcard.suit:
                    del simulate_hand.cards[i]
                    break

            # simulate adding the card to the table and turn it into a string
            simulate_table.add_card(str(playcard))

            # get all possible combinations of the claimable cards based on the move
            all_combos = cardcombos(playcard, simulate_table.cards, self)

            # Go through all combinations and choose the best
            for combination in all_combos:
                
                # Remove the claimed cards.
                for claimed_card in combination:
                    for i, table_card in enumerate(simulate_table.cards):
                        if table_card.rank == claimed_card.rank and table_card.suit == claimed_card.suit:
                            del simulate_table.cards[i]
                            break

            print(f"Algorithm simulates: {playcard}")
            print(f"Algorithm's hand after the play: {simulate_hand}")
            print()


        for i in range(len(hand)):
            score = wombo_combo_point[i]
        return best_play
    
    def cardpoints(self):
        cardpoint = {
        "AS": 1.173076923,
        "2S": 1.173076923,
        "3S": 0.173076923,
        "4S": 0.173076923,
        "5S": 0.173076923,
        "6S": 0.173076923,
        "7S": 0.173076923,
        "8S": 0.173076923,
        "9S": 0.173076923,
        "10S": 0.173076923,
        "JS": 0.173076923,
        "QS": 0.173076923,
        "KS": 0.173076923,
        "AC": 1.019230769,
        "2C": 0.019230769,
        "3C": 0.019230769,
        "4C": 0.019230769,
        "5C": 0.019230769,
        "6C": 0.019230769,
        "7C": 0.019230769,
        "8C": 0.019230769,
        "9C": 0.019230769,
        "10C": 0.019230769,
        "JC": 0.019230769,
        "QC": 0.019230769,
        "KC": 0.019230769,
        "AD": 1.019230769,
        "2D": 0.019230769,
        "3D": 0.019230769,
        "4D": 0.019230769,
        "5D": 0.019230769,
        "6D": 0.019230769,
        "7D": 0.019230769,
        "8D": 0.019230769,
        "9D": 0.019230769,
        "10D": 2.019230769,
        "JD": 0.019230769,
        "QD": 0.019230769,
        "KD": 0.019230769,
        "AH": 1.019230769,
        "2H": 0.019230769,
        "3H": 0.019230769,
        "4H": 0.019230769,
        "5H": 0.019230769,
        "6H": 0.019230769,
        "7H": 0.019230769,
        "8H": 0.019230769,
        "9H": 0.019230769,
        "10H": 0.019230769,
        "JH": 0.019230769,
        "QH": 0.019230769,
        "KH": 0.019230769,
        }

        return cardpoint.get(self, "CARD DOES NOT EGGSIST")

    # def play_card(self, card, claimed_cards=None):
    #     # Play the card first
    #     self.table.add_card(str(card))  # Add the card to the table
    #     self.hand.cards.remove(card)  # Remove the card from the hand's cards list
    #     print(f"CPU plays: {card}")

    #     # Only handle claiming cards if a valid combination was found
    #     if claimed_cards:
    #         self.claimed_cards.extend(claimed_cards)
    #         print(f"CPU claims: {', '.join(str(c) for c in claimed_cards)}")
    #     else:
    #         print(f"CPU claims no cards.")

class Game:
    def __init__(self, num_players=2):
        self.num_players = num_players  # How many players are in the game
        self.turn = 0  # To track which player's turn it is (0 for Player 1, 1 for Player 2)
        self.players = ["CPU", "Player 2"]  # List of players (assuming CPU is player 1, but you can customize this)
        self.current_player = self.players[self.turn]  # This will hold the current player's name
        self.hand = Hand()  # Initialize player's hand
        self.table = Table()  # Initialize table

    def play_turn(self):
        """
        Simulate the action for the current player's turn.
        If it's the CPU's turn, the CPU will play a card.
        If it's the human player's turn, you may want to collect input (depending on how they interact with the game).
        """
        print(f"{self.current_player}'s turn:")
        
        if self.current_player == "CPU":
            # Call the CPU's decision-making function here
            CPU = KrypKasinoAlgorithm(self.hand, self.table)
            CPU.decision()

        else:
            # Handle human player's move (get input, etc.)
            print("Player 2's turn: Input move manually")
        
        # After each turn, switch to the next player
        self.next_turn()

    def ops_turn(self):
        """
        Monitor the table for card changes (indicating the human player has played a card).
        """
        initial_table_card_count = len(self.table.cards)
        
        print(f"Waiting for {self.current_player} to make a move...")
        
        while True:
            time.sleep(2)  # Check every two seconds
            
            # Check the current number of cards on the table
            current_table_card_count = len(self.table.cards)
            
            # If the number of cards on the table has increased, Player 1 has played a card
            if current_table_card_count != initial_table_card_count:
                print(f"{self.current_player} has played a card!")
                break  # Exit the loop to switch turns

    def switchturn(self):
        # Switch to next player
        self.turn = (self.turn + 1) % self.num_players # This will cycle between 0 and 1 if there are 2 players
        self.current_player = self.players[self.turn] # Set the current player to the next one
        print(f"Next turn: {self.current_player}")

# Logic to see what cards add up to what
def cardcombos(card, table_cards, CPU_instance):
    card_value = card.get_value()  # Get the value of the card being played
    all_combinations = [] # Store all valid combinations in an array

    # For every card in the hand check what combinations there are that match the value of the card "played"
    for r in range(1, len(table_cards) + 1):
        for combination in itertools.combinations(table_cards, r):
            if sum(c.get_value() for c in combination) == card_value:
                all_combinations.append(list(combination)) 

    # find the value of each combo and set the val in an array
    wombo_combo_point = []
    for combination in all_combinations: # g throught very combo 
        combo_point = 0.0 # start val for value of combo
        for card in combination: # get the value of each of the cards in the combos
            cardkey = str(card) # make sure it is a str and the OG doesn't change
            card_point = CPU_instance.cardpoints().get(cardkey, 0.0) # Get the card point from the cardpoints dictionary.
            combo_point += card_point # add the cards value to the combo
        wombo_combo_point.append(combo_point) # add the value of the combo in a varibale
    wombo_combo_point.sort() # sort form small too big

    combined_data = list(zip(wombo_combo_point, all_combinations))
    combined_data.sort()
    sorted_points, sorted_combinations = zip(*combined_data) if combined_data else ([], [])

    return list(sorted_combinations), list(sorted_points)

hand = Hand() # CPU's hand 
table = Table() # cards on the table

# This is a testing code to be used as a temporary input
# This is a dummy hand. There will be a maximum of four cards in the hand
# hand.add_card(["7S", "4H", "8C", "AH"])
hand.add_card(["7D", "5S", "2D"])
# This is a dummy table
# table.add_card(["7D", "8H", "7H", "5S"])
table.add_card(["7H","8H"])


# Now, set the location for all cards after they are added
hand.set_location()
table.set_location()

# Print the hand using the str method. The str method is used to print out a human-readable format
print("Algorithm hand: ", str(hand))  # This will use Hand.__str__, which calls Card.__str__

# Get values of all cards in the hand
# for card in hand.cards:
#     print(f"{card}: Value = {card.get_value()}")

# Initialize CPU and make a decision
algorithm = KrypKasinoAlgorithm(hand, table)
# Call best_move() to get the best card
best_card = algorithm.best_move()