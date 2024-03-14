from deck import Deck
from player import player
from collections import Counter

deck = Deck()
deck.shuffle()

player1 = player("p1")
player2 = player("p2")
flop = []

for _ in range(2):  # Drawing 2 cards
    player1.hand.append(deck.draw_card())
    print(f"{player1.name} Card: {player1.hand[-1].name}, Value: {player1.hand[-1].value}")
    player2.hand.append(deck.draw_card())
    print(f"{player2.name} Card: {player2.hand[-1].name}, Value: {player2.hand[-1].value}")

for _ in range(5):
    flop.append(deck.draw_card())
    print(f"Flop: {flop[-1].name}, Value: {flop[-1].value}")


def isRoyal(cards):
    pass
def highcard(cards):
    return sum(card.value for card in cards[:2])

def hasPair(hand,flop):
    # Create a copy of the hand to avoid modifying the original list
    hand_copy = hand[:]
    # Extend the copy with the flop cards
    hand_copy.extend(flop)
    values = [card.value for card in hand_copy]
    value_counts = Counter(values)
    pairs = [value for value, count in value_counts.items() if count >= 2]
    if pairs:
        return max(pairs)
    else:
        return None

def hasThree(hand,flop):
    # Create a copy of the hand to avoid modifying the original list
    hand_copy = hand[:]
    # Extend the copy with the flop cards
    hand_copy.extend(flop)
    values = [card.value for card in hand_copy]
    value_counts = Counter(values)
    three_of_a_kind = [value for value, count in value_counts.items() if count >= 3]
    if three_of_a_kind:
        return max(three_of_a_kind)
    else:
        return None


def hasStraight(hand, flop):
    # Create a copy of the hand to avoid modifying the original list
    hand_copy = hand[:]
    # Extend the copy with the flop cards
    hand_copy.extend(flop)

    # Extract values of the cards and sort them
    values = sorted([card.value for card in hand_copy])

    # Check for consecutive values
    for i in range(len(values) - 4):
        if values[i] + 4 == values[i + 4]:
            return values[i + 4]  # Return the highest value of the straight
    return None


def hasFlush(hand, flop):
    # Create a copy of the hand to avoid modifying the original list
    hand_copy = hand[:]
    # Extend the copy with the flop cards
    hand_copy.extend(flop)

    # Count the occurrences of each suit
    suit_counts = {}
    for card in hand_copy:
        suit = card.suit
        suit_counts[suit] = suit_counts.get(suit, 0) + 1

    # Check if any suit occurs five or more times
    for suit, count in suit_counts.items():
        if count >= 5:
            return suit  # Return the suit of the flush
    return None



