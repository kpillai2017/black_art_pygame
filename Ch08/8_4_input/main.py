
# --- Import required modules and game components ---
import pygame, sys, os, random
from graphics import Graphics
from image import Image
from input import Input

# --- Game configuration constants ---
FPS = 30  # Frames per second
FRAME_TIME = 1000 / FPS  # Duration of each frame in ms
SCREEN_WIDTH = 800  # Window width
SCREEN_HEIGHT = 600  # Window height
FULLSCREEN = False  # Fullscreen toggle
SPRITE_SPEED = 10  # Speed of sprite movement

# --- Global game objects ---
graphics = Graphics()  # Handles all drawing
myinput = Input()      # Handles keyboard/mouse input
sprite = Image()       # The main sprite image
background = Image()   # The background image


def rand() -> int:
    """Return a random integer (used for demo purposes)."""
    return random.randint(0, 32768)


def init_program() -> None:
    """
    Initialize pygame, graphics, images, and input system.
    Returns True if all resources loaded successfully.
    """
    pygame.init()

    if not graphics.init(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN):
        return False

    pygame.display.set_caption("Input Test")

    if not sprite.load("graphics/spaceship.bmp", 150, 120):
        return False

    if not background.load("graphics/background.bmp"):
        return False

    myinput.init()

    return True

def free_program() -> None:
    """Release all resources and quit pygame."""
    sprite.free()
    background.free()
    myinput.kill()
    pygame.quit()


def program_is_running() -> bool:
    """Return True if the main loop should continue running."""
    return not myinput.get_event(pygame.QUIT)


def main() -> int:
    """
    Main game loop: handles input, updates, and rendering.
    Returns 0 on normal exit.
    """
    sprite_x = 300
    sprite_y = 300

    if not init_program():
        free_program()
        return False

    while program_is_running():
        # --- Input handling ---
        myinput.update()

        if myinput.key_down(pygame.K_ESCAPE):
            break

        frame_start = pygame.time.get_ticks()

        # Move sprite to mouse position if left or right mouse button pressed
        if myinput.mouse_down(Input.MOUSE_LEFT):
            sprite_x = myinput.get_mouse_x()
            sprite_y = myinput.get_mouse_y()

        if myinput.mouse_hit(Input.MOUSE_RIGHT):
            sprite_x = myinput.get_mouse_x()
            sprite_y = myinput.get_mouse_y()

        # Keyboard arrow keys move the sprite
        if myinput.key_down(pygame.K_UP):
            sprite_y -= SPRITE_SPEED

        if myinput.key_down(pygame.K_DOWN):
            sprite_y += SPRITE_SPEED

        if myinput.key_down(pygame.K_LEFT):
            sprite_x -= SPRITE_SPEED

        if myinput.key_down(pygame.K_RIGHT):
            sprite_x += SPRITE_SPEED

        # --- Rendering ---
        graphics.clear(0, 0, 0)

        background.draw(0, 0, graphics)

        sprite.draw(sprite_x, sprite_y, graphics)

        graphics.flip()

        # --- Frame timing ---
        frame_time = pygame.time.get_ticks() - frame_start
        delay = FRAME_TIME - frame_time

        if delay > 0:
            pygame.time.delay(int(delay))

    free_program()

    return 0


if __name__ == '__main__':
    main()
