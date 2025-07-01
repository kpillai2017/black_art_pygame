
# State management classes for handling game states and transitions
from dataclasses import dataclass
from stack import Stack
from graphics import Graphics

@dataclass
class GameState:
    def __init__(self):
        # Reference to the state manager
        self.manager = None

    def update(self) -> None:
        """Override to update state logic."""
        pass

    def draw(self) -> None:
        """Override to draw state visuals."""
        pass

    def get_manager(self):
        """Return the state manager."""
        return self.manager

    def set_manager(self, m) -> None:
        """Set the state manager reference."""
        self.manager = m

@dataclass
class StateManager:
    def __init__(self):
        # Stack of game states
        self.states = Stack()

    def add_state(self, s: GameState) -> None:
        """Push a new state onto the stack."""
        s.set_manager(self)
        self.states.push(s)

    def pop_state(self) -> GameState:
        """Pop the current state from the stack."""
        self.states.pop()

    def update(self) -> None:
        """Update the current state if available."""
        if not self.states.is_empty():
            if self.states.peek() is not None:
                self.states.peek().update()

    def draw(self, g: Graphics) -> None:
        """Draw the current state if available."""
        if not self.states.is_empty():
            if self.states.peek() is not None:
                self.states.peek().draw(g)

    def is_empty(self) -> bool:
        """Return True if there are no states left."""
        return self.states.is_empty()
