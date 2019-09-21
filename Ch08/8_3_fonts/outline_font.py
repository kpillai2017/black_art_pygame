import pygame
from dataclasses import dataclass
from graphics import Graphics


@dataclass
class OutlineFont:
    def __init__(self):
        self.font = 0
        pygame.init()

    def load(self, file_spec: str, size: int) -> bool:
        self.font = pygame.font.Font(file_spec, size)
        if not self.font:
            return False

        return True

    def free(self) -> None:
        if self.font is not None:
            pygame.font.quit()

    def draw(self, text: str, x: int, y: int, r: int, g: int, b: int, gfx: Graphics) -> None:
        if not self.font:
            return False

        surface = self.font.render(text, True, (r, g, b))
        gfx.get_backbuffer().blit(surface, (x, y))
