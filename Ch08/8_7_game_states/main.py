
# Entry point for running the game state demo
from game_state_demo import GameStateDemo

def main() -> int:
    # Create and initialize the game
    game = GameStateDemo()
    if not game.init():
        game.free()
    game.run()
    return 0

if __name__ == '__main__':
    main()
