from deck import Deck
from player import player
from card import Card
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
full_house_cards_2 = [
    Card("Ace", 14, "Hearts"),
    Card("Ace", 14, "Clubs")
]

full_house_cards_5 = [
    Card("King", 13, "Hearts"),
    Card("King", 13, "Clubs"),
    Card("King", 13, "Diamonds"),
    Card("Ace", 13, "Spades"),
    Card("Ace", 10, "Diamonds")
]
player2.hand = full_house_cards_2
flop = full_house_cards_5
print(player2.hasSquad(player2.hand,flop))



