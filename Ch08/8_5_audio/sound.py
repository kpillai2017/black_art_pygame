
# sound.py
# Provides a Sound class for loading and playing sound effects using pygame.

import pygame
import pygame.gfxdraw
from dataclasses import dataclass



@dataclass
class Sound:
    """
    Sound class for loading, playing, and freeing sound effects.
    """
    def __init__(self):
        self.sound = None  # The pygame Sound object
        # pygame.mixer.pre_init(22050, -16, 2, 1024)
        # pygame.init()
        # pygame.mixer.quit()
        # pygame.mixer.init(22050, -16, 2, 1024)

    def load(self, file_spec: str) -> bool:
        """
        Load a sound effect from file.
        """
        self.sound = pygame.mixer.Sound(file_spec)
        if not self.sound:
            print(f"Failed to load sound: {file_spec}")
            return False
        return True

    def free(self) -> None:
        """
        Free the loaded sound resource.
        """
        pygame.mixer.quit()
        self.sound = None

    def play(self, loops=0) -> int:
        """
        Play the loaded sound effect, optionally looping.
        Returns the channel or -1 if not loaded.
        """
        if self.sound is not None:
            return self.sound.play(loops)
        else:
            return -1

    def is_loaded(self) -> bool:
        """
        Check if the sound is loaded.
        """
        return self.sound is not None
