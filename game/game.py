# game/game.py
import random
from .deck import Deck
from .player import Player
from treys import Evaluator, Card as TreysCard, Deck as TreysDeck

class Game:
    def __init__(self, player_name, bot_names, starting_chips=1000):
        self.players = [Player(player_name, chips=starting_chips)]
        self.players += [Player(name, chips=starting_chips, is_bot=True) for name in bot_names]
        self.evaluator = Evaluator()
        self.hand_history = []
        self.dealer_index = 0

    def start_round(self):
        self.assign_positions()
        self.deck = Deck()
        self.pot = 0
        self.community_cards = []
        for player in self.players:
            player.hand = []
            player.active = True
            player.current_bet = 0

        self.collect_blinds()

    def collect_blinds(self):
        small_blind = 5  # Set blind amounts
        big_blind = 10

        for player in self.players:
            if player.position == 'Small Blind':
                amount = player.bet(small_blind)
                self.pot += amount
                print(f"{player.name} posts small blind of {amount} chips.")
            elif player.position == 'Big Blind':
                amount = player.bet(big_blind)
                self.pot += amount
                print(f"{player.name} posts big blind of {amount} chips.")

    def deal_hole_cards(self):
        for player in self.players:
            player.receive_cards(self.deck.deal(2))
        print("\nHole Cards:")
        for player in self.players:
            print(f"{player.name}: {player.hand}")

    def betting_round(self, round_name):
        print(f"\n{round_name} Betting Round:")
        active_players = [player for player in self.players if player.active and player.chips > 0]
        current_bet = max(player.current_bet for player in self.players)
        actions_taken = False

        # Determine the starting index based on the round
        if round_name == "Pre-Flop":
            # First betting round starts with the player after the big blind
            start_index = (self.dealer_index + 3) % len(self.players)
        else:
            # Post-flop rounds start with the player after the dealer
            start_index = (self.dealer_index + 1) % len(self.players)

        betting_order = self.players[start_index:] + self.players[:start_index]

        while True:
            for player in betting_order:
                if not player.active or player.chips == 0:
                    continue

                # Check if betting can end
                if all(p.current_bet == current_bet for p in active_players if p.active):
                    if actions_taken:
                        break  # Betting round ends when all bets are equal

                print(f"\n{player.name}'s turn ({player.position}).")
                print(f"Current bet: {current_bet}, Your bet: {player.current_bet}")
                print(f"Chips: {player.chips}, Pot: {self.pot}")

                if player.is_bot:
                    action = self.get_bot_action(player, current_bet)
                    # Handle bot's action and print their decisions
                    self.handle_bot_action(player, action, current_bet)
                else:
                    action = self.get_player_action(player, current_bet)
                    # Handle player's action
                    self.handle_player_action(player, action, current_bet)

                actions_taken = True
                current_bet = max(p.current_bet for p in self.players if p.active)

            active_players = [p for p in self.players if p.active and p.chips > 0]
            if len(active_players) <= 1 or all(
                p.current_bet == current_bet for p in active_players if p.active
            ):
                break

        for player in self.players:
            player.reset_bet()

    def get_player_action(self, player, current_bet):
        if current_bet == 0:
            valid_actions = ['check', 'bet']
        elif player.current_bet < current_bet:
            valid_actions = ['fold', 'call', 'raise']
        else:
            valid_actions = ['check', 'raise']

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
        self.record_hand(winner, hand_name)

    def check_for_winner(self):
        active_players = [p for p in self.players if p.active]
        if len(active_players) == 1:
            winner = active_players[0]
            print(f"\nAll other players folded. {winner.name} wins the pot of {self.pot} chips!")
            winner.chips += self.pot
            return True
        return False

    def record_hand(self, winner, hand_name):
        hand_details = {
            'winner': winner.name,
            'winning_hand': hand_name,
            'pot': self.pot,
            'community_cards': self.community_cards.copy(),
            'players': []
        }
        for player in self.players:
            player_info = {
                'name': player.name,
                'hand': player.hand.copy(),
                'final_hand': self.evaluate_hand(player.hand)[1],
                'active': player.active
            }
            hand_details['players'].append(player_info)
        self.hand_history.append(hand_details)

    def show_hand_history(self):
        print("\nHand History:")
        for i, hand in enumerate(self.hand_history, 1):
            print(f"\nHand {i}:")
            print(f"Winner: {hand['winner']} with {hand['winning_hand']}")
            print(f"Pot: {hand['pot']} chips")
            print(f"Community Cards: {hand['community_cards']}")
            print("Players:")
            for player in hand['players']:
                status = '(Folded)' if not player['active'] else ''
                print(f"  {player['name']}: {player['hand']} - {player['final_hand']} {status}")

    def remove_busted_players(self):
        self.players = [player for player in self.players if player.chips > 0 or not player.is_bot]
        if len(self.players) == 1:
            print(f"\n{self.players[0].name} has won all the chips!")
            exit()

    def get_bot_action(self, player, current_bet):
        hand_strength = self.evaluate_hand_strength(player)
        random_factor = random.uniform(-0.1, 0.1)
        adjusted_strength = hand_strength + random_factor

        if current_bet == 0:
            # No bets yet; decide between check or bet
            if adjusted_strength > 0.6:
                return 'bet'
            else:
                return 'check'
        else:
            if adjusted_strength > 0.7:
                return 'raise'
            elif adjusted_strength > 0.4:
                return 'call'
            else:
                return 'fold'

    def evaluate_hand_strength(self, player):
        evaluator = Evaluator()
        hole_cards = [self.card_to_treys(card) for card in player.hand]
        community_cards = [self.card_to_treys(card) for card in self.community_cards]

        if not self.community_cards:
            # Pre-flop hand strength estimation
            strength = self.preflop_hand_strength(player)
        else:
            # Post-flop hand evaluation
            all_cards = community_cards + hole_cards
            rank = evaluator.evaluate(community_cards, hole_cards)
            max_rank = 7462  # Maximum possible rank in treys
            strength = 1 - (rank / max_rank)  # Normalize to [0,1], higher is better

        return strength
    
    def play(self):
         while True:
            self.start_round()
            self.deal_hole_cards()
            self.betting_round("Pre-Flop")
            if self.check_for_winner():
                if not self.continue_game():
                    break
                else:
                    continue
            self.deal_flop()
            self.betting_round("Flop")
            if self.check_for_winner():
                if not self.continue_game():
                    break
                else:
                    continue
            self.deal_turn()
            self.betting_round("Turn")
            if self.check_for_winner():
                if not self.continue_game():
                    break
                else:
                    continue
            self.deal_river()
            self.betting_round("River")
            if self.check_for_winner():
                if not self.continue_game():
                    break
                else:
                    continue
            self.determine_winner()
            self.remove_busted_players()
            if not self.continue_game():
                break

    def continue_game(self):
        player = self.players[0]  # Human player is always the first in the list
        if player.chips == 0:
            print(f"\n{player.name}, you have lost all your chips. Game over!")
            return False
        elif len(self.players) == 1 and self.players[0] == player:
            print(f"\nCongratulations {player.name}, you have won all the chips!")
            return False
        else:
            return True
        
    def assign_positions(self):
        num_players = len(self.players)
        # Rotate dealer
        self.dealer_index = (self.dealer_index) % num_players
        positions = ['Dealer', 'Small Blind', 'Big Blind']
        # Add other positions based on number of players
        if num_players > 3:
            positions += ['UTG'] + ['Middle Position'] * (num_players - 4)
        # Assign positions to players
        for i, player in enumerate(self.players):
            player.position = positions[i % len(positions)]

    def handle_bot_action(self, player, action, current_bet):
        if action == 'fold':
            player.fold()
            print(f"{player.name} folds.")
        elif action == 'call':
            bet = current_bet - player.current_bet
            self.pot += player.bet(bet)
            print(f"{player.name} calls {bet} chips.")
        elif action == 'raise':
            bet = current_bet - player.current_bet
            raise_amount = self.get_bot_raise_amount(player, current_bet)
            total_bet = bet + raise_amount
            current_bet += raise_amount
            self.pot += player.bet(total_bet)
            print(f"{player.name} raises by {raise_amount} chips. Total bet: {current_bet}")
        elif action == 'bet':
            bet_amount = self.get_bot_bet_amount(player)
            current_bet = bet_amount
            self.pot += player.bet(bet_amount)
            print(f"{player.name} bets {bet_amount} chips. Current bet is now {current_bet}")
        elif action == 'check':
            print(f"{player.name} checks.")

    def get_bot_bet_amount(self, player):
        min_bet = 10
        max_bet = min(100, player.chips)
        bet_amount = random.randint(min_bet, max_bet)
        return bet_amount

    def get_bot_raise_amount(self, player, current_bet):
        min_raise = 10
        max_raise = min(100, player.chips - (current_bet - player.current_bet))
        raise_amount = random.randint(min_raise, max_raise)
        return raise_amount

    def handle_player_action(self, player, action, current_bet):
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
            print(f"{player.name} raises by {raise_amount} chips. Total bet: {current_bet}")
        elif action == 'bet':
            bet_amount = self.get_bet_amount(player, min_bet=10)
            current_bet = bet_amount
            self.pot += player.bet(bet_amount)
            print(f"{player.name} bets {bet_amount} chips. Current bet is now {current_bet}")
        elif action == 'check':
            print(f"{player.name} checks.")

    def get_bet_amount(self, player, min_bet):
        while True:
            try:
                amount = int(input(f"Enter bet amount (minimum {min_bet}): "))
                if amount >= min_bet and amount <= player.chips:
                    return amount
                else:
                    print(f"Invalid amount. Enter a value between {min_bet} and {player.chips}.")
            except ValueError:
                print("Please enter a numeric value.")

    def preflop_hand_strength(self, player):
        card_ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                      '7': 7, '8': 8, '9': 9, '10': 10,
                      'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
        ranks = [card_ranks[card.rank] for card in player.hand]
        suits = [card.suit for card in player.hand]
        pair = ranks[0] == ranks[1]
        suited = suits[0] == suits[1]
        high_card = max(ranks)
        low_card = min(ranks)

        # Simple heuristic for pre-flop strength
        if pair:
            strength = 0.8 + (high_card / 14) * 0.2  # Pairs are strong
        elif suited and high_card >= 10:
            strength = 0.6 + (high_card / 14) * 0.2  # High suited cards
        elif high_card >= 12:
            strength = 0.5 + (high_card / 14) * 0.2  # High cards
        elif suited:
            strength = 0.4 + (high_card / 14) * 0.1  # Suited cards
        else:
            strength = 0.2 + (high_card / 14) * 0.1  # Others

        return strength
    
    def card_to_treys(self, card):
        rank_translation = {'10': 'T', 'Jack': 'J', 'Queen': 'Q', 'King': 'K', 'Ace': 'A'}
        rank = rank_translation.get(card.rank, card.rank)
        suit_translation = {'Hearts': 'h', 'Diamonds': 'd', 'Clubs': 'c', 'Spades': 's'}
        suit = suit_translation[card.suit]
        return TreysCard.new(f"{rank}{suit}")