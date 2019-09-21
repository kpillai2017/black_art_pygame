import pygame, sys, os, random
from graphics import Graphics
from image import Image
from raster_font import RasterFont
from outline_font import OutlineFont

FPS = 30
FRAME_TIME = 1000 / FPS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FULLSCREEN = False

MAX_FRAME_DELAY = 2
MAX_FRAME = 11

graphics = Graphics()
background = Image()
raster_font = RasterFont()
outline_font = OutlineFont()

image_frame = 0
frame_delay = 0


def rand() -> int:
    return random.randint(0, 32768)


def init_program() -> None:
    pygame.init()

    if not graphics.init(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN):
        return False

    pygame.display.set_caption("Font Test")

    if not background.load("graphics/background.bmp"):
        return False

    if not raster_font.load("graphics/blocky_font.bmp"):
        return False

    if not outline_font.load("graphics/bbrick.ttf", 25):
        return False

    return True


def free_program() -> None:
    background.free()
    raster_font.free()
    outline_font.free()
    pygame.quit()


def program_is_running() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False

    return True


def main() -> int:
    color_counter = 0

    if not init_program():
        free_program()
        return False

    while program_is_running():
        frame_start = pygame.time.get_ticks()

        graphics.clear(0, 0, 0)

        color_counter += 5
        if color_counter > 255:
            color_counter = 0

        background.draw(0, 0, graphics)
        raster_font.draw("Raster fonts are really cool!!!", 100, 100, graphics)
        outline_font.draw("Outline fonts are just as cool!!!", 100, 150, 0, 0, color_counter, graphics)

        graphics.flip()

        frame_time = pygame.time.get_ticks() - frame_start
        delay = FRAME_TIME - frame_time

        if delay > 0:
            pygame.time.delay(int(delay))

    free_program()

    return 0


if __name__ == '__main__':
    main()
