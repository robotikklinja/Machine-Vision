"""
This code is supposed to be the AI for the card game KrypKasino.
This is supposed to be coded to take inputs from the OpenCV program made by B.Stokke.
For now (12.12.2024) it is getting inputs locally.

Made by V.Dalisay on 12.12.2024
"""

import numpy as np
from collections import defaultdict
import itertools


# Since the input comes as a string, a king of hearts will be inputted as a KH. The first character being the rank, K, and the second character being the suit, H.
# This class makes it so that it identifies the input as a card.
class Cardrule:
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
        rank_values = {
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

        # Value changes depending on where the card is placed
        if self.location == "table":
            return rank_values.get(self.rank, 0)  # Values for cards in the table (basic values)
        
        elif self.location == "hand":
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
            
            card_key = f"{self.rank}{self.suit}"  # Combine rank and suit to form the key

            # Handle the special cases for 2 of Spades and 10 of Diamonds
            if card_key == "2S":
                return 15  # The 2 of spades has a value of 15 in the player's hand
            elif card_key == "10D":
                return 16  # The 10 of diamonds has a value of 16 in the player's hand

            # Handle all other cards normally
            return hand_rank_values.get(self.rank, 0)
        
        else:
            return 0  # Default if card location is not defined

# This class is used to define what cards the program has in its "hand"
class Hand:
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
        if len(self.cards) > 4:
            raise SyntaxError("Too many cards in hand")
        
    def set_location(self, location):
        # Set the location for each card in the hand (hand, table, etc.).
        for card in self.cards:
            card.location = "hand"
    
    def __str__(self):
        # Use the str method for printing the hand (human-readable format)
        return ", ".join(str(card) for card in self.cards)

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
        
    def set_location(self, location):
        # Set the location for each card in the hand (hand, table, etc.).
        for card in self.cards:
            card.location = "table"
    
    def __str__(self):
        # Use the str method for printing the hand (human-readable format)
        return ", ".join(str(card) for card in self.cards)

    # def __repr__(self):
    #     # Use the repr method for debugging or more precise representation
    #     return f', '.join(repr(card) for card in self.cards)

class KrypKasinoAI:
    def __init__(self, hand, table):
        self.hand = hand  # List of cards in the hand of the AI (list of Card objects)
        self.table = table  # List of cards on the table
        self.claimed_cards = [] # The 
        self.points = 0 # The points that the AI has
        return

    def decision(self):
        """
        Decision logic: Play a card which will result in the least
        amount of points earned at the end of the turn.
        """
        best_card = None
        best_claim = None
        worst_claim = float('inf') # To avoid claims that result in getting points

        for card in self.hand:
            can_claim, claim = cardcombos(card, self.table)
            if can_claim:
                # Calculate how many cards would be claimed if this card is played
                claim_size = len(claim)

                # AI should avoid claiming a card that would result in a lot of claimed cards
                if claim_size < worst_claim:
                    worst_claim = claim_size
                    best_card = card
                    best_claim = claim

        # If no card can be claimed (safe move), just play the card with the lowest value
        if best_card is None:
            best_card = max(self.hand, key=lambda card: card.get_value())

        # Simulate playing the chosen card
        self.play_card(best_card, best_claim)
        return best_card
    
    def play_card(self, card, claimed_cards=None):
        if claimed_cards:
            self.claimed_cards.extend(claimed_cards)
            self.hand.remove(card)  # Remove the card from the hand as it's now played
            print(f"AI claims: {', '.join(str(c) for c in claimed_cards)}")
        else:
            self.table.append(card)  # Put the card on the table
            self.hand.remove(card)
            print(f"AI plays: {card}")

# Logic to see what cards add up to what
def cardcombos(card, table_cards):
    card_value = card.get_value()
    # Generate all possible combinations of the table cards
    for r in range(1, len(table_cards) + 1):  # r is the size of the combination
        for combination in itertools.combinations(table_cards, r):
            # If the sum of a combination matches the card value, return True
            if sum(card.get_value() for card in combination) == card_value:
                return True, combination  # Return True with the combination of cards
    return False, []

# This is a testing code to be used as a temporary input
hand = Hand()
table = Table()

# This is a dummy hand. There will be a maximum of four cards in the hand
hand.add_card(["2S", "10D", "10C", "AH"])

# This is a dummy table
table.add_card(["7D", "8H", "7S", "5S"])

# Now, set the location for all cards after they are added
hand.set_location("hand")

# Print the hand using the str method. The str method is used to print out a human-readable format
print(str(hand))  # This will use Hand.__str__, which calls Card.__str__

# Get values of all cards in the hand
for card in hand.cards:
    print(f"{card}: Value = {card.get_value()}")