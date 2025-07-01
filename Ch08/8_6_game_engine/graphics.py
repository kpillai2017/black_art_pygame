
# Graphics module for drawing and managing the display surface
import pygame
import pygame.gfxdraw
from dataclasses import dataclass


@dataclass
class Graphics:
    def __init__(self):
        # The main drawing surface (pygame Surface)
        self.backbuffer = 0
        self.width = 0
        self.height = 0

    def init(self, a_width: int, a_height: int, a_fullscreen: bool) -> bool:
        # Initialise the graphics system and create the display surface
        self.width = a_width
        self.height = a_height
        if a_fullscreen:
            self.backbuffer = pygame.display.set_mode(
                (self.width, self.height),
                pygame.SWSURFACE | pygame.SWFULLSCREEN, 32)
        else:
            self.backbuffer = pygame.display.set_mode(
                (self.width, self.height),
                pygame.SWSURFACE, 32)
        if self.backbuffer is None:
            print(f"Failed to initialise graphics!")
            return False
        return True

    def draw_pixel(self, x: int, y: int, r: int, g: int, b: int) -> None:
        # Draw a single pixel at (x, y) with the given color
        if self.backbuffer is None:
            return
        if self.backbuffer.mustlock():
            self.backbuffer.lock()
            if not self.backbuffer.get_locked():
                return
        if x >= self.backbuffer.get_width() or x < 0 or y >= self.backbuffer.get_height() or y < 0:
            return
        pygame.gfxdraw.pixel(self.backbuffer, x, y, (r, g, b))
        if self.backbuffer.mustlock():
            self.backbuffer.unlock()

    def draw_rect(self, x: int, y: int, width: int, height: int, r: int, g: int, b: int) -> None:
        # Draw a rectangle outline
        pygame.draw.rect(self.backbuffer, (r, g, b), (x, y, width, height), 1)

    def fill_rect(self, x: int, y: int, width: int, height: int, r: int, g: int, b: int) -> None:
        # Draw a filled rectangle
        pygame.draw.rect(self.backbuffer, (r, g, b), (x, y, width, height))

    def clear(self, r: int, g: int, b: int) -> None:
        # Clear the screen with the given color
        if self.backbuffer is None:
            return
        self.fill_rect(0, 0, self.get_width(), self.get_height(), r, g, b)

    def get_width(self) -> int:
        # Get the width of the display surface
        return self.width

    def get_height(self) -> int:
        # Get the height of the display surface
        return self.height

    def get_backbuffer(self) -> pygame.Surface:
        # Get the backbuffer surface
        return self.backbuffer

    @staticmethod
    def flip() -> None:
        # Update the display with the contents of the backbuffer
        pygame.display.flip()
