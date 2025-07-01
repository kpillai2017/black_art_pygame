
# RunState represents the main gameplay state with animated gear and background
import pygame
from dataclasses import dataclass
from state import GameState, StateManager
from graphics import Graphics
from image import Image
from input import Input

@dataclass
class RunState(GameState):
    def __init__(self):
        super().__init__()
        self.input = Input()
        self.background_image = Image()
        self.gear_image = Image()
        self.IMAGE_FRAMES = 5  # Number of animation frames.
        self.image_frame = 0
        self.frame_counter = 0

    def init(self, i: Input, m: StateManager) -> bool:
        """Initialize the run state with images and input."""
        self.input = i
        self.set_manager(m)
        if not self.background_image.load("graphics/run/background.bmp"):
            return False
        if not self.gear_image.load("graphics/run/gear.bmp", 400, 400):
            return False
        self.image_frame = 0
        self.frame_counter = 0
        return True

    def free(self) -> None:
        """Free resources for this state."""
        self.gear_image.free()
        self.background_image.free()

    def update(self) -> None:
        """Update animation and handle input to exit state."""
        if self.input.key_hit(pygame.K_ESCAPE):
            self.get_manager().pop_state()
        self.frame_counter += 1
        if self.frame_counter > 5:
            self.frame_counter = 0
            self.image_frame += 1
        if self.image_frame > self.IMAGE_FRAMES:
            self.image_frame = 0

    def draw(self, g: Graphics) -> None:
        """Draw the background and animated gear image."""
        self.background_image.draw(0, 0, g)
        self.gear_image.draw(
            g.get_width() / 2 - self.gear_image.get_frame_width() / 2,
            g.get_height() / 2 - self.gear_image.get_frame_height() / 2,
            self.image_frame, g)
