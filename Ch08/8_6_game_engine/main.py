from game import Game


def main() -> int:
    game = Game()

    if not game.init():
        game.free()

    game.run()

    return 0


if __name__ == '__main__':
    main()
