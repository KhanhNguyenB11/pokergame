from deck import Deck
from player import player
from card import Card


player1 = player("p1")
player2 = player("p2")
player_list = [player1,player2]

poker_ranks = {
    "High Card": 1,
    "One Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Squad": 8,
    "Straight Flush": 9,
    "Royal Flush": 10
}

poker_rounds = {
    0: "Preflop",
    1: "Flop",
    2: "Turn",
    3: "River",
    4: "Showdown"
}
def print_name_of_flop(flop):
    print("-"*30)
    print(f"Flop: {[card.name for card in flop]}")

def check_winner(pot):
        if len(player_list) == 1:
            print(f"{player_list[0].name} wins!!!\n +{pot}$")
            player_list[0].money += pot


def print_current_round(round_number):
    if round_number in poker_rounds:
        print("Current Round:", poker_rounds[round_number])
    else:
        print("Invalid round number.")

def print_action(player, current_bet):
    print(f"\n{player.name}, select choice:")
    if current_bet == 0:
        print("1.Bet  2.Fold  3.Check")
    else:
        print("1.Call  2.Raise  3.Fold")
    player.print_name_of_hand()
    print(f"Your Money: {player.money}")


def game():
    flop = []
    pot = 0
    small_blind = 5
    can_bet = True
    deck = Deck()
    deck.shuffle()
    dealCards(player_list, deck)

    # 5 rounds of poker loop
    for i in range(5):
        if len(player_list) == 1:
            print(f"{player_list[0].name} wins")
            player_list[0].money += pot
            break
        current_bet = 0
        if i == 0:
            make_pot(player_list, small_blind, pot)
            current_bet = small_blind * 2
        if i == 1:
            flop_deal(flop, deck)
        elif i == 2 or i == 3:
            flop.append(deck.draw_card())
        #last round
        elif i == 4:
            winner = showdown(player_list, flop)
            if type(winner) is list:
                for player in winner:
                    print(f"{player.name} wins")
                    player.money += pot//len(winner)
            else:
                print(f"{winner.name} wins")
                winner.money += pot
            break

        # loop stop if its go back to highest_better
        highest_better = None
        active_player = player_list[0]
        # loop to end round if all players have checked or called the highest raise/bet
        while highest_better is not active_player:
            # players action
            for player in player_list:
                if len(player_list) == 1:
                    break
                if not highest_better:
                    highest_better = player_list[0]
                # loop to check for invalid action
                while True:
                    if i != 0:
                        print_name_of_flop(flop)
                    print_current_round(i)
                    print_action(player, current_bet)
                    print(f"Current bet: {current_bet}")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        if current_bet != 0:
                            player.call(current_bet)
                            break
                        else:
                            bet_amount = int(input("Enter the amount: "))
                            if bet_amount < current_bet:
                                print("Amount not valid!")
                                continue
                            else:
                                player.bet(bet_amount)
                                current_bet = bet_amount
                                highest_better = player
                                break
                    elif choice == "2":
                        if current_bet == 0:
                            player.fold()
                        bet_amount = int(input("Enter the amount: "))
                        if bet_amount < current_bet:
                            print("Amount not valid!")
                            continue
                        else:
                            player.bet(bet_amount)
                            current_bet = bet_amount
                            highest_better = player
                            break
                    elif choice == "3":
                        if current_bet > 0:
                            player.fold()
                            player_list.remove(player)
                            break
                        else:
                            print(f"{player.name} check")
                            break
                    elif choice == "4":
                        if current_bet == 0:
                            pass
                            break
                        else:
                            player.fold()
                            player_list.remove(player)
                            break
                    else:
                        print("Invalid choice. Please select again.")
                        print("-" * 20)
                        continue


def make_pot(player_list,small_blind,pot):
    small = player_list[0]
    big = player_list[1]
    small.money -= small_blind
    big.money -= small_blind * 2
    small.initial_bet = small_blind
    big.initial_bet = small_blind * 2
    pot += small_blind*3

# args: a list of players and flop cards
# return: a list of winner
def showdown(players,flop):
    for player in players:
        player.determine_highest(flop)
    # Sort players by the rank of their highest hands
    players.sort(key=lambda x: (x.highest[0]), reverse=True)
    highest_hand = players[0].highest[0]
    # Check if there's a single winner
    highest_players = filter_by_highest_hand(players, highest_hand)
    if len(highest_players) == 1:
        return highest_players[0]
    # more than 2 players have the same rank
    else:
        # royal flush
        if highest_hand == 14:
            return highest_players
        # straight and straight flush
        elif highest_hand == 5 or highest_hand == 9:
            return find_player_with_n_highest_value(highest_players)
        # squad
        elif highest_hand == 8:
            highest_players = find_player_with_n_highest_value(highest_players)
            if len(highest_players) == 1:
                return highest_players
            # if there are players that have the same value and rank, then we compare their high card
            else:
                return compare_high_cards(highest_players, flop, 1)
        # full house
        elif highest_hand == 7:
            highest_players = find_player_with_n_highest_value(highest_players)
            if len(highest_players) == 1:
                return highest_players
            else:
                return find_player_with_n_highest_value(highest_players, 1)
        # flush
        elif highest_hand == 6:
            for i in range(5):
                highest_players = find_player_with_n_highest_value(highest_players, i)
                if len(highest_players) == 1:
                    return highest_players
            return highest_players
        # 2 pairs
        elif highest_hand == 3:
            highest_players = find_player_with_n_highest_value(highest_players)
            if len(highest_players) == 1:
                return highest_players
            else:
                highest_players = find_player_with_n_highest_value(highest_players, 1)
                # if there are players that have the same value and rank, then we compare their high card
                return compare_high_cards(highest_players, flop, 1)
        # three
        elif highest_hand == 4:
            highest_players = find_player_with_n_highest_value(highest_players)
            if len(highest_players) == 1:
                return highest_players
            # if there are players that have the same value and rank, then we compare their high card
            else:
                return compare_high_cards(highest_players, flop, 2)
        # pair
        elif highest_hand == 2:
            highest_players = find_player_with_n_highest_value(highest_players)
            if len(highest_players) == 1:
                return highest_players
            # if there are players that have the same value and rank, then we compare their high card
            else:
                return compare_high_cards(highest_players, flop, 3)
        # high card
        elif highest_hand == 1:
            return compare_high_cards(highest_players,flop,7)


def compare_high_cards(highest_players, flop, number_of_high_cards):
    # calculate high card by removing best hand combination
    for player in highest_players:
        if player.highest[0] == 1:
            pass
        else:
            player.highest = [1,player.highcard(player.highest[1], flop, number_of_high_cards)]
    for i in range(number_of_high_cards):
        highest_players = find_player_with_n_highest_value(highest_players, i)
        if len(highest_players) == 1:
            return highest_players
    return highest_players


def find_player_with_n_highest_value(players, n=0):
    highest_value = 0
    for player in players:
        if type(player.highest[1][n]) is int:
            if player.highest[1][n] >= highest_value:
                highest_value = player.highest[1][n]
        else:
            if player.highest[1][n].value >= highest_value:
                highest_value = player.highest[1][n].value
    if type(players[0].highest[1][n]) is int:
        return [p for p in players if p.highest[1][n] >= highest_value]
    return [p for p in players if p.highest[1][n].value >= highest_value]


def filter_by_value(players,value):
    return [player for player in players if player.highest[1][0] == value]


def dealCards(p_list,deck):
    for player in p_list:
        for _ in range(2):
            player.hand.append(deck.draw_card())


def flop_deal(flop,deck):
    for _ in range(3):
        flop.append(deck.draw_card())


def filter_by_highest_hand(players, target):
    return [player for player in players if player.highest[0] == target]


game()


# testing
# hand = [Card('5', 5, 'Clubs'),Card('5', 5, 'fdaf'),Card('2', 8, 'sac'), Card('3', 11, 'Diamonds'), Card('7', 3, 'zzz')]
# player1.hand = [Card('5', 5, 'Clubs'),Card('5', 8, 'Clubs')]
# player2.hand = [Card('5', 5, 'Clubs'),Card('5', 8, 'Clubs')]
# test = showdown([player1, player2], hand)
# print(test)
