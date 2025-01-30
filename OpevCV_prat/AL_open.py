
num_players = 2
def play(num_players):

    players = {}  # Dictionary to store players

    for i in range(num_players): 
        player_name = f"Player {i+1}"
        players[f"Player_{i+1}"] = player_name

    # Loop through the players 
    for key, value in players.items():
        print(f"{key}: 4 Cards ")

    return None

def generate_player_names(num_players):
    """
    Generate names for players in the format P1, P2, ...

    Parameters:
        num_players (int): The number of players to generate names for.

    Returns:
        list: A list of player names.
    """
    return [f"OP_{i+1}" for i in range(num_players)]

# Example usage 
num_players = 5  # Change this to the desired number of players
player_names = generate_player_names(num_players)
print(player_names)

random_hand = ["2D", "3H", "JC", "7D"]



for i in range(len(player_names)):
    player_names[i] = random_hand
    print(player_names[i])
    
