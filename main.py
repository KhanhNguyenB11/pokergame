from deck import Deck
from player import player
import socket
import threading


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
    return(f"Flop: {[card.name for card in flop]}")

def check_winner(pot):
        if len(player_list) == 1:
            print(f"{player_list[0].name} wins!!!\n +{pot}$")
            player_list[0].money += pot


def print_current_round(round_number):
    if round_number in poker_rounds:
        return f"Current Round:  {poker_rounds[round_number]}"
    else:
        return ("Invalid round number.")

def print_action(player, current_bet):
    print(f"\n{player.name}, select choice:")
    if current_bet == 0:
        return ("1.Bet  2.Fold  3.Check")
    else:
        return ("1.Call  2.Raise  3.Fold")
    player.print_name_of_hand()
    return (f"Your Money: {player.money}")


def game(player_list):
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
                    s = ""
                    if i != 0:
                        s+= print_name_of_flop(flop) + "\n"

                    s+= print_current_round(i) + "\n"
                    s+= print_action(player, current_bet) + "\n"
                    s+=(f"Current bet: {current_bet}") +"\n"
                    player.conn.sendall(s.encode())
                    data = player.conn.recv(1024).decode()
                    if data:
                        choice = data.split()[0]
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
                            player.conn.sendall("Invalid choice. Please select again.").encode()
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


HOST = 'localhost'  # Replace with actual server IP if needed
PORT = 65432

# Define dictionary to store connected clients and their room IDs
connected_clients = {}


def handle_client(conn, addr):
    """Handles communication with a connected client."""
    print(f'Connected by {addr}')
    current_player = None
    try:
        # Check for JOIN message format
        data = conn.recv(1024).decode()
        if data.startswith("JOIN"):
            try:
                room_id = int(data.split()[1])
                name = data.split()[3]
                # Create room if it doesn't exist
                if room_id not in connected_clients:
                    connected_clients[room_id] = []
                    # connected_clients[room_id].append()
                # Add client to the room
                current_player = player(name, conn)
                current_player.room = room_id
                if len(connected_clients[room_id]) == 0:
                    current_player.host = True
                    conn.sendall(f'{current_player.name} created room successfully!'.encode())
                else:
                    conn.sendall('Joined room successfully!'.encode())
                connected_clients[room_id].append(current_player)
                print(f'Client {addr} joined room {room_id}')
            except (ValueError, IndexError):
                conn.sendall('Invalid room ID format. Please use JOIN <number>'.encode())
                return  # Exit the loop on invalid format
            # ... remaining logic for messages within the room ...
        else:
            conn.sendall('Invalid message format.'.encode())
            return  # Exit the loop on invalid format
        # Broadcast messages to clients in the same room
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            # Print the received message (optional)
            print(f'Client {addr} in room {room_id}: {data}')
            room_clients = connected_clients.get(room_id)
            if data.endswith("START") and current_player.host == True and len(room_clients) > 1:
                data = "GAME START"
                game(room_clients)
            elif len(room_clients) < 2:
                data = "Not enough player"

            # Find room clients to broadcast to
            if room_clients:
                for client in room_clients:
                    try:
                        # Broadcast message with sender information
                        client.conn.sendall(f'{data}'.encode())
                    except ConnectionAbortedError:
                        print(f'Client {addr} disconnected unexpectedly.')
                        connected_clients[room_id].remove(client)

    except ConnectionError as e:
        print(f'Error communicating with client {addr}: {e}')
    finally:
        if current_player is not None:
            connected_clients[room_id].remove(current_player)
        conn.close()
        print(f'Client {addr} disconnected.')


def main():
    """Starts the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}')

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


if __name__ == '__main__':
    main()


