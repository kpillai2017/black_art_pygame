from dataclasses import dataclass
from stack import Stack
from graphics import Graphics


@dataclass
class GameState:
    def __init__(self):
        self.manager = None

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def get_manager(self):
        return self.manager

    def set_manager(self, m) -> None:
        self.manager = m


@dataclass
class StateManager:
    def __init__(self):
        self.states = Stack()

    def add_state(self, s: GameState) -> None:
        s.set_manager(self)
        self.states.push(s)

    def pop_state(self) -> GameState:
        self.states.pop()

    def update(self) -> None:
        if not self.states.is_empty():
            if self.states.peek() is not None:
                self.states.peek().update()

    def draw(self, g: Graphics) -> None:
        if not self.states.is_empty():
            if self.states.peek() is not None:
                self.states.peek().draw(g)

    def is_empty(self) -> bool:
        return self.states.is_empty()
