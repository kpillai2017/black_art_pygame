import pygame
import pygame.gfxdraw
from dataclasses import dataclass


@dataclass
class Music:
    def __init__(self):
        self.music = None

    def load(self, file_spec: str) -> bool:
        pygame.mixer.music.load(file_spec)
        self.music = True

        # if self.music is None:
        #     print(f"Failed to load song: {file_spec}")
        #     return False

        return True

    def free(self) -> None:
        if self.music is not None:
            music = None

    def play(self, loops: int) -> None:
        if self.music:
            pygame.mixer.music.play(loops)

    def is_loaded(self) -> None:
        return self.music

    def music_playing(self) -> bool:
        return pygame.mixer.music.get_busy()
