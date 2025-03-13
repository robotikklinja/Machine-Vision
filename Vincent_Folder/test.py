import itertools


def cardcombos(card, table_cards):
    card_value = card.get_value()  # Get the value of the card being played
    all_combinations = [] # Store all valid combinations in an array

    for r in range(1, len(table_cards) + 1):
        for combination in itertools.combinations(table_cards, r):
            if sum(c.get_value() for c in combination) == card_value:
                all_combinations.append(list(combination))

    return all_combinations

card = []
table_cards = []

print(cardcombos(card, table_cards))