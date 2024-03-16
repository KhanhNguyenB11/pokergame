from deck import Deck
from player import player
from card import Card


player1 = player("p1")
player2 = player("p2")
player_list = [player1,player2]
flop = []
poker_ranks = {
    "High Card": 1,
    "One Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9,
    "Royal Flush": 10
}
def print_name_of_flop(flop):
    print("-"*30)
    print(f"Flop: {[card.name for card in flop]}")

def check_winner(pot):
        if len(player_list) == 1:
            print(f"{player_list[0].name} wins!!!\n +{pot}$")
            player_list[0].money += pot

def print_action(player):
    print(f"\n{player.name}, select choice:")
    print("1.Fold  2.Bet  3.Call 4.Check")
    player.print_name_of_hand()
    print(f"Your Money: {player.money}")
def game():

    pot = 0
    # ante amount
    current_bet = 0
    small_blind = 5
    deck = Deck()
    deck.shuffle()
    make_pot(player_list,small_blind,pot)
    dealCards(player_list, deck)
    for i in range(5):
        if i == 1:
            flopdeal(flop, deck)
        elif i > 1:
            flop.append(deck.draw_card())
        for player in player_list:
            if i != 0:
                print_name_of_flop(flop)
            print_action(player)
            choice = input("Enter your choice: ")
            if choice == "1":
                player.fold(current_bet)
                player_list.remove(player)
            elif choice == "2":
                bet_amount = int(input("Enter the bet amount: "))
                player.bet(current_bet)
            elif choice == "3":
                player.call(current_bet)
            elif choice == "4":
                pass
            else:
                print("Invalid choice. Please select again.")
                print("-"*20)
                print_action(player)
                choice = input("Enter your choice: ")


def make_pot(player_list,small_blind,pot):
    small = player_list[0]
    big = player_list[1]
    small.money -= small_blind
    big.money -= small_blind * 2
    pot += small_blind*3

def reset_game():
    flop = []
    current_bet = 0
    pot = 0
def dealCards(p_list,deck):
    for player in p_list:
        for _ in range(2):
            player.hand.append(deck.draw_card())
def flopdeal(flop,deck):
    for _ in range(3):
        flop.append(deck.draw_card())


game()


