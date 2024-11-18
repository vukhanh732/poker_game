# game/player.py

class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        self.active = True

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def bet(self, amount):
        actual_bet = min(self.chips, amount)
        self.chips -= actual_bet
        return actual_bet