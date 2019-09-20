import pygame, sys, os, random
from graphics import Graphics

FPS = 30
FRAME_TIME = 1000 / FPS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FULLSCREEN = False

graphics = Graphics()


def rand() -> int:
    return random.randint(0, 32768)


def init_program() -> None:
    pygame.init()

    if not graphics.init(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN):
        return False

    pygame.display.set_caption("Graphics Test")

    return True


def free_program() -> None:
    pygame.quit()


def program_is_running() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False

    return True


def main() -> bool:
    if not init_program():
        free_program()
        return False

    counter = 0

    while program_is_running():
        frame_start = pygame.time.get_ticks()

        counter += 1

        if counter > 90:
            counter = 0
            graphics.clear(rand() % 255, rand() % 255, rand() % 255)

        for i in range(100):
            graphics.draw_pixel(
                rand() % SCREEN_WIDTH, rand() % SCREEN_HEIGHT,
                rand() % 255, rand() % 255, rand() % 255)

        graphics.draw_rect(
            rand() % SCREEN_WIDTH, rand() % SCREEN_HEIGHT,
            rand() % 100, rand() % 100,
            rand() % 255, rand() % 255, rand() % 255)

        graphics.fill_rect(
            rand() % SCREEN_WIDTH, rand() % SCREEN_HEIGHT,
            rand() % 100, rand() % 100,
            rand() % 255, rand() % 255, rand() % 255)

        graphics.flip()

        frame_time = pygame.time.get_ticks() - frame_start
        delay = FRAME_TIME - frame_time

        if delay > 0:
            pygame.time.delay(int(delay))


if __name__ == '__main__':
    main()
