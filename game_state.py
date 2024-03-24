class game_state:
    def __init__(self, deck,current_bet = 0, round = 0):
        self.flop = []
        self.current_bet = current_bet
        self.round = round
        self.pot = 0
        self.highest_better = None
        self.active_player = None
        self.deck = deck