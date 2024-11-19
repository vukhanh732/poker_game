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
        active_players = [player for player in self.players if player.active and player.chips > 0]
        current_bet = 0
        last_bettor = None

        while True:
            actions_taken = False
            for player in active_players:
                if not player.active or player.chips == 0:
                    continue
                if all(p.current_bet == current_bet for p in active_players if p.active):
                    if actions_taken:
                        break  # Betting round ends when all bets are equal
                print(f"\n{player.name}'s turn. Current bet: {current_bet}, Your bet: {player.current_bet}")
                print(f"Chips: {player.chips}, Pot: {self.pot}")
                action = self.get_player_action(player, current_bet)
                if action == 'fold':
                    player.fold()
                    print(f"{player.name} folds.")
                elif action == 'call':
                    bet = current_bet - player.current_bet
                    self.pot += player.bet(bet)
                    print(f"{player.name} calls {bet} chips.")
                elif action == 'raise':
                    bet = current_bet - player.current_bet
                    raise_amount = self.get_raise_amount(player, min_raise=10)
                    total_bet = bet + raise_amount
                    current_bet += raise_amount
                    self.pot += player.bet(total_bet)
                    last_bettor = player
                    print(f"{player.name} raises by {raise_amount} chips. Total bet: {current_bet}")
                elif action == 'check':
                    print(f"{player.name} checks.")
                actions_taken = True

            active_players = [p for p in self.players if p.active and p.chips > 0]
            if len(active_players) <= 1 or all(p.current_bet == current_bet for p in active_players):
                break

        for player in self.players:
            player.reset_bet()

    def get_player_action(self, player, current_bet):
        if player.current_bet < current_bet:
            valid_actions = ['fold', 'call', 'raise']
        else:
            valid_actions = ['check', 'raise', 'fold']

        while True:
            action = input(f"{player.name}, choose an action ({'/'.join(valid_actions)}): ").lower()
            if action in valid_actions:
                return action
            else:
                print("Invalid action. Please try again.")

    def get_raise_amount(self, player, min_raise):
        while True:
            try:
                amount = int(input(f"Enter raise amount (minimum {min_raise}): "))
                if amount >= min_raise and amount <= player.chips:
                    return amount
                else:
                    print(f"Invalid amount. Enter a value between {min_raise} and {player.chips}.")
            except ValueError:
                print("Please enter a numeric value.")

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

    def check_for_winner(self):
        active_players = [p for p in self.players if p.active]
        if len(active_players) == 1:
            winner = active_players[0]
            print(f"\nAll other players folded. {winner.name} wins the pot of {self.pot} chips!")
            winner.chips += self.pot
            return True
        return False

    def play(self):
        self.start_round()
        self.deal_hole_cards()
        self.betting_round("Pre-Flop")
        if self.check_for_winner():
            return
        self.deal_flop()
        self.betting_round("Flop")
        if self.check_for_winner():
            return
        self.deal_turn()
        self.betting_round("Turn")
        if self.check_for_winner():
            return
        self.deal_river()
        self.betting_round("River")
        if self.check_for_winner():
            return
        self.determine_winner()

