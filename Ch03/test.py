import pygame, sys, os
import random
from pygame.locals import *

def programIsRunning():
    running = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    return running

def loadImages():
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

def freeImages():
    pass

background = 0
sprite = 0

pygame.init()
backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)
pygame.display.set_caption('Pygame!!!')

if not loadImages():
    print("Images failed to load.")
    freeImages()
    pygame.quit()
    sys.exit()

backbuffer.blit(background, (0,0))

while programIsRunning():
    backbuffer.blit(sprite, (random.randint(0, 32767)%800, random.randint(0, 32767)%600))
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
sys.exit()



