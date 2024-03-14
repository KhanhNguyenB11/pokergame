import deck
from player import player
from card import Card
deck = deck.Deck()
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
    player1.hand.append(deck.draw_card())
    player2.hand.append(deck.draw_card())

def isRoyal(cards):
    pass
def highcard(cards):
    return sum(card.value for card in cards[:2])


# Fake Scenario to test high card

v1 = highcard(player1.hand)
v2 = highcard(player2.hand)
print(v1)
print(v2)
