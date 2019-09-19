import pygame, sys, os


def load_files() -> bool:
    global background

    background = load_image('graphics', 'background.bmp')
    if not background:
        return False

    pygame.mixer.music.load("audio/happy_song.mp3")

    return True


def free_files():
    pass


def load_image(folder, file_name):
    image_loaded = pygame.image.load(os.path.join(folder, file_name))
    processed_image = image_loaded.convert()
    if processed_image is not None:
        processed_image.set_colorkey((255, 0, 255))

    return processed_image


def draw_image(image, dest_surface, x, y):
    dest_surface.blit(image, (x, y))


def draw_image_frame(image, dest_surface, x, y, width, height, frame):
    columns = image.get_width() / width
    source_rect_y = (frame // columns) * height
    source_rect_x = (frame % columns) * width
    source_rect_w = width
    source_rect_h = height
    dest_surface.blit(image, (x, y), (source_rect_x, source_rect_y, source_rect_w, source_rect_h))


# Quit program if QUIT event is received
def program_is_running() -> None:
    running: bool = True
    global music_playing

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                pygame.mixer.music.stop()
                music_playing = False
            elif event.key == pygame.K_SPACE:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
                    music_playing = True
                else:
                    if music_playing:
                        pygame.mixer.music.pause()
                        music_playing = False
                    else:
                        pygame.mixer.music.unpause()
                        music_playing = True

    return running


# Surfaces
background = 0

# Setup Pygame
pygame.mixer.pre_init(22050, -16, 2, 2048)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 2048)

backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)

pygame.display.set_caption("BLASTING OUT MUSIC XD")

if not load_files():
    print("Failed to load files!")
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()

while program_is_running():
    draw_image(background, backbuffer, 0, 0)

    pygame.time.delay(20)
    pygame.display.flip()

pygame.mixer.quit()
pygame.quit()
sys.exit()
