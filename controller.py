from time import sleep
import sys
from snake import Snake


class GameController(object):
    SnakeCls = Snake

    KEY_UP = 'u'
    KEY_DOWN = 'd'
    KEY_LEFT = 'l'
    KEY_RIGHT = 'r'
    KEY_ESC = 'esc'

    KEY_BINDS = {  # This may not work as expected... investigate...
        KEY_UP: SnakeCls.UP,
        KEY_DOWN: SnakeCls.DOWN,
        KEY_LEFT: SnakeCls.LEFT,
        KEY_RIGHT: SnakeCls.RIGHT,
    }

    _controller = None

    _halt = False
    _pause = False

    _snake = None
    _walls = ()
    _apples = ()

    def __init__(self):
        self._snake = self.SnakeCls()

    @classmethod
    def get(cls):
        if not cls._controller:
            cls._controller = cls()
        return cls._controller

    def exit(self):
        sys.exit()

    def halt(self):
        self._halt = True

    def key_down(self, key):
        if key == self.KEY_ESC:
            self.exit()

        if key in self.KEY_BINDS:
            self._snake.set_direction(self.KEY_BINDS[key])

    def render(self):
        for wall in self._walls:
            wall.render()

        self._snake.render()

        for apple in self._apples:
            apple.render()

    def run(self):
        while not self._halt:
            self.main_loop()
            sleep(0.1)

    def main_loop(self):
        self._snake.move()
        self.render()
