import pygame, sys
from pygame.locals import *

pygame.init()
pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)
pygame.display.set_caption('Hello World!')
pygame.time.delay(3000)
pygame.quit()
sys.exit()
