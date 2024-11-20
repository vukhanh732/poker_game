# game/player.py

class Player:
    def __init__(self, name, chips=1000, is_bot=False):
        self.name = name
        self.chips = chips
        self.hand = []
        self.active = True
        self.current_bet = 0
        self.is_bot = is_bot
        self.position = None  # Position at the table

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def bet(self, amount):
        bet_amount = min(self.chips, amount)
        self.chips -= bet_amount
        self.current_bet += bet_amount
        if self.chips == 0:
            print(f"{self.name} is all-in!")
        return bet_amount

    def reset_bet(self):
        self.current_bet = 0

    def fold(self):
        self.active = False