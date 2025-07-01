
# RasterFont module for drawing bitmap fonts using an image spritesheet
from dataclasses import dataclass
from image import Image
from graphics import Graphics


@dataclass
class RasterFont:
    def __init__(self):
        # Number of columns in the font spritesheet
        self.NUM_COLUMNS = 16
        # ASCII code of the first character
        self.START_CHAR = 32
        # Image object for the font
        self.image = Image()
        # Size of each character
        self.char_size = 0

    def load(self, file_spec: str) -> bool:
        # Load the font image and set up character size
        if not self.image.load(file_spec):
            return False
        self.char_size = self.image.get_width() / self.NUM_COLUMNS
        self.image.set_frame_size(self.char_size, self.char_size)
        return True

    def draw(self, text: str, x: int, y: int, g: Graphics) -> None:
        # Draw a string using the raster font at (x, y)
        if not self.image.is_loaded():
            return
        for i in range(len(text)):
            self.image.draw(x + i * self.char_size, y, ord(text[i]) - self.START_CHAR, g)

    def free(self) -> None:
        # Free the font image resource
        self.image.free()
