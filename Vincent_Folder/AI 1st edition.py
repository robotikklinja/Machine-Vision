"""
This code is supposed to be the AI for the card game KrypKasino.
This is supposed to be coded to take inputs from the OpenCV program made by B.Stokke.
For now (12.12.2024) it is getting inputs locally.

Made by V.Dalisay on 12.12.2024
"""

import numpy as np
import tensorflow as tf
from collections import defaultdict
import itertools
import time
import random

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

# This class is used to define what cards the AI has in its "hand"
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

class KrypKasinoAI:
    def __init__(self, hand, table):
        self.hand = hand  # List of cards in the hand of the AI (list of Card objects)
        self.table = table  # List of cards on the table
        self.claimed_cards = []  # Array of the cards claimed by the AI.
        self.points = 0  # The points that the AI has
        # Initialize epsilon here (typically a value between 0 and 1)
        self.epsilon = 0.1  # Exploration rate (e.g., 10% of the time the AI explores)
        # **Initialize the learning rate here**
        self.learning_rate = 0.01  # Learning rate for the Adam optimizer
        # **Initialize the model here**
        self.model = self.build_model()  # Call the build_model function to create the model

    def build_model(self):
        # Define the input shape (you'll need to adjust this based on your state representation)
        input_shape = (len(self.get_state()),) 
        model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=input_shape),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(len(self.hand.cards), activation='linear') 
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate), loss='mse')
        return model

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

    def decision(self):
        if np.random.rand() < self.epsilon:  # Explore (choose a random action)
            return random.choice(self.hand.cards)

        state = self.get_state()
        state_tensor = np.array([state])
        q_values = self.model.predict(state_tensor)[0]

        # Choose the action with the highest predicted Q-value
        action_index = np.argmax(q_values)
        return self.hand.cards[action_index]

    def play_card(self, card, claimed_cards=None):
        # Play the card first
        self.table.add_card(str(card))  # Add the card to the table
        self.hand.cards.remove(card)  # Remove the card from the hand's cards list
        print(f"AI plays: {card}")

        # Only handle claiming cards if a valid combination was found
        if claimed_cards:
            self.claimed_cards.extend(claimed_cards)
            print(f"AI claims: {', '.join(str(c) for c in claimed_cards)}")
        else:
            print(f"AI claims no cards.")

        # Store the experience in the replay buffer
        old_state = self.get_state() 
        action_index = self.hand.cards.index(card)  # Get the index of the chosen action
        reward = self.calculate_reward(claimed_cards)  # Calculate reward (e.g., -len(claimed_cards))
        new_state = self.get_state() 
        self.store_experience((old_state, action_index, reward, new_state))

    def store_experience(self, experience):
        self.experience_replay_buffer.append(experience)
        if len(self.experience_replay_buffer) > self.experience_replay_buffer_size:
            self.experience_replay_buffer.pop(0)

    def train_model(self):
        if len(self.experience_replay_buffer) < 32:  # Adjust batch size as needed
            return

        batch = random.sample(self.experience_replay_buffer, 32)
        states, actions, rewards, next_states = zip(*batch)
        states = np.array(states)
        actions = np.array(actions)
        rewards = np.array(rewards)
        next_states = np.array(next_states)

        # Predict Q-values for current and next states
        q_values = self.model.predict(states)
        next_q_values = self.model.predict(next_states)

        # Calculate target Q-values
        target_q_values = rewards + self.gamma * np.max(next_q_values, axis=1)

        # Update Q-values for the taken actions
        for i in range(len(batch)):
            q_values[i][actions[i]] = target_q_values[i]

        # Train the model
        self.model.fit(states, q_values, epochs=1, verbose=0) 

# ... (Game class and other functions remain the same) ...

# class KrypKasinoAI:
#     def __init__(self, hand, table):
#         self.hand = hand  # List of cards in the hand of the AI (list of Card objects)
#         self.table = table  # List of cards on the table
#         self.claimed_cards = [] # Array of the cards claimed by the AI.
#         self.points = 0 # The points that the AI has
#         return

#     def decision(self):
#         """
#         Decision logic: Play a card which will result in the least
#         amount of points earned at the end of the turn.
#         """
#         # Check if the AI has any card left
#         if not self.hand.cards:
#             print("AI has no cards to play!")
#             return None
#         best_card = None
#         best_claim = None
#         worst_claim = float('inf') # To avoid claims that result in getting points

#         for card in self.hand:
#             # Pass self.table.cards (the list of cards on the table)
#             can_claim, claim = cardcombos(card, self.table.cards)
#             if can_claim:
#                 # Calculate how many cards would be claimed if this card is played
#                 claim_size = len(claim)

#                 # AI should avoid claiming a card that would result in a lot of claimed cards
#                 if claim_size < worst_claim:
#                     worst_claim = claim_size
#                     best_card = card
#                     best_claim = claim

#         # If no card can be claimed (safe move), just play the card with the highest value
#         if best_card is None:
#             best_card = max(self.hand, key=lambda card: card.get_value()) # I have no clue what key=lambda card is

#         # Simulate playing the chosen card
#         self.play_card(best_card, best_claim)

#         # Print the AI's hand after making the decision
#         print(f"AI's hand after the decision: {self.hand}")

#         return best_card
    
    def play_card(self, card, claimed_cards=None):
        # Play the card first
        self.table.add_card(str(card))  # Add the card to the table
        self.hand.cards.remove(card)  # Remove the card from the hand's cards list
        print(f"AI plays: {card}")
    
        # Only handle claiming cards if a valid combination was found
        if claimed_cards:
            self.claimed_cards.extend(claimed_cards)
            print(f"AI claims: {', '.join(str(c) for c in claimed_cards)}")
        else:
            print(f"AI claims no cards.")

class Game:
    def __init__(self, num_players=2):
        self.num_players = num_players  # How many players are in the game
        self.turn = 0  # To track which player's turn it is (0 for Player 1, 1 for Player 2)
        self.players = ["AI", "Player 2"]  # List of players (assuming AI is player 1, but you can customize this)
        self.current_player = self.players[self.turn]  # This will hold the current player's name
        self.hand = Hand()  # Initialize player's hand
        self.table = Table()  # Initialize table

    def play_turn(self):
        """
        Simulate the action for the current player's turn.
        If it's the AI's turn, the AI will play a card.
        If it's the human player's turn, you may want to collect input (depending on how they interact with the game).
        """
        print(f"{self.current_player}'s turn:")
        
        if self.current_player == "AI":
            # Call the AI's decision-making function here
            ai = KrypKasinoAI(self.hand, self.table)
            ai.decision()
        else:
            # Handle human player's move (get input, etc.)
            print("Player 2's turn: Input move manually")
        
        # After each turn, switch to the next player
        self.next_turn()

    def human_turn(self):
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
def cardcombos(card, table_cards):
    card_value = card.get_value()  # Get the value of the card being played
    claim = []

    # Generate all possible combinations of the table cards
    for r in range(1, len(table_cards) + 1):  # r is the size of the combination
        for combination in itertools.combinations(table_cards, r):
            # Check if the sum of the combination of table cards matches the value of the card being played
            if sum(c.get_value() for c in combination) == card_value:
                claim = list(combination)  # Take this combination
                break  # We have found a valid combination, no need to continue the search

    # After finding a valid combination, check for all cards with the same rank on the table
    # Add all cards of the same rank (like 7s) to the claim
    matching_rank_cards = [c for c in table_cards if c.rank == card.rank]

    # Add the matching rank cards to the claim, ensuring no duplicates
    for card in matching_rank_cards:
        if card not in claim:
            claim.append(card)

    # Only claim the card if we found a valid combination (not just the played card)
    if claim:
        claim.append(card)  # Always claim the card played by the AI (which is also part of the claim)
        return True, claim
    
    return False, []  # Return False if no valid claim was found

hand = Hand() # AI's hand 
table = Table() # cards on the table

# This is a testing code to be used as a temporary input
# This is a dummy hand. There will be a maximum of four cards in the hand
# hand.add_card(["7S", "4H", "8C", "AH"])
hand.add_card(["7D", "5S"])
# This is a dummy table
# table.add_card(["7D", "8H", "7H", "5S"])
table.add_card(["7H","8H"])


# Now, set the location for all cards after they are added
hand.set_location()
table.set_location()

# Print the hand using the str method. The str method is used to print out a human-readable format
print("AI hand: ", str(hand))  # This will use Hand.__str__, which calls Card.__str__

# Get values of all cards in the hand
# for card in hand.cards:
#     print(f"{card}: Value = {card.get_value()}")

# Initialize AI and make a decision
ai = KrypKasinoAI(hand, table)
best_card = ai.decision()