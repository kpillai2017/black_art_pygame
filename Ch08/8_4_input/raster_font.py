
# raster_font.py
# Provides the RasterFont class for rendering bitmap fonts using sprite sheets.

from dataclasses import dataclass
from image import Image
from graphics import Graphics



@dataclass
class RasterFont:
    """
    Handles loading and rendering of bitmap (raster) fonts using a sprite sheet image.
    """
    def __init__(self):
        # Number of columns in the sprite sheet
        self.NUM_COLUMNS = 16
        # ASCII code of the first character in the font
        self.START_CHAR = 32
        # The Image object containing the font sprite sheet
        self.image = Image()
        # Size of each character cell
        self.char_size = 0

    def load(self, file_spec: str) -> bool:
        """
        Load the font sprite sheet from file_spec.
        Returns True if successful, False otherwise.
        """
        if not self.image.load(file_spec):
            return False

        self.char_size = self.image.get_width() / self.NUM_COLUMNS
        self.image.set_frame_size(self.char_size, self.char_size)

        return True

    def draw(self, text: str, x: int, y: int, g: Graphics) -> None:
        """
        Draw the given text at (x, y) using the loaded bitmap font.
        """
        if not self.image.is_loaded():
            return

        for i in range(len(text)):
            self.image.draw(x + i * self.char_size, y, ord(text[i]) - self.START_CHAR, g)

    def free(self) -> None:
        """
        Free the font image resources.
        """
        self.image.free()
