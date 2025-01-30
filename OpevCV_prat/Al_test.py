from itertools import combinations
from collections import Counter

def not_cards(array):
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

def combos(array):
    # Initialize a list to store sums
    possible_sums = []

    # Iterate over all possible numbers of elements to combine (1 to length of array)
    for r in range(1, len(array) + 1):
        # Generate all combinations of length r
        for combination in combinations(array, r):
            # Calculate the sum of the combination
            total = sum(combination)
            # Check if the sum is less than or equal to 16
            if total <= 16:
                possible_sums.append(total)

    # Count occurrences of each sum
    sum_counter = Counter(possible_sums)

    # Create a new list allowing occurrences of each value based on its original count in the input array
    limited_sums = []
    for value in sorted(sum_counter):
        limited_sums.extend([value] * sum_counter[value])

    return limited_sums

board_array = [2, 2, 5, 7]

print(not_cards(board_array))
print(combos(board_array))
