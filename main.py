# main.py

from game.game import Game

def main():
    player_names = ['Alice', 'Bob', 'Charlie']
    game = Game(player_names)
    game.play()

if __name__ == "__main__":
    main()
