from deck import Deck
from player import player
from card import Card
deck = Deck()
deck.shuffle()

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
    print(f"Flop: {[card.name for card in flop]}")

def check_winner(pot):
        if len(player_list) == 1:
            print(f"{player_list[0].name} wins!!!\n +{pot}$")
            player_list[0].money += pot

def print_action(player):
    print(f"\n{player.name}, select choice:")
    print("1.Fold")
    print("2.Bet")
    print("3.Call")
    print("4.Check")
    player.print_name_of_hand()
def game():
    dealCards(player_list)
    pot = 0
    # ante amount
    current_bet = 10
    make_ante(player_list,current_bet,pot)
    for i in range(5):
        if(i == 1):
            flopdeal(flop)
            print_name_of_flop(flop)
        while len(player_list) > 1:
            for player in player_list:
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


def make_ante(player_list,amount,pot):
    for player in player_list:
        player.money -= amount
        pot += amount
def reset_game():
    flop = []
    current_bet = 0
    pot = 0
def dealCards(p_list):
    for player in p_list:
        for _ in range(2):
            player.hand.append(deck.draw_card())
def flopdeal(flop):
    for _ in range(3):
        flop.append(deck.draw_card())


game()

