
# Demo game class that uses a state manager to switch between splash and run states
from dataclasses import dataclass
from game import Game
from graphics import Graphics
from state import GameState, StateManager
from run_state import RunState
from splash_state import SplashState

@dataclass
class GameStateDemo(Game):
    def __init__(self):
        super().__init__()
        # State manager and game states
        self.manager = StateManager()
        self.run_state = RunState()
        self.splash_state = SplashState()

    def init(self) -> bool:
        """Initialize the game and all states."""
        if not self.init_system("Game State Demo", 800, 600, False):
            return False

        if not self.run_state.init(self.get_input(), self.manager):
            return False

        if not self.splash_state.init(self.get_input(), self.manager):
            return False

        # Add states to the manager (splash on top)
        self.manager.add_state(self.run_state)
        self.manager.add_state(self.splash_state)
        return True

    def free(self) -> None:
        """Free resources for all states."""
        self.run_state.free()
        self.splash_state.free()

    def update(self) -> None:
        """Update the current state, or end if no states remain."""
        if self.manager.is_empty():
            self.end()
            return
        self.manager.update()

    def draw(self, g: Graphics) -> None:
        """Draw the current state."""
        self.manager.draw(g)
