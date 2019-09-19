import pygame, sys, os

# Quit program if QUIT event is received
def program_is_running() -> None:
    running: bool = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_a:
                note_channel[0] = c_note.play()
            elif event.key == pygame.K_w:
                note_channel[1] = cs_note.play()
            elif event.key == pygame.K_s:
                note_channel[2] = d_note.play()
            elif event.key == pygame.K_e:
                note_channel[3] = ds_note.play()
            elif event.key == pygame.K_d:
                note_channel[4] = e_note.play()
            elif event.key == pygame.K_f:
                note_channel[5] = f_note.play()
            elif event.key == pygame.K_t:
                note_channel[6] = fs_note.play()
            elif event.key == pygame.K_g:
                note_channel[7] = g_note.play()
            elif event.key == pygame.K_y:
                note_channel[8] = gs_note.play()
            elif event.key == pygame.K_h:
                note_channel[9] = a_note.play()
            elif event.key == pygame.K_u:
                note_channel[10] = as_note.play()
            elif event.key == pygame.K_j:
                note_channel[11] = b_note.play()
            elif event.key == pygame.K_k:
                note_channel[12] = high_c_note.play()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_a:
                note_channel[0].stop()
            elif event.key == pygame.K_w:
                note_channel[1].stop()
            elif event.key == pygame.K_s:
                note_channel[2].stop()
            elif event.key == pygame.K_e:
                note_channel[3].stop()
            elif event.key == pygame.K_d:
                note_channel[4].stop()
            elif event.key == pygame.K_f:
                note_channel[5].stop()
            elif event.key == pygame.K_t:
                note_channel[6].stop()
            elif event.key == pygame.K_g:
                note_channel[7].stop()
            elif event.key == pygame.K_y:
                note_channel[8].stop()
            elif event.key == pygame.K_h:
                note_channel[9].stop()
            elif event.key == pygame.K_u:
                note_channel[10].stop()
            elif event.key == pygame.K_j:
                note_channel[11].stop()
            elif event.key == pygame.K_k:
                note_channel[12].stop()

    return running


def load_image(folder, file_name):
    image_loaded = pygame.image.load(os.path.join(folder, file_name))
    processed_image = image_loaded.convert()
    if processed_image is not None:
        processed_image.set_colorkey((255, 0, 255))

    return processed_image


def load_files() -> bool:
    global background
    global c_note, cs_note, d_note, ds_note, e_note, f_note
    global fs_note, g_note, gs_note, a_note, as_note, b_note, high_c_note

    background = load_image('graphics', 'background.bmp')

    c_note = pygame.mixer.Sound("notes/c.wav")
    cs_note = pygame.mixer.Sound("notes/cs.wav")
    d_note = pygame.mixer.Sound("notes/d.wav")
    ds_note = pygame.mixer.Sound("notes/ds.wav")
    e_note = pygame.mixer.Sound("notes/e.wav")
    f_note = pygame.mixer.Sound("notes/f.wav")
    fs_note = pygame.mixer.Sound("notes/fs.wav")
    g_note = pygame.mixer.Sound("notes/g.wav")
    gs_note = pygame.mixer.Sound("notes/gs.wav")
    a_note = pygame.mixer.Sound("notes/a.wav")
    as_note = pygame.mixer.Sound("notes/as.wav")
    b_note = pygame.mixer.Sound("notes/b.wav")
    high_c_note = pygame.mixer.Sound("notes/highC.wav")

    if not background or not c_note or not cs_note or not d_note or \
            not ds_note or not e_note or not f_note  or not fs_note  or \
            not g_note or not gs_note or not a_note or not as_note or \
            not b_note or not high_c_note:
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

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 1024)


# pygame.init()
backbuffer = 0
note_channel = []

# pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024,
#                   devicename="aa",
#                   allowedchanges=0)

# pygame.mixer.init()

backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)

pygame.display.set_caption("SDL Piano")

for i in range(13):
    note_channel.append(-1)

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
