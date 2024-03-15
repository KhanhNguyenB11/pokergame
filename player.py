from collections import Counter
class player:
    def __init__(self,name,money = 5000,highest = [0,0]):
        self.name = name
        self.highest = highest
        self.hand = []
        self.money = money

    def sort_hand_by_value(self,cards):
        return sorted(cards,key=lambda card: card.value)

    def highcard(self,cards):
        return sum(card.value for card in cards[:])

    def hasPair(self,hand, flop):
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

    def hasThree(self,hand, flop):
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

    def hasSquad(self, hand, flop):
        # Create a copy of the hand to avoid modifying the original list
        hand_copy = hand[:]
        # Extend the copy with the flop cards
        hand_copy.extend(flop)
        values = [card.value for card in hand_copy]
        value_counts = Counter(values)
        squad = [value for value, count in value_counts.items() if count >= 4]
        if squad:
            return max(squad)
        else:
            return None
    def hasFullHouse(self,hand,flop):
        three = self.hasThree(hand,flop)
        pair = self.hasPair(hand,flop)
        if three is not None and pair is not None:
            return [three,pair]
    def hasStraight(self,hand, flop):
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

    def hasFlush(self,hand, flop,nmax = 0):
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
                flush_cards = self.filter_by_suit(hand_copy, suit)
                if(nmax == 0):
                    return max(flush_cards, key=lambda x: x.value).value
                else:
                    flush_cards = self.sort_hand_by_value(flush_cards)
                    return flush_cards[-nmax].value
        return None


    def filter_by_suit(self,cards, target_suit):
        return [card for card in cards if card.suit == target_suit]
