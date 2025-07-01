
# outline_font.py
# Provides an OutlineFont class for rendering text with a font using pygame.

import pygame
from dataclasses import dataclass
from graphics import Graphics



@dataclass
class OutlineFont:
    """
    OutlineFont class for loading a font and rendering text to the screen.
    """
    def __init__(self):
        self.font = 0  # The pygame font object
        pygame.init()

    def load(self, file_spec: str, size: int) -> bool:
        """
        Load a font from file with the given size.
        """
        self.font = pygame.font.Font(file_spec, size)
        if not self.font:
            return False
        return True

    def free(self) -> None:
        """
        Free the loaded font resource.
        """
        if self.font is not None:
            pygame.font.quit()

    def draw(self, text: str, x: int, y: int, r: int, g: int, b: int, gfx: Graphics) -> None:
        """
        Draw the given text at (x, y) with the specified color using the loaded font.
        """
        if not self.font:
            return False
        surface = self.font.render(text, True, (r, g, b))
        gfx.get_backbuffer().blit(surface, (x, y))
