import pygame, sys, os


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


def draw_outline_text(backbuffer, text, x, y, font, r, g, b):
    surface = font.render(text, True, (r, g, b))
    backbuffer.blit(surface, (x, y))


# Setup Pygame
pygame.init()
backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)

font = pygame.font.Font("fonts/Alfphabet.ttf", 24)

pygame.display.set_caption("Outline Fonts")

counter = 0


while program_is_running():
    fill_rect(backbuffer, 0, 0, 800, 600, 0, 0, 0)

    counter += 1
    if counter > 1000:
        counter = 0

    buffer = f"I can count to 1000 really fast: {counter}"

    draw_outline_text(backbuffer, "I am the king of Drawing Text!", 100, 100, font, 255, 0, 0)
    draw_outline_text(backbuffer, "I can draw text in any color I want!", 100,150, font, 0, 255, 0)
    draw_outline_text(backbuffer, buffer, 100, 200, font, 0, 0, 255)

    pygame.time.delay(20)
    pygame.display.flip()

pygame.quit()
sys.exit()
