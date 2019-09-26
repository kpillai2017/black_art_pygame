import pygame
import pygame.gfxdraw
import os
from dataclasses import dataclass


@dataclass
class Image:
    def __init__(self):
        self.surface = 0
        self.width = 0
        self.height = 0
        self.frame_width = 0
        self.frame_height = 0

    def load(self, file_spec: str, *args) -> bool:
        i_list = []

        dir_name = os.path.dirname(file_spec)
        file_name = os.path.basename(file_spec)

        image_loaded = pygame.image.load(os.path.join(dir_name, file_name))
        self.surface = image_loaded.convert()

        if self.surface is not None:
            self.surface.set_colorkey((255, 0, 255))
            self.width = self.surface.get_width()
            self.height = self.surface.get_height()

            # for method overloading, may include 2 parm for width and height
            # get the two optional parameters
            for arg in args:
                i_list.append(arg)

            # process iff there are the 2 parameters
            if len(i_list) == 2:
                self.frame_width = i_list[0]
                self.frame_height = i_list[1]

        else:
            print(f"Failed to load image: {file_name}")
            return False

        return True

    def draw(self, x: int, y: int, *args) -> None:
        if not self.surface:
            return

        i_list = []

        for arg in args:
            i_list.append(arg)

        # process iff there are 1 or 2 parameters after x and y
        # if one parameter, it's the Graphics() instance
        if len(i_list) == 1:
            i_list[0].get_backbuffer().blit(self.surface, (x, y))

        elif len(i_list) == 2:
            columns = self.surface.get_width() / self.frame_width

            src_rect_y = (i_list[0] // columns) * self.frame_height
            src_rect_x = (i_list[0] % columns) * self.frame_width
            src_rect_w = self.frame_width
            src_rect_h = self.frame_height

            i_list[1].get_backbuffer().blit(
                self.surface, (x, y),
                (src_rect_x, src_rect_y, src_rect_w, src_rect_h))

    def free(self) -> None:
        self.surface = 0

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_frame_width(self) -> int:
        return self.frame_width

    def get_frame_height(self) -> int:
        return self.frame_height

    def set_frame_size(self, w: int, h: int) -> None:
        self.frame_width = w
        self.frame_height = h

    def is_loaded(self) -> bool:
        return self.surface is not None
