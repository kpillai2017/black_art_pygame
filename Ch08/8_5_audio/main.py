import pygame, sys, os, random
from graphics import Graphics
from image import Image
from input import Input
from audio import Audio
from sound import Sound


FPS = 30
FRAME_TIME = 1000 / FPS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FULLSCREEN = False

graphics = Graphics()
audio = Audio()
myinput = Input()
sounds = [Sound() for i in range(5)]
background = Image()


def rand() -> int:
    return random.randint(0, 32768)


def init_program() -> bool:
    pygame.init()

    if not graphics.init(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN):
        return False

    pygame.display.set_caption("Audio Test")

    if not audio.init():
        return False

    if not background.load("graphics/background.bmp"):
        return False

    if not audio.music.load("audio/Loop.wav"):
        return False

    if not sounds[0].load("audio/Ahh.wav"):
        return False

    if not sounds[1].load("audio/Beep.wav"):
        return False

    if not sounds[2].load("audio/Punch.wav"):
        return False

    if not sounds[3].load("audio/Scream.wav"):
        return False

    if not sounds[4].load("audio/Telephone.wav"):
        return False

    myinput.init()

    return True


def free_program() -> None:
    audio.music.free()

    for i in range(len(sounds)):
        sounds[i].free()

    background.free()
    myinput.kill()
    audio.kill()
    pygame.quit()


def program_is_running() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    return True


def main() -> int:
    if not init_program():
        free_program()
        return False

    while program_is_running():
        myinput.update()

        if myinput.key_hit(pygame.K_SPACE):
            if not audio.music_playing():
                audio.music_play(-1)
            else:
                if audio.music_paused():
                    audio.resume_music()
                else:
                    audio.pause_music()

        if myinput.key_hit(pygame.K_ESCAPE):
            audio.stop_music()

        frame_start = pygame.time.get_ticks()

        if myinput.key_hit(pygame.K_1):
            sounds[0].play()

        if myinput.key_hit(pygame.K_2):
            sounds[1].play()

        if myinput.key_hit(pygame.K_3):
            sounds[2].play()

        if myinput.key_hit(pygame.K_4):
            sounds[3].play()

        if myinput.key_hit(pygame.K_5):
            sounds[4].play()

        graphics.clear(0, 0, 0)

        background.draw(0, 0, graphics)

        graphics.flip()

        frame_time = pygame.time.get_ticks() - frame_start
        delay = FRAME_TIME - frame_time

        if delay > 0:
            pygame.time.delay(int(delay))

    free_program()

    return 0


if __name__ == '__main__':
    main()
