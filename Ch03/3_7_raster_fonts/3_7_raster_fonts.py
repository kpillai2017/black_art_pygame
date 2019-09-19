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
    global font_image

    background = load_image('graphics', 'background.bmp')
    if not background:
        return False

    font_image = load_image('graphics', 'blocky_font.bmp')
    if not font_image:
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


def draw_raster_text(surface, dest_surface, string, x, y, char_size):
    for i in range(len(string)):
        draw_image_frame(surface, dest_surface, x + i * char_size, y, char_size, char_size, ord(string[i]) - 32)


# Setup Pygame
char_size = 16
pygame.init()
backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)
pygame.display.set_caption("Raster Fonts")

if not load_files():
    print("Failed to load files!")
    pygame.quit()
    sys.exit()

while program_is_running():
    draw_image(background, backbuffer, 0, 0)
    draw_raster_text(font_image, backbuffer, "All Systems Go!", 100, 100, char_size)
    draw_raster_text(font_image, backbuffer, "Drawing Fonts is Fun!", 100, 116, char_size)

    pygame.time.delay(20)
    pygame.display.flip()

pygame.quit()
sys.exit()
