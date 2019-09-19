import pygame, sys, os

LEFT = 1
RIGHT = 3


# Quit program if QUIT event is received
def program_is_running() -> None:
    global sprite_x, sprite_y
    running: bool = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                sprite_x -= 50
            elif event.key == pygame.K_RIGHT:
                sprite_x += 50
            elif event.key == pygame.K_UP:
                sprite_y -= 50
            elif event.key == pygame.K_DOWN:
                sprite_y += 50

    return running


def load_image(folder, file_name):
    image_loaded = pygame.image.load(os.path.join(folder, file_name))
    processed_image = image_loaded.convert()
    if processed_image is not None:
        processed_image.set_colorkey((255, 0, 255))

    return processed_image


def load_files() -> bool:
    global sprite_image
    global background

    sprite_image = load_image('graphics', 'spaceship.bmp')
    if not sprite_image:
        return False

    background = load_image('graphics', 'background.bmp')
    if not background:
        return False
    return True


def draw_image(image, dest_surface, x, y):
    dest_surface.blit(image, (x, y))


def draw_image_frame(image, dest_surface, x, y, width, height, frame):
    columns = image.get_width() / width
    source_rect_y = (frame // columns) * height
    source_rect_x = (frame % columns) * width
    source_rect_w = width
    source_rect_h = height
    dest_surface.blit(image, (x, y), (source_rect_x, source_rect_y, source_rect_w, source_rect_h))


# Setup Pygame
pygame.init()
backbuffer = 0

sprite_x = 350
sprite_y = 250

backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)
pygame.display.set_caption("Use the arrow keys to move the sprite around and ESC to exit.")

if not load_files():
    print("Failed to load files!")
    pygame.quit()
    sys.exit()

while program_is_running():
    frame_start = pygame.time.get_ticks()

    draw_image(background, backbuffer, 0, 0)
    draw_image(sprite_image, backbuffer, sprite_x, sprite_y)

    pygame.time.delay(20)
    pygame.display.flip()

pygame.quit()
sys.exit()
