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
        self.manager = StateManager()
        self.run_state = RunState()
        self.splash_state = SplashState()

    def init(self) -> bool:
        if not self.init_system("Game State Demo", 800, 600, False):
            return False

        if not self.run_state.init(self.get_input(), self.manager):
            return False

        if not self.splash_state.init(self.get_input(), self.manager):
            return False

        self.manager.add_state(self.run_state)
        self.manager.add_state(self.splash_state)

        return True

    def free(self) -> None:
        self.run_state.free()
        self.splash_state.free()

    def update(self) -> None:
        if self.manager.is_empty():
            self.end()
            return

        self.manager.update()

    def draw(self, g: Graphics) -> None:
        self.manager.draw(g)
