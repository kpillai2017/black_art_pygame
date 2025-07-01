
# Audio module for handling music and sound playback using pygame
import pygame
import pygame.gfxdraw
from dataclasses import dataclass
from music import Music

@dataclass
class Audio:
    def __init__(self):
        # Track if music is currently playing
        self.is_music_playing = False
        # Music object for background music
        self.music = Music()

    def init(self) -> bool:
        # Initialise the audio system
        pygame.mixer.pre_init(22050, -16, 2, 2048)
        pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init(22050, -16, 2, 2048)
        return True

    def kill(self) -> None:
        # Shut down the audio system
        pygame.mixer.quit()

    def music_play(self, loops=0) -> None:
        # Play music with optional looping
        self.music.play(loops)
        self.is_music_playing = True

    def music_playing(self) -> bool:
        # Check if music is currently playing
        return self.music.music_playing()

    def music_paused(self) -> bool:
        # Check if music is paused
        return not self.is_music_playing

    def pause_music(self) -> None:
        # Pause the music playback
        pygame.mixer.music.pause()
        self.is_music_playing = False

    def resume_music(self) -> None:
        # Resume the music playback
        pygame.mixer.music.unpause()
        self.is_music_playing = True

    def stop_music(self) -> None:
        # Stop the music playback
        pygame.mixer.music.stop()
        self.is_music_playing = False

    def stop_channel(self, channel: pygame.mixer.Channel) -> None:
        # Stop playback on a specific channel
        channel.stop()
