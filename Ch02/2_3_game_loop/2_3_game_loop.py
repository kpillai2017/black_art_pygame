import pygame, sys, os
import random
from pygame.locals import *


# Quit program if QUIT event is received
def program_is_running() -> bool:
    running = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    return running


def load_images() -> bool:
    global background
    global sprite

    background = pygame.image.load(os.path.join('graphics', 'background.bmp'))
    background = background.convert()
    if not background:
        return False

    sprite = pygame.image.load(os.path.join('graphics', 'sprite.bmp'))
    sprite = sprite.convert()

    if not sprite:
        return False

    return True


def free_images() -> None:
    pass


background = 0
sprite = 0

# Setup Pygame
pygame.init()
back_buffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)
pygame.display.set_caption('Pygame!!!')

# Load images
if not load_images():
    print("Images failed to load.")
    free_images()
    pygame.quit()
    sys.exit()

back_buffer.blit(background, (0, 0))

while program_is_running():
    back_buffer.blit(sprite, (random.randint(0, 32767) % 800,
                              random.randint(0, 32767) % 600))
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
