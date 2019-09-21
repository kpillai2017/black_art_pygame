from dataclasses import dataclass
from image import Image
from graphics import Graphics


@dataclass
class RasterFont:
    def __init__(self):
        self.NUM_COLUMNS = 16
        self.START_CHAR = 32
        self.image = Image()
        self.char_size = 0

    def load(self, file_spec: str) -> bool:
        if not self.image.load(file_spec):
            return False

        self.char_size = self.image.get_width() / self.NUM_COLUMNS
        self.image.set_frame_size(self.char_size, self.char_size)

        return True

    def draw(self, text: str, x: int, y: int, g: Graphics) -> None:
        if not self.image.is_loaded():
            return

        for i in range(len(text)):
            self.image.draw(x + i * self.char_size, y, ord(text[i]) - self.START_CHAR, g)

    def free(self) -> None:
        self.image.free()
