class player:
    def __init__(self,name,money = 5000,highest = [0,0]):
        self.name = name
        self.highest = highest
        self.hand = []
        self.money = money

    def sort_hand_by_value(self):
        self.hand.sort(key=lambda card: card.value)