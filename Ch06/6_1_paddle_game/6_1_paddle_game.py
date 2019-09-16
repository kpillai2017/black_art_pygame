import pygame, sys, os, random

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_WIDTH = 20
BALL_HEIGHT = 20
BALL_MAX_SPEED = 20

PLAYER_PADDLE_X = PADDLE_WIDTH
ENEMY_PADDLE_X = SCREEN_WIDTH - PADDLE_WIDTH * 2

PLAYER_SPEED = 10
ENEMY_SPEED = 7

FPS = 30
FRAME_DELAY = 1000 / FPS

# Surfaces
backbuffer = 0
background_image = 0
ball_image = 0
player_paddle_image = 0
enemy_paddle_image = 0

# Font
game_font = 0

# Sounds
ball_bounce_sound = 0
ball_spawn_sound = 0
player_score_sound = 0
enemy_score_sound = 0

# Music
game_music = 0

# Game variables
player_score = 0
enemy_score = 0

ball_x_vel = 0
ball_y_vel = 0

player_paddle_rect = pygame.Rect(0, 0, 0, 0)
enemy_paddle_rect = pygame.Rect(0, 0, 0, 0)
ball_rect = pygame.Rect(0, 0, 0, 0)


def fill_rect(surface, x, y, width, height, r, g, b) -> None:
    pygame.draw.rect(surface, (r, g, b), (x, y, width, height))


def free_game():
    pygame.mixer.quit()
    pygame.quit()


def load_image(folder, file_name):
    image_loaded = pygame.image.load(os.path.join(folder, file_name))
    processed_image = image_loaded.convert()
    if processed_image is not None:
        processed_image.set_colorkey((255, 0, 255))

    return processed_image


def draw_image_frame(image, dest_surface, x, y, width, height, frame):
    columns = image.get_width() / width
    source_rect_y = (frame // columns) * height
    source_rect_x = (frame % columns) * width
    source_rect_w = width
    source_rect_h = height
    dest_surface.blit(image, (x, y), (source_rect_x, source_rect_y, source_rect_w, source_rect_h))


def draw_image(image, dest_surface, x, y):
    dest_surface.blit(image, (x, y))


def draw_text(surface, text, x, y, font, r, g, b):
    rendered_text = font.render(text, True, (r, g, b))
    surface.blit(rendered_text, (x, y))


# Quit program if QUIT event is received
def program_is_running() -> bool:
    running: bool = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    return running


def load_files() -> bool:
    global background_image, ball_image, player_paddle_image, enemy_paddle_image
    global game_font, ball_bounce_sound, ball_spawn_sound, player_score_sound, enemy_score_sound

    background_image = load_image('graphics', 'background.bmp')
    ball_image = load_image('graphics', 'ball.bmp')
    player_paddle_image = load_image('graphics', 'player.bmp')
    enemy_paddle_image = load_image('graphics', 'enemy.bmp')

    if not background_image:
        return False
    if not ball_image:
        return False
    if not player_paddle_image:
        return False
    if not enemy_paddle_image:
        return False

    game_font = pygame.font.Font("graphics/alfphabet.ttf", 30)
    if not game_font:
        return False

    ball_bounce_sound = pygame.mixer.Sound("audio/ballBounce.wav")
    ball_spawn_sound = pygame.mixer.Sound("audio/ballSpawn.wav")
    player_score_sound = pygame.mixer.Sound("audio/playerScore.wav")
    enemy_score_sound = pygame.mixer.Sound("audio/enemyScore.wav")

    if not ball_bounce_sound:
        return False
    if not ball_spawn_sound:
        return False
    if not player_score_sound:
        return False
    if not enemy_score_sound:
        return False

    # Load music
    pygame.mixer.music.load("audio/song.mp3")

    return True


def free_files():
    pass


def rect_overlap(rect1, rect2):
    if rect1.x >= rect2.x + rect2.w:
        return False

    if rect1.y >= rect2.y + rect2.h:
        return False

    if rect2.x >= rect1.x + rect1.w:
        return False

    if rect2.y >= rect1.y + rect1.h:
        return False

    return True


def init_sdl():
    global backbuffer

    # Setup Pygame
    pygame.mixer.pre_init(22050, -16, 2, 2048)
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(22050, -16, 2, 2048)

    backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)

    return True


def reset_game():
    global ball_x_vel, ball_y_vel

    # Position the player's paddle
    player_paddle_rect.x = PLAYER_PADDLE_X
    player_paddle_rect.y = SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2
    player_paddle_rect.w = PADDLE_WIDTH
    player_paddle_rect.h = PADDLE_HEIGHT

    # Position the enemies paddle
    enemy_paddle_rect.x = ENEMY_PADDLE_X
    enemy_paddle_rect.y = SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2
    enemy_paddle_rect.w = PADDLE_WIDTH
    enemy_paddle_rect.h = PADDLE_HEIGHT

    # Position the ball
    ball_rect.x = SCREEN_WIDTH / 2 - BALL_WIDTH / 2
    ball_rect.y = SCREEN_HEIGHT / 2 - BALL_HEIGHT / 2
    ball_rect.w = BALL_WIDTH
    ball_rect.h = BALL_HEIGHT

    # Make the ball X velocity a random value from 1 to BALL_MAX_SPEED
    ball_x_vel = random.randint(0, 32768) % BALL_MAX_SPEED + 1

    # Make the ball Y velocity a random value from -BALL_MAX_SPEED to BALL_MAX_SPEED
    ball_y_vel = (random.randint(0, 32768) % BALL_MAX_SPEED * 2 + 1) - BALL_MAX_SPEED

    # Give it a 50% probability of going toward's the player
    if random.randint(0, 32768) % 2 == 0:
        ball_x_vel *= -1

    # Play the spawn sound
    ball_spawn_sound.play()


def init_game():
    global player_score, enemy_score

    # Init SDL
    if not init_sdl():
        return False

    # Load Files
    if not load_files():
        return False

    # Set the title
    pygame.display.set_caption("Paddle Game!")

    # Set scores to 0
    player_score = 0
    enemy_score = 0

    # This can also set the initial variables
    reset_game()

    # Play Music
    pygame.mixer.music.play()

    return True


def update_player():
    keys = pygame.key.get_pressed()

    # Move the paddle when the up/down key is pressed
    if keys[pygame.K_UP]:
        player_paddle_rect.y -= PLAYER_SPEED

    if keys[pygame.K_DOWN]:
        player_paddle_rect.y += PLAYER_SPEED;

    # Make sure the paddle doesn't leave the screen
    if player_paddle_rect.y < 0:
        player_paddle_rect.y = 0

    if player_paddle_rect.y > SCREEN_HEIGHT - player_paddle_rect.h:
        player_paddle_rect.y = SCREEN_HEIGHT - player_paddle_rect.h


def update_ai():
    # If the paddle's center higher than the ball's center, move the paddle up
    if (enemy_paddle_rect.y + enemy_paddle_rect.h / 2) > (ball_rect.y + ball_rect.h / 2):
        enemy_paddle_rect.y -= ENEMY_SPEED

    # If the paddle's center lower than the ball's center, move the paddle down
    if (enemy_paddle_rect.y + enemy_paddle_rect.h / 2) < (ball_rect.y + ball_rect.h / 2):
        enemy_paddle_rect.y += ENEMY_SPEED

    # Make sure the paddle doesn't leave the screen
    if enemy_paddle_rect.y < 0:
        enemy_paddle_rect.y = 0

    if enemy_paddle_rect.y > SCREEN_HEIGHT - enemy_paddle_rect.h:
        enemy_paddle_rect.y = SCREEN_HEIGHT - enemy_paddle_rect.h


def update_ball():
    global ball_x_vel, ball_y_vel, player_score, enemy_score

    ball_rect.x += ball_x_vel
    ball_rect.y += ball_y_vel

    # If the ball hits the player, make it bounce
    if rect_overlap(ball_rect, player_paddle_rect):
        ball_x_vel = (random.randint(0, 32768) % BALL_MAX_SPEED) + 1
        ball_bounce_sound.play()

    # If the ball hits the enemy, make it bounce
    if rect_overlap(ball_rect, enemy_paddle_rect):
        ball_x_vel = (random.randint(0, 32768) % BALL_MAX_SPEED + 1) * -1
        ball_bounce_sound.play()

    # Make sure the ball doesn't leave the screen and make it
    # bounce randomly
    if ball_rect.y < 0:
        ball_rect.y = 0
        ball_y_vel = (random.randint(0, 32768) % BALL_MAX_SPEED) + 1
        ball_bounce_sound.play()

    if ball_rect.y > (SCREEN_HEIGHT - ball_rect.h):
        ball_rect.y = SCREEN_HEIGHT - ball_rect.h
        ball_y_vel = (random.randint(0, 32768) % BALL_MAX_SPEED + 1) * -1
        ball_bounce_sound.play()

    # If player scores
    if ball_rect.x > SCREEN_WIDTH:
        player_score += 1
        player_score_sound.play()
        reset_game()

    # If enemy scores
    if ball_rect.x < 0 - ball_rect.w:
        enemy_score += 1
        enemy_score_sound.play()
        reset_game()


def run_game():
    update_player()
    update_ai()
    update_ball()


def draw_game():
    global backbuffer, background_image, ball_image, player_paddle_image, enemy_paddle_image, game_font

    draw_image(background_image, backbuffer, 0, 0)
    draw_image(ball_image, backbuffer, ball_rect.x, ball_rect.y)
    draw_image(player_paddle_image, backbuffer, player_paddle_rect.x, player_paddle_rect.y)
    draw_image(enemy_paddle_image, backbuffer, enemy_paddle_rect.x, enemy_paddle_rect.y)

    player_hud = f"Player Score: {player_score}"
    enemy_hud = f"Enemy Score: {enemy_score}"

    draw_text(backbuffer, player_hud, 0, 1, game_font, 64, 64, 64)
    draw_text(backbuffer, enemy_hud, 0, 30, game_font, 64, 64, 64)


def free_game():
    pygame.mixer.quit()
    pygame.quit()


if not init_game():
    free_game()

while program_is_running():
    old_time = pygame.time.get_ticks()

    fill_rect(backbuffer, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    run_game()
    draw_game()

    frame_time = pygame.time.get_ticks() - old_time

    if frame_time < FRAME_DELAY:
        pygame.time.delay(int(FRAME_DELAY - frame_time))
    pygame.display.flip()

sys.exit()
