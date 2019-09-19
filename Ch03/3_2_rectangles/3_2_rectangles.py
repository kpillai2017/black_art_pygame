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


def fill_rect(surface, x, y, width, height, r, g, b) -> None:
    pygame.draw.rect(surface, (r, g, b), (x, y, width, height))


def draw_rect(surface, x, y, width, height, r, g, b) -> None:
    pygame.draw.rect(surface, (r, g, b), (x, y, width, height), 1)


# Setup Pygame
pygame.init()
back_buffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)
pygame.display.set_caption('Drawing Rectangles')

while program_is_running():
    draw_rect(back_buffer,
              random.randint(0, 32768) % 600, random.randint(0, 32768) % 600,  # rand posn
              random.randint(0, 32768) % 200, random.randint(0, 32768) % 200,  # rand size
              random.randint(0, 32768) % 255,
              random.randint(0, 32768) % 255,
              random.randint(0, 32768) % 255)

    fill_rect(back_buffer,
              random.randint(0, 32768) % 600, random.randint(0, 32768) % 600,  # rand posn
              random.randint(0, 32768) % 200, random.randint(0, 32768) % 200,  # rand size
              random.randint(0, 32768) % 255,
              random.randint(0, 32768) % 255,
              random.randint(0, 32768) % 255)

    pygame.time.delay(20)
    pygame.display.flip()

pygame.quit()
sys.exit()
