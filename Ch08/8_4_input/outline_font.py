
# outline_font.py
# Provides the OutlineFont class for rendering outlined text using pygame.

import pygame
from dataclasses import dataclass
from graphics import Graphics



@dataclass
class OutlineFont:
    """
    Handles loading and rendering of outlined fonts using pygame's font system.
    """
    def __init__(self):
        # The pygame Font object
        self.font = 0
        pygame.init()

    def load(self, file_spec: str, size: int) -> bool:
        """
        Load a font from file_spec with the given size.
        Returns True if successful, False otherwise.
        """
        self.font = pygame.font.Font(file_spec, size)
        if not self.font:
            return False

        return True

    def free(self) -> None:
        """
        Free the font resources.
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
