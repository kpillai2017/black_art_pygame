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

    sprite_image = load_image('graphics', 'demon.bmp')
    if not sprite_image:
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
background = 0
sprite_image = 0

sprite_frame = 0
frame_counter = 0

max_sprite_frame = 11
frame_delay = 2

background_X = 0

pygame.init()
backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)
pygame.display.set_caption('Moving Image')

if not load_files():
    print("Failed to load files!")
    pygame.quit()
    sys.exit()

FPS = 30
FRAME_DELAY = 1000/FPS

while program_is_running():
    frame_start = pygame.time.get_ticks()

    # Updates the sprites frame
    frame_counter += 1

    if frame_counter > frame_delay:
        frame_counter = 0
        sprite_frame += 1

    if sprite_frame > max_sprite_frame:
        sprite_frame = 0

    background_X -= 6
    if background_X <= -800:
        background_X = 0

    draw_image(background, backbuffer, background_X, 0)
    draw_image(background, backbuffer, background_X + 800, 0)
    draw_image_frame(sprite_image, backbuffer, 350, 250, 150, 120, sprite_frame)

    frame_time = pygame.time.get_ticks() - frame_start
    if frame_time < FRAME_DELAY:
        pygame.time.delay(int(FRAME_DELAY - frame_time))

    pygame.display.flip()

pygame.quit()
sys.exit()
