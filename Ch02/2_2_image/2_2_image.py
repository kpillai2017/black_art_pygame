import pygame, sys, os
from pygame.locals import *

pygame.init()
backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)
pygame.display.set_caption('Pygame!!!')

image = pygame.image.load(os.path.join('graphics', 'image.bmp'))
image = image.convert()

# pygame.Surface.blit(image, backbuffer, (0,0))
backbuffer.blit(image, (0,0))
pygame.display.flip()

pygame.time.delay(3000)
pygame.quit()
sys.exit()
