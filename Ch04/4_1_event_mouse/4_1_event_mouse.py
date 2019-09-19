import pygame, sys, os

LEFT = 1
RIGHT = 3


# Quit program if QUIT event is received
def program_is_running() -> None:
    global cross1X, cross1Y, cross2X, cross2Y
    running: bool = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                cross1X = pygame.mouse.get_pos()[0]
                cross1Y = pygame.mouse.get_pos()[1]

            if event.button == RIGHT:
                cross2X = pygame.mouse.get_pos()[0]
                cross2Y = pygame.mouse.get_pos()[1]

        if event.type == pygame.MOUSEMOTION:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]

            buffer = f"Mouse X: {mouseX}, Mouse Y: {mouseY}"
            pygame.display.set_caption(buffer)

    return running


def load_image(folder, file_name):
    image_loaded = pygame.image.load(os.path.join(folder, file_name))
    processed_image = image_loaded.convert()
    if processed_image is not None:
        processed_image.set_colorkey((255, 0, 255))

    return processed_image


def load_files() -> bool:
    global cross1
    global cross2
    global background

    cross1 = load_image('graphics', 'cross_1.bmp')
    if not cross1:
        return False

    cross2 = load_image('graphics', 'cross_2.bmp')
    if not cross2:
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

cross1 = 0
cross2 = 0

cross1X = -100
cross1Y = -100
cross2X = -100
cross2Y = -100
backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)

if not load_files():
    print("Failed to load files!")
    pygame.quit()
    sys.exit()

while program_is_running():
    frame_start = pygame.time.get_ticks()

    draw_image(background, backbuffer, 0, 0)
    draw_image(cross1, backbuffer, cross1X - 50, cross1Y - 50)
    draw_image(cross2, backbuffer, cross2X - 50, cross2Y - 50)

    pygame.time.delay(20)
    pygame.display.flip()

pygame.quit()
sys.exit()
