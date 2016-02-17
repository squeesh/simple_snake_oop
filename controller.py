from random import randint
from time import sleep
import sys

from snake import Snake
from wall import Wall
from apple import Apple
from exception import LevelNotFoundException, GameOverException


class GameController(object):
    SnakeCls = Snake
    WallCls = Wall
    AppleCls = Apple

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

    DIFFICULTY = 0.0065 # higher = harder...
    PER_APPLE = 10

    START_SPEED = 0.1
    MAX_APPLES = 15

    _controller = None

    _halt = False
    _pause = False

    _snake = None
    _walls = ()
    _apples = ()

    def __init__(self):
        self._game_speed = self.START_SPEED
        self._snake = self.SnakeCls()
        self._walls, self._apples = self.generate_level(1)

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

    def _check_collisions(self):
        snake_head_coord = self._snake.get_head()
        # wall_coords = [wall.get_coord() for wall in self._walls]
        # apple_coords = [apple.get_coord() for apple in self._apples]

        if snake_head_coord in self._snake.get_tail() or snake_head_coord in self._walls:
            raise GameOverException()

    def _check_eat_apple(self):
        snake_head_coord = self._snake.get_head()
        if snake_head_coord in self._apples:
            index = self._apples.index(snake_head_coord)
            self._apples.pop(index)
            self._snake.add_length(self.PER_APPLE)
            self._game_speed -= self.DIFFICULTY

    def run(self):
        while not self._halt:
            self.main_loop()
            sleep(self._game_speed)

    def main_loop(self):
        self._snake.move()
        self._check_collisions()
        self._check_eat_apple()
        self.render()

    @classmethod
    def generate_level(cls, level):
        level -= 1  # convert to 0 base

        def _level_1():
            outer_walls = \
                [(i, 0) for i in range(1, 99)] + \
                [(i, 99) for i in range(1, 99)] + \
                [(0, i) for i in range(1, 99)] + \
                [(99, i) for i in range(1, 99)]
            inner_walls = \
                [(i, 48) for i in range(48, 52)] + \
                [(i, 51) for i in range(48, 52)] + \
                [(48, i) for i in range(49, 51)] + \
                [(51, i) for i in range(49, 51)] + \
                [(49, i) for i in range(49, 51)] + \
                [(50, i) for i in range(49, 51)]
            walls = tuple(outer_walls + inner_walls)

            # wall_coords = [wall.get_coord() for wall in walls]

            apples = []
            # apple_coords = []
            for i in range(0, cls.MAX_APPLES):
                while True:
                    apple_coord = (randint(1, 99), randint(1, 99))
                    if apple_coord not in walls and apple_coord not in apples:
                        apples.append(apple_coord)
                        break

            return walls, apples

        available_levels = [_level_1]#, _level_2, _level_3]

        if level in range(0, len(available_levels)):
            return available_levels[level]()

        raise LevelNotFoundException()

