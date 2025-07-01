
# Main entry point for the game engine
from game import Game

def main() -> int:
    # Create the game instance
    game = Game()
    if not game.init():
        game.free()
    game.run()
    return 0

if __name__ == '__main__':
    main()
