
# SplashState represents the splash/intro screen with logo animation and sound
import pygame
from dataclasses import dataclass
from state import GameState, StateManager
from graphics import Graphics
from image import Image
from input import Input
from sound import Sound

TARGET_Y = 300

@dataclass
class SplashState(GameState):
    def __init__(self):
        super().__init__()
        self.input = Input()
        self.background_image = Image()
        self.logo_image = Image()
        self.sound = Sound()
        self.logo_image_x = 0
        self.logo_image_y = 0
        self.sound_played = 0

    def init(self, i: Input, m: StateManager) -> bool:
        """Initialize splash state with images and sound"""
        self.input = i
        self.set_manager(m)
        if not self.background_image.load("graphics/splash/background.bmp"):
            return False
        if not self.logo_image.load("graphics/splash/logo.bmp"):
            return False
        if not self.sound.load("audio/splash/sound.wav"):
            return False
        self.logo_image_y = self.logo_image.get_height()
        self.sound_played = False
        return True

    def free(self) -> None:
        """Free splash state resources."""
        self.logo_image.free()
        self.background_image.free()
        self.sound.free()

    def update(self) -> None:
        """Animate logo and handle input to exit splash screen."""
        if self.input.key_hit(pygame.K_SPACE) or \
                self.input.key_hit(pygame.K_ESCAPE) or \
                self.input.key_hit(pygame.K_RETURN):
            self.get_manager().pop_state()
        # Animate logo dropping down
        if self.logo_image_y < TARGET_Y - (self.logo_image.get_height() / 2):
            self.logo_image_y += 10
        elif not self.sound_played:
            self.sound.play()
            self.sound_played = True

    def draw(self, g: Graphics) -> None:
        self.background_image.draw(0, 0, g)
        self.logo_image.draw(g.get_width() / 2 - self.logo_image.get_width() / 2, self.logo_image_y, g)
