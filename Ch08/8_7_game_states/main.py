from game_state_demo import GameStateDemo


def main() -> int:
    game = GameStateDemo()

    if not game.init():
        game.free()

    game.run()

    return 0


if __name__ == '__main__':
    main()
