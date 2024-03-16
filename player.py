from collections import Counter
class player:
    def __init__(self,name,money = 5000):
        self.name = name
        self.highest = []
        self.hand = []
        self.money = money

    def print_value_of_hand(self,cards):
        values = [card.value for card in self.hand]
        print(values)

    def print_name_of_hand(self):
        print(f"Your hand: {[card.name for card in self.hand]}")
    def sort_hand_by_value(self,cards):
        return sorted(cards,key=lambda card: card.value)

    def highcard(self,cards):
        return sum(card.value for card in cards[:])

    def hasStraightFlush(self, hand, flop):
        # Check if the player has a flush
        flush_value = self.hasFlush(hand, flop)
        if flush_value:
            # Check if the player has a straight within the flush cards
            flush_cards = self.filter_by_suit(hand + flop, flush_value.suit)
            straight_value = self.hasStraight(flush_cards, [])
            if straight_value:
                return straight_value  # Return the value of the highest card in the straight flush
        return None


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

    def has2pairs(self, hand, flop):
        # Create a copy of the hand to avoid modifying the original list
        hand_copy = hand[:]
        # Extend the copy with the flop cards
        hand_copy.extend(flop)

        values = [card.value for card in hand_copy]
        value_counts = Counter(values)

        pairs = [value for value, count in value_counts.items() if count >= 2]

        if len(pairs) >= 2:
            return sorted(pairs, reverse=True)[:2]  # Return the two highest pairs
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
                if nmax == 0:
                    return max(flush_cards, key=lambda x: x.value)
                else:
                    flush_cards = self.sort_hand_by_value(flush_cards)
                    return flush_cards[-nmax].value
        return None

    def fold(self,current_bet):
        self.money -= current_bet

    def call(self, current_bet):
        if self.money >= current_bet:
            print(f"{self.name} calls the bet of {current_bet}.")
            self.money -= current_bet
            return True
        else:
            print(f"{self.name} doesn't have enough chips to call. They go all-in with {self.money} chips.")
            self.money = 0
            return False

    def bet(self, amount):
        if self.money >= amount:
            print(f"{self.name} bets {amount} money.")
            self.money -= amount
            return amount
        else:
            print(f"{self.name} doesn't have enough money to bet. They go all-in with {self.money} chips.")
            bet_all_in = self.money
            self.money = 0
            return bet_all_in

    def filter_by_suit(self,cards, target_suit):
            return [card for card in cards if card.suit == target_suit]

    def determine_highest(self, flop):
        hand = self.hand
        # Check for various hand combinations starting from the strongest
        straight_flush = self.hasStraightFlush(hand,flop)
        if straight_flush:
            if straight_flush == 14:
                self.highest = ("Royal Flush", straight_flush)
            else:
                self.highest = ("Straight Flush", straight_flush)
            return

        squad = self.hasSquad(hand, flop)
        if squad:
            self.highest = ("Squad", squad)
            return

        full_house = self.hasFullHouse(hand, flop)
        if full_house:
            self.highest = ("Full House", full_house)
            return

        flush = self.hasFlush(hand, flop)
        if flush:
            self.highest = ("Flush", flush.value)
            return

        straight = self.hasStraight(hand, flop)
        if straight:
            self.highest = ("Straight", straight)
            return

        three_of_a_kind = self.hasThree(hand, flop)
        if three_of_a_kind:
            self.highest = ("Three of a Kind", three_of_a_kind)
            return

        two_pairs = self.has2pairs(hand,flop)
        if two_pairs:
            self.highest = ["Two Pairs",two_pairs]
            return

        pair = self.hasPair(hand, flop)
        if pair:
            self.highest = ("Pair", pair)
            return

        # If no strong hand is found, determine high card
        high_card = self.highcard(hand)
        self.highest = ("High Card", high_card)


