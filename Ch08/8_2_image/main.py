import pygame, sys, os, random
from graphics import Graphics
from image import Image

FPS = 30
FRAME_TIME = 1000 / FPS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FULLSCREEN = False

MAX_FRAME_DELAY = 2
MAX_FRAME = 11

graphics = Graphics()
sprite = Image()
background = Image()

image_frame = 0
frame_delay = 0


def rand() -> int:
    return random.randint(0, 32768)


def init_program() -> None:
    pygame.init()

    if not graphics.init(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN):
        return False

    pygame.display.set_caption("Image Test")

    if not sprite.load("graphics/demon.bmp", 150, 120):
        return False

    if not background.load("graphics/background.bmp"):
        return False

    return True


def free_program() -> None:
    sprite.free()
    background.free()
    pygame.quit()


def program_is_running() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False

    return True


def main() -> int:
    global frame_delay, image_frame

    if not init_program():
        free_program()
        return False

    counter = 0

    while program_is_running():
        frame_start = pygame.time.get_ticks()

        frame_delay += 1

        if frame_delay > MAX_FRAME_DELAY:
            frame_delay = 0
            image_frame += 1

            if image_frame > MAX_FRAME:
                image_frame = 0

        graphics.clear(0, 0, 0)

        background.draw(0, 0, graphics)

        for x in range(0, 800, 200):
            sprite.draw(x, 300, image_frame, graphics)

        graphics.flip()

        frame_time = pygame.time.get_ticks() - frame_start
        delay = FRAME_TIME - frame_time

        if delay > 0:
            pygame.time.delay(int(delay))

    free_program()

    return 0


if __name__ == '__main__':
    main()
