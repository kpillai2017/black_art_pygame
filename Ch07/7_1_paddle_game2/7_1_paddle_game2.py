import pygame, sys, os, random
from dataclasses import dataclass

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_Y = 550
BALL_WIDTH = 20
BALL_HEIGHT = 20
BALL_SPEED = 10

PLAYER_SPEED = 10

FPS = 30
FRAME_DELAY = 1000 / FPS

GAMEAREA_X1 = 20
GAMEAREA_Y1 = 20
GAMEAREA_X2 = 598
GAMEAREA_Y2 = 600

BLOCK_COLUMNS = 11
BLOCK_ROWS = 5
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 25

GS_SPLASH = 0
GS_RUNNING = 1
GS_GAMEOVER = 2
GS_PAUSED = 3

# Surfaces
backbuffer = 0
background_image = 0
ball_image = 0
player_paddle_image = 0
block_image = 0
splash_image = 0
gameover_image = 0
gamepaused_image = 0

# Font
game_font = 0

# Sounds
ball_bounce_sound = 0
ball_spawn_sound = 0
explosion_sound = 0

# Music
game_music = 0


@dataclass
class Block:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.alive = True
        self.frame = 0


@dataclass
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.x_vel = 0
        self.y_vel = 0
        self.is_locked = True


@dataclass
class Player:
    # rect: pygame.Rect(0, 0, 0, 0)
    # lives: int = 0
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.lives = 0


blocks = [Block() for i in range(BLOCK_COLUMNS * BLOCK_ROWS)]
player = Player()
ball = Ball()
game_state = 0


def fill_rect(surface, x, y, width, height, r, g, b) -> None:
    pygame.draw.rect(surface, (r, g, b), (x, y, width, height))


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


def draw_text(surface, text, x, y, font, r, g, b):
    rendered_text = font.render(text, True, (r, g, b))
    surface.blit(rendered_text, (x, y))


# Quit program if QUIT event is received
def program_is_running() -> bool:
    global game_state

    running: bool = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == GS_RUNNING:
                    game_state = GS_PAUSED
                elif game_state == GS_PAUSED:
                    game_state = GS_RUNNING

    return running


def load_files() -> bool:
    global background_image, splash_image, gameover_image
    global gamepaused_image, ball_image, player_paddle_image, block_image
    global game_font, ball_bounce_sound, ball_spawn_sound, explosion_sound

    # Load images
    background_image = load_image('graphics', 'background.bmp')
    splash_image = load_image('graphics', 'splash.bmp')
    gameover_image = load_image('graphics', 'gameover.bmp')
    gamepaused_image = load_image('graphics', 'gamepaused.bmp')
    ball_image = load_image('graphics', 'ball.bmp')
    player_paddle_image = load_image('graphics', 'player.bmp')
    block_image = load_image('graphics', 'blocks.bmp')

    # Error checking images
    if not background_image:
        return False
    if not splash_image:
        return False
    if not gameover_image:
        return False
    if not gamepaused_image:
        return False
    if not ball_image:
        return False
    if not player_paddle_image:
        return False
    if not block_image:
        return False

    # Load font
    game_font = pygame.font.Font("graphics/brick.ttf", 20)
    if not game_font:
        return False

    # Load sounds
    ball_bounce_sound = pygame.mixer.Sound("audio/ball_bounce.wav")
    ball_spawn_sound = pygame.mixer.Sound("audio/ball_spawn.wav")
    explosion_sound = pygame.mixer.Sound("audio/explosion.wav")

    if not ball_bounce_sound:
        return False
    if not ball_spawn_sound:
        return False
    if not explosion_sound:
        return False

    # Load music
    pygame.mixer.music.load("audio/song.mp3")

    return True


def free_files():
    pass


def rects_overlap(rect1, rect2):
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
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(22050, -16, 2, 2048)

    backbuffer = pygame.display.set_mode((800, 600), pygame.SWSURFACE, 32)

    return True


def set_blocks():
    global blocks

    i = 0

    for x in range(BLOCK_COLUMNS):
        for y in range(BLOCK_ROWS):
            blocks[i].rect.x = x * BLOCK_WIDTH + GAMEAREA_X1 + x * 3
            blocks[i].rect.y = (y * 2) * BLOCK_HEIGHT + GAMEAREA_Y1 + y * 3
            blocks[i].rect.w = BLOCK_WIDTH
            blocks[i].rect.h = BLOCK_HEIGHT
            blocks[i].alive = True
            blocks[i].frame = i % 4
            i += 1


def draw_blocks():
    global blocks, block_image, backbuffer

    for i in range(BLOCK_COLUMNS * BLOCK_ROWS):
        if blocks[i].alive:
            draw_image_frame(block_image, backbuffer,
                             blocks[i].rect.x, blocks[i].rect.y,
                             blocks[i].rect.w, blocks[i].rect.h,
                             blocks[i].frame)


def num_blocks_left():
    global blocks

    result = 0

    for i in range(BLOCK_COLUMNS * BLOCK_ROWS):
        if blocks[i].alive:
            result += 1

    return result


def reset_game():
    global ball, ball_spawn_sound, player

    # Position the player's paddle
    player.rect.x = (GAMEAREA_X2 - GAMEAREA_X1) // 2 - PADDLE_WIDTH // 2 + GAMEAREA_X1
    player.rect.y = PADDLE_Y
    player.rect.w = PADDLE_WIDTH
    player.rect.h = PADDLE_HEIGHT

    # Position the ball
    ball.rect.x = SCREEN_WIDTH / 2 - BALL_WIDTH / 2
    ball.rect.y = SCREEN_HEIGHT / 2 - BALL_HEIGHT / 2
    ball.rect.w = BALL_WIDTH
    ball.rect.h = BALL_HEIGHT

    # Play the spawn sound
    ball_spawn_sound.play()

    set_blocks()
    ball.is_locked = True
    player.lives = 3


def init_game():
    global game_state

    # Init SDL
    if not init_sdl():
        return False

    # Load Files
    if not load_files():
        return False

    # Set the title
    pygame.display.set_caption("Paddle Game 2!")

    # Play Music
    pygame.mixer.music.play()

    # Set the game state
    game_state = GS_SPLASH

    return True


def update_player():
    global player, ball

    keys = pygame.key.get_pressed()

    # Move the paddle when the left/right key is pressed
    if keys[pygame.K_LEFT]:
        player.rect.x -= PLAYER_SPEED

    if keys[pygame.K_RIGHT]:
        player.rect.x += PLAYER_SPEED

    if keys[pygame.K_SPACE] and ball.is_locked:
        ball.is_locked = False
        ball.x_vel = random.randint(0, 32768) % 3 - 1
        ball.y_vel = BALL_SPEED

    # Make sure the paddle doesn't leave the screen
    if player.rect.x < GAMEAREA_X1:
        player.rect.x = GAMEAREA_X1

    if player.rect.x > GAMEAREA_X2 - player.rect.w:
        player.rect.x = GAMEAREA_X2 - player.rect.w


def update_ball():
    global ball, player, explosion_sound, ball_bounce_sound, blocks, ball_spawn_sound

    if ball.is_locked:  # If the ball is locked, position it on top of the paddle and centred on the X axis
        paddle_center_x = player.rect.x + player.rect.w / 2
        ball.rect.x = paddle_center_x - ball.rect.w / 2
        ball.rect.y = player.rect.y - ball.rect.h
    else:
        ball.rect.x += ball.x_vel

        # If the ball hits the player while moving on the X-Axis, make it bounce accordingly
        if rects_overlap(ball.rect, player.rect):
            ball.rect.x -= ball.x_vel
            ball.x_vel *= -1
            ball_bounce_sound.play()
        else:  # If not, check if it hit any blocks while moving on the X-Axis
            for i in range(BLOCK_COLUMNS * BLOCK_ROWS):
                if blocks[i].alive and rects_overlap(ball.rect, blocks[i].rect):
                    ball.rect.x -= ball.x_vel
                    ball.x_vel *= -1
                    blocks[i].alive = False

                    explosion_sound.play()

        ball.rect.y += ball.y_vel

        # If the ball hits the player while moving in the Y-Axis, make it bounce accordingly
        if rects_overlap(ball.rect, player.rect):
            ball.rect.y -= ball.y_vel
            ball.y_vel *= -1

            # Make the X velocity the distance between the paddle's center and the ball's center devided by 5
            ball_center_x = ball.rect.x + ball.rect.w / 2
            paddle_center_x = player.rect.x + player.rect.w / 2

            ball.x_vel = (ball_center_x - paddle_center_x) / 5
            ball_bounce_sound.play()

        else:  # If not, check if it hit any blocks while moving on the Y-Axis
            for i in range(BLOCK_COLUMNS * BLOCK_ROWS):
                if blocks[i].alive and rects_overlap(ball.rect, blocks[i].rect):
                    ball.rect.y -= ball.y_vel
                    ball.y_vel *= -1
                    blocks[i].alive = False

                    explosion_sound.play()

        # Make sure the ball doesn't leave the screen and make it
        # bounce randomly
        if ball.rect.y < GAMEAREA_Y1:
            ball.rect.y = GAMEAREA_Y1
            ball.y_vel *= -1
            ball_bounce_sound.play()

        if ball.rect.x > (GAMEAREA_X2 - ball.rect.w):
            ball.rect.x = GAMEAREA_X2 - ball.rect.w
            ball.x_vel *= -1
            ball_bounce_sound.play()

        if ball.rect.x < GAMEAREA_X1:
            ball.rect.x = GAMEAREA_X1
            ball.x_vel *= -1
            ball_bounce_sound.play()

        # If the player looses the ball

        if ball.rect.y > GAMEAREA_Y2:
            ball.is_locked = True

            # Reposition Ball
            paddle_center_x = player.rect.x + player.rect.w / 2
            ball.rect.x = paddle_center_x - ball.rect.w / 2
            ball.rect.y = player.rect.y - ball.rect.h

            player.lives -= 1
            ball_spawn_sound.play()


def update_splash():
    global game_state

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RETURN]:
        # This will start a new game
        reset_game()
        game_state = GS_RUNNING


def draw_splash():
    global backbuffer

    draw_image(splash_image, backbuffer, 0, 0)


def update_game():
    global game_state

    update_player()
    update_ball()

    if player.lives <= 0:
        game_state = GS_GAMEOVER

    if num_blocks_left() <= 0:
        reset_game()


def draw_game():
    global backbuffer, background_image, ball_image, player_paddle_image, ball, player, game_font

    draw_image(background_image, backbuffer, 0, 0)
    draw_image(ball_image, backbuffer, ball.rect.x, ball.rect.y)
    draw_image(player_paddle_image, backbuffer, player.rect.x, player.rect.y)
    draw_blocks()

    blocks_text = f"Blocks: {num_blocks_left()}"
    lives_text = f"Lives: {player.lives}"

    draw_text(backbuffer, blocks_text, 645, 150, game_font, 255, 255, 255)
    draw_text(backbuffer, lives_text, 645, 170, game_font, 255, 255, 255)


def draw_game_paused():
    global gamepaused_image, backbuffer

    draw_game()
    draw_image(gamepaused_image, backbuffer, 0, 0)


def update_game_over():
    global game_state

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        game_state = GS_SPLASH


def draw_game_over():
    global gameover_image, backbuffer

    draw_game()
    draw_image(gameover_image, backbuffer, 0, 0)


def run_game():
    if game_state == GS_SPLASH:
        update_splash()
    elif game_state == GS_RUNNING:
        update_game()
    elif game_state == GS_GAMEOVER:
        update_game_over()


def draw_screen():
    if game_state == GS_SPLASH:
        draw_splash()
    elif game_state == GS_RUNNING:
        draw_game()
    elif game_state == GS_GAMEOVER:
        draw_game_over()
    elif game_state == GS_PAUSED:
        draw_game_paused()


def free_game():
    pygame.mixer.quit()
    pygame.quit()


if not init_game():
    free_game()

while program_is_running():
    old_time = pygame.time.get_ticks()

    fill_rect(backbuffer, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    run_game()
    draw_screen()

    frame_time = pygame.time.get_ticks() - old_time

    if frame_time < FRAME_DELAY:
        pygame.time.delay(int(FRAME_DELAY - frame_time))
    pygame.display.flip()

sys.exit()
