import pygame
import pygame.gfxdraw
from dataclasses import dataclass
from graphics import Graphics
from input import Input
from audio import Audio


@dataclass
class Game:
    def __init__(self):
        self.graphics = Graphics()
        self.input = Input()
        self.audio = Audio()
        self.is_done = False
        self.fps = 30

    def get_ticks(self) -> int:
        return pygame.time.get_ticks()

    def set_fps(self, f: int) -> None:
        self.fps = f

    def delay(self, ticks: int) -> None:
        if ticks > 0:
            pygame.time.delay(int(ticks))

    def init_system(self, title: str, width: int, height: int, fullscreen: bool) -> bool:
        pygame.mixer.pre_init(22050, -16, 2, 2048)
        pygame.init()

        if not self.graphics.init(width, height, fullscreen):
            return False

        pygame.display.set_caption(title)

        if not self.audio.init():
            return False

        self.input.init()

        return True

    def free_system(self) -> None:
        self.input.kill()
        self.audio.kill()
        pygame.quit()

    def run(self) -> None:
        while not self.is_done:
            frame_start = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_done = True
                    break

            self.input.update()
            self.update()
            self.draw(self.get_graphics())

            self.get_graphics().flip()

            frame_time = pygame.time.get_ticks() - frame_start
            delay_time = (1000 / self.fps) - frame_time

            pygame.time.delay(int(delay_time))

        self.free()
        self.free_system()

    def end(self) -> None:
        self.is_done = True

    def init(self) -> bool:
        return self.init_system("Game", 800, 600, False)

    def free(self) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, g: Graphics) -> None:
        g.clear(255, 255, 255)

    def get_graphics(self) -> Graphics:
        return self.graphics

    def get_input(self) -> Input:
        return self.input

    def get_audio(self) -> Audio:
        return self.audio
