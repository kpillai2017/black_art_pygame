import pygame, sys, os, random
from graphics import Graphics
from image import Image
from input import Input

FPS = 30
FRAME_TIME = 1000 / FPS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FULLSCREEN = False
SPRITE_SPEED = 10

graphics = Graphics()
myinput = Input()
sprite = Image()
background = Image()


def rand() -> int:
    return random.randint(0, 32768)


def init_program() -> None:
    pygame.init()

    if not graphics.init(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN):
        return False

    pygame.display.set_caption("Input Test")

    if not sprite.load("graphics/spaceship.bmp", 150, 120):
        return False

    if not background.load("graphics/background.bmp"):
        return False

    myinput.init()

    return True


def free_program() -> None:
    sprite.free()
    background.free()
    myinput.kill()
    pygame.quit()


def program_is_running() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False

    return True


def main() -> int:
    sprite_x = 300
    sprite_y = 300

    if not init_program():
        free_program()
        return False

    while program_is_running():
        myinput.update()

        if myinput.key_down(pygame.K_ESCAPE):
            break

        frame_start = pygame.time.get_ticks()

        if myinput.mouse_down(Input.MOUSE_LEFT):
            sprite_x = myinput.get_mouse_x()
            sprite_y = myinput.get_mouse_y()

        if myinput.mouse_hit(Input.MOUSE_RIGHT):
            sprite_x = myinput.get_mouse_x()
            sprite_y = myinput.get_mouse_y()

        if myinput.key_down(pygame.K_UP):
            sprite_y -= SPRITE_SPEED

        if myinput.key_down(pygame.K_DOWN):
            sprite_y += SPRITE_SPEED

        if myinput.key_down(pygame.K_LEFT):
            sprite_x -= SPRITE_SPEED

        if myinput.key_down(pygame.K_RIGHT):
            sprite_x += SPRITE_SPEED

        graphics.clear(0, 0, 0)

        background.draw(0, 0, graphics)

        sprite.draw(sprite_x, sprite_y, graphics)

        graphics.flip()

        frame_time = pygame.time.get_ticks() - frame_start
        delay = FRAME_TIME - frame_time

        if delay > 0:
            pygame.time.delay(int(delay))

    free_program()

    return 0


if __name__ == '__main__':
    main()
