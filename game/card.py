# game/card.py

class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    TREYS_SUITS = {'Hearts': 'h', 'Diamonds': 'd', 'Clubs': 'c', 'Spades': 's'}
    TREYS_RANKS = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
                   '7': '7', '8': '8', '9': '9', '10': 'T',
                   'Jack': 'J', 'Queen': 'Q', 'King': 'K', 'Ace': 'A'}

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def to_treys_notation(self):
        return self.TREYS_RANKS[self.rank] + self.TREYS_SUITS[self.suit]

    def __repr__(self):
        return f"{self.rank} of {self.suit}"