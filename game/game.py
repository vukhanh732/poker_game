# game/game.py

from .deck import Deck
from .player import Player
from treys import Evaluator, Card as TreysCard, Deck as TreysDeck

class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.evaluator = Evaluator()

    def start_round(self):
        self.deck = Deck()
        self.pot = 0
        self.community_cards = []
        for player in self.players:
            player.hand = []
            player.active = True

    def deal_hole_cards(self):
        for player in self.players:
            player.receive_cards(self.deck.deal(2))
        print("\nHole Cards:")
        for player in self.players:
            print(f"{player.name}: {player.hand}")

    def betting_round(self, round_name):
        print(f"\n{round_name} Betting Round:")
        for player in self.players:
            if player.active and player.chips > 0:
                bet_amount = min(10, player.chips)
                self.pot += player.bet(bet_amount)
                print(f"{player.name} bets {bet_amount} chips.")
            else:
                player.active = False
                print(f"{player.name} folds.")

    def deal_flop(self):
        self.community_cards.extend(self.deck.deal(3))
        print(f"\nFlop: {self.community_cards}")

    def deal_turn(self):
        card = self.deck.deal(1)[0]
        self.community_cards.append(card)
        print(f"\nTurn: {card}")

    def deal_river(self):
        card = self.deck.deal(1)[0]
        self.community_cards.append(card)
        print(f"\nRiver: {card}")

    def evaluate_hand(self, hand):
        treys_hand = [TreysCard.new(card.to_treys_notation()) for card in hand]
        treys_community = [TreysCard.new(card.to_treys_notation()) for card in self.community_cards]
        rank = self.evaluator.evaluate(treys_community, treys_hand)
        hand_class = self.evaluator.get_rank_class(rank)
        hand_name = self.evaluator.class_to_string(hand_class)
        return rank, hand_name

    def determine_winner(self):
        print("\nShowdown:")
        best_rank = None
        winners = []
        for player in self.players:
            if player.active:
                rank, hand_name = self.evaluate_hand(player.hand)
                print(f"{player.name} has {player.hand} - {hand_name}")
                if best_rank is None or rank < best_rank:
                    best_rank = rank
                    winners = [player]
                elif rank == best_rank:
                    winners.append(player)
        if len(winners) == 1:
            winner = winners[0]
            print(f"\n{winner.name} wins the pot of {self.pot} chips with {hand_name}!")
            winner.chips += self.pot
        else:
            split_pot = self.pot // len(winners)
            winner_names = ', '.join(winner.name for winner in winners)
            print(f"\nTie between {winner_names}, pot is split. Each wins {split_pot} chips.")
            for winner in winners:
                winner.chips += split_pot

    def play(self):
        self.start_round()
        self.deal_hole_cards()
        self.betting_round("Pre-Flop")
        self.deal_flop()
        self.betting_round("Flop")
        self.deal_turn()
        self.betting_round("Turn")
        self.deal_river()
        self.betting_round("River")
        self.determine_winner()