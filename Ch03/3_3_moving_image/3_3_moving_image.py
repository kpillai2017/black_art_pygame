import pygame, sys, os
import pygame.gfxdraw
import random
from pygame.locals import *


# Quit program if QUIT event is received
def program_is_running() -> None:
    running: bool = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    return running


def load_files() -> bool:
    global background
    global sprite_image

    background = pygame.image.load(os.path.join('graphics', 'background.bmp'))
    background = background.convert()
    if not background:
        return False

    sprite_image = pygame.image.load(os.path.join('graphics', 'spaceship.bmp'))
    sprite_image = sprite_image.convert()

    if not sprite_image:
        return False

    return True


# Setup Pygame
pygame.init()
backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)
pygame.display.set_caption('Moving Image')

if not load_files():
    print("Failed to load files!")
    pygame.quit()
    sys.exit()

sprite_pos_x = 0
sprite_pos_y = 250
while program_is_running():
    sprite_pos_x += 5
    if sprite_pos_x > 800:
        sprite_pos_x = -200

    backbuffer.blit(background, (0, 0))
    backbuffer.blit(sprite_image, (sprite_pos_x, sprite_pos_y))

    pygame.time.delay(20)
    pygame.display.flip()

pygame.quit()
sys.exit()
