# game/player.py

class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        self.active = True
        self.current_bet = 0  # Track player's bet in the current round

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def bet(self, amount):
        bet_amount = min(self.chips, amount)
        self.chips -= bet_amount
        self.current_bet += bet_amount
        return bet_amount

    def reset_bet(self):
        self.current_bet = 0

    def fold(self):
        self.active = False