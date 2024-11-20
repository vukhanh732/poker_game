# main.py

from game.game import Game

def main():
    player_name = input("Enter your name: ")
    try:
        num_bots = int(input("Enter the number of bots to play against: "))
        if num_bots < 1:
            raise ValueError("Number of bots must be at least 1.")
        if num_bots > 9:
            raise ValueError("Number of bots must be less than 9.")
    except ValueError as e:
        print("Invalid input. Using 2 bots by default.")
        num_bots = 2
        
    starting_chips = int(input("Enter the starting chip count for each player: "))
    bot_names = [f'Bot{i+1}' for i in range(num_bots)]
    game = Game(player_name, bot_names, starting_chips)
    game.play()

if __name__ == "__main__":
    main()