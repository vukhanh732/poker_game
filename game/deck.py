# game/deck.py

import random
from .card import Card

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards=1):
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards left to deal")
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

    def __len__(self):
        return len(self.cards)