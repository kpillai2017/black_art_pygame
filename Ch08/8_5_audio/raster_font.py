
# raster_font.py
# Provides a RasterFont class for rendering bitmap font text using an image spritesheet.

from dataclasses import dataclass
from image import Image
from graphics import Graphics



@dataclass
class RasterFont:
    """
    RasterFont class for loading a bitmap font and rendering text using an image spritesheet.
    """
    def __init__(self):
        self.NUM_COLUMNS = 16  # Number of columns in the font spritesheet
        self.START_CHAR = 32   # ASCII code of the first character
        self.image = Image()   # Image object for the font
        self.char_size = 0     # Size of each character

    def load(self, file_spec: str) -> bool:
        """
        Load the font image and set up frame size for each character.
        """
        if not self.image.load(file_spec):
            return False
        self.char_size = self.image.get_width() / self.NUM_COLUMNS
        self.image.set_frame_size(self.char_size, self.char_size)
        return True

    def draw(self, text: str, x: int, y: int, g: Graphics) -> None:
        """
        Draw the given text at (x, y) using the bitmap font.
        """
        if not self.image.is_loaded():
            return
        for i in range(len(text)):
            self.image.draw(x + i * self.char_size, y, ord(text[i]) - self.START_CHAR, g)

    def free(self) -> None:
        """
        Free the font image resource.
        """
        self.image.free()
