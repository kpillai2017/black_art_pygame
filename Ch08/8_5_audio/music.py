
# music.py
# Provides a Music class for loading and controlling background music playback using pygame.

import pygame
import pygame.gfxdraw
from dataclasses import dataclass



@dataclass
class Music:
    """
    Music class manages loading, playing, and freeing background music.
    """
    def __init__(self):
        self.music = None  # Track if music is loaded

    def load(self, file_spec: str) -> bool:
        """
        Load a music file for playback.
        """
        pygame.mixer.music.load(file_spec)
        self.music = True
        # If loading fails, self.music would remain None
        return True

    def free(self) -> None:
        """
        Free the loaded music resource.
        """
        if self.music is not None:
            music = None

    def play(self, loops: int) -> None:
        """
        Play the loaded music, looping if specified.
        """
        if self.music:
            pygame.mixer.music.play(loops)

    def is_loaded(self) -> None:
        """
        Check if music is loaded.
        """
        return self.music

    def music_playing(self) -> bool:
        """
        Return True if music is currently playing.
        """
        return pygame.mixer.music.get_busy()
