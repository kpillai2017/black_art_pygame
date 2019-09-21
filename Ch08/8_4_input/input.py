import pygame
import pygame.gfxdraw
from dataclasses import dataclass


@dataclass
class Input:
    MOUSE_LEFT = 0
    MOUSE_MIDDLE = 1
    MOUSE_RIGHT = 2

    def __init__(self):
        self.keys = []
        self.prev_keys = []
        self.mouse_keys = [0 for i in range(3)]
        self.prev_mouse_keys = [0 for i in range(3)]

        self.num_keys = 0
        self.mouse_x = 0
        self.mouse_y = 0

    def init(self) -> None:
        keyboard = pygame.key.get_pressed()

        self.num_keys = len(keyboard)
        self.keys = keyboard[:]
        self.prev_keys = [False for i in range(len(keyboard))]

        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]
        self.mouse_keys = pygame.mouse.get_pressed()
        self.prev_mouse_keys = [False for i in range(len(self.mouse_keys))]

    def kill(self) -> None:
        self.keys = []
        self.prev_keys = []

    def update(self) -> None:
        keyboard = pygame.key.get_pressed()

        self.prev_keys = self.keys[:]
        self.keys = keyboard[:]

        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]
        self.prev_mouse_keys = self.mouse_keys[:]
        self.mouse_keys = pygame.mouse.get_pressed()

    def key_down(self, key: int) -> bool:
        if key < 0 or key > self.num_keys:
            return False

        return self.keys[key]

    def key_hit(self, key: int) -> bool:
        if key < 0 or key > self.num_keys:
            return False

        return self.keys[key] and not self.prev_keys[key]

    def key_up(self, key: int) -> bool:
        if key < 0 or key > self.num_keys:
            return False

        return self.prev_keys[key] and not self.keys[key]

    def mouse_down(self, key: int) -> int:
        if key < 0 or key > 3:
            return False

        return self.mouse_keys[key]

    def mouse_hit(self, key: int) -> bool:
        if key < 0 or key > 3:
            return False

        return self.mouse_keys[key] and not self.prev_mouse_keys[key]

    def mouse_up(self, key: int) -> bool:
        if key < 0 or key > 3:
            return False

        return self.prev_mouse_keys[key] and not self.mouse_keys[key]

    def get_mouse_x(self) -> int:
        return self.mouse_x

    def get_mouse_y(self) -> int:
        return self.mouse_y

    def set_mouse_pos(self, x: int, y: int) -> None:
        pygame.mouse.set_pos([x, y])

    def hide_cursor(self, hide: bool) -> None:
        if hide:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
