import pygame, sys, os
import pygame.gfxdraw
import random
from pygame.locals import *


# Quit program if QUIT event is received
def program_is_running():
    running = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    return running


def draw_pixel(surface, x, y, r, g, b):
    if surface.mustlock():
        surface.lock()
        if not surface.get_locked():
            return

    if x >= surface.get_width() or x < 0 or y >= surface.get_height() or y < 0:
        return

    pygame.gfxdraw.pixel(surface, x, y, (r, g, b))

    if surface.mustlock():
        surface.unlock()


background = 0
sprite = 0

# Setup Pygame
pygame.init()
back_buffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)
pygame.display.set_caption('Pixel Plot')

while program_is_running():
    for i in range(100):
        draw_pixel(back_buffer,
                   random.randint(0, 32767) % 800,
                   random.randint(0, 32767) % 600,
                   random.randint(0, 32767) % 255,
                   random.randint(0, 32767) % 255,
                   random.randint(0, 32767) % 255)

    pygame.time.delay(200)
    pygame.display.flip()

pygame.quit()
sys.exit()
