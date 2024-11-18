# Poker Game

This is a simple Texas Hold'em poker game implemented in Python. The game uses the `treys` library for hand evaluation.

## Features

- **Deck and Card Management**: A deck of cards is created, shuffled, and dealt to players.
- **Player Management**: Players can join the game, receive hole cards, and place bets.
- **Betting Rounds**: The game includes betting rounds for Pre-Flop, Flop, Turn, and River.
- **Community Cards**: Community cards are dealt and displayed for Flop, Turn, and River.
- **Hand Evaluation**: Hands are evaluated using the `treys` library to determine the winner.
- **Showdown**: At the end of the game, the winner is determined and the pot is awarded.

## Current Implementation

- **Deck and Card Classes**: Classes to manage the deck and individual cards.
- **Player Class**: A class to manage player information, including chips and hand.
- **Game Class**: The main game logic, including dealing cards, managing betting rounds, and determining the winner.

### Example Output
Hole Cards: Alice: [9 of Hearts, King of Spades] Bob: [10 of Diamonds, Ace of Clubs]

Pre-Flop Betting Round: Alice bets 10 chips. Bob bets 10 chips.

Flop: [4 of Diamonds, 2 of Clubs, 5 of Clubs]

Flop Betting Round: Alice bets 10 chips. Bob bets 10 chips.

Turn: Jack of Hearts

Turn Betting Round: Alice bets 10 chips. Bob bets 10 chips.

River: 3 of Spades

River Betting Round: Alice bets 10 chips. Bob bets 10 chips.

Showdown: Alice has [9 of Hearts, King of Spades] - High Card Bob has [10 of Diamonds, Ace of Clubs] - High Card

Bob wins the pot of 120 chips with High Card!


## Future Plans

- **Improved Betting Logic**: Implement more realistic betting logic, including raises, calls, and all-ins.
- **Player Actions**: Allow players to choose actions (bet, call, raise, fold) during betting rounds.
- **Hand History**: Keep a history of hands played and display it at the end of the game.
- **Graphical Interface**: Develop a graphical user interface (GUI) for a more interactive experience.
- **Multiplayer Support**: Allow multiple players to join the game over a network.
- **Advanced Hand Evaluation**: Improve hand evaluation to handle ties and edge cases more accurately.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/vukhanh732/poker_game.git
   cd poker_game
   ```

2. Create a virtual environment and activate it:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

4. Run the game:
```
python3 main.py
```