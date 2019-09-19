import pygame, sys, os


# Quit program if QUIT event is received
def program_is_running() -> None:
    running: bool = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    return running


def load_image(folder, file_name):
    image_loaded = pygame.image.load(os.path.join(folder, file_name))
    processed_image = image_loaded.convert()
    if processed_image is not None:
        processed_image.set_colorkey((255, 0, 255))

    return processed_image


def load_files() -> bool:
    global background
    global sprite_image

    background = load_image('graphics', 'background.bmp')
    if not background:
        return False

    sprite_image = load_image('graphics', 'spaceship.bmp')
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
