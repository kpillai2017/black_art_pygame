
# graphics.py
# Provides a Graphics class for drawing and managing the display surface using pygame.

import pygame
import pygame.gfxdraw
from dataclasses import dataclass



@dataclass
class Graphics:
    """
    Graphics class handles the main drawing surface and basic drawing operations.
    """
    def __init__(self):
        self.backbuffer = 0  # The main drawing surface
        self.width = 0
        self.height = 0


    def init(self, a_width: int, a_height: int, a_fullscreen: bool) -> bool:
        """
        Initialize the display surface with the given width, height, and fullscreen mode.
        """
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
        """
        Draw a single pixel at (x, y) with the given RGB color.
        """
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
        """
        Draw an outlined rectangle at (x, y) with the given size and color.
        """
        pygame.draw.rect(self.backbuffer, (r, g, b), (x, y, width, height), 1)


    def fill_rect(self, x: int, y: int, width: int, height: int, r: int, g: int, b: int) -> None:
        """
        Draw a filled rectangle at (x, y) with the given size and color.
        """
        pygame.draw.rect(self.backbuffer, (r, g, b), (x, y, width, height))


    def clear(self, r: int, g: int, b: int) -> None:
        """
        Clear the screen to the given RGB color.
        """
        if self.backbuffer is None:
            return
        self.fill_rect(0, 0, self.get_width(), self.get_height(), r, g, b)

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_backbuffer(self) -> pygame.Surface:
        return self.backbuffer

    @staticmethod
    def flip() -> None:
        pygame.display.flip()
