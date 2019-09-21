import pygame
import pygame.gfxdraw
from dataclasses import dataclass
from music import Music

@dataclass
class Audio:
    def __init__(self):
        self.is_music_playing = False
        self.music = Music()

    def init(self) -> bool:
        pygame.mixer.pre_init(22050, -16, 2, 2048)
        pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init(22050, -16, 2, 2048)

        return True

    def kill(self) -> None:
        pygame.mixer.quit()

    def music_play(self, loops=0) -> None:
        self.music.play(loops)
        self.is_music_playing = True

    def music_playing(self) -> bool:
        return self.music.music_playing()

    def music_paused(self) -> bool:
        return not self.is_music_playing

    def pause_music(self) -> None:
        pygame.mixer.music.pause()
        self.is_music_playing = False

    def resume_music(self) -> None:
        pygame.mixer.music.unpause()
        self.is_music_playing = True

    def stop_music(self) -> None:
        pygame.mixer.music.stop()
        self.is_music_playing = False

    def stop_channel(self, channel: pygame.mixer.Channel) -> None:
        channel.stop()
