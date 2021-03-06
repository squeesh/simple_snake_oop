from random import randint
from time import sleep
import sys

from snake import Snake, SnakeSegment
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

    HALT_PLAYER_WIN = 'win'
    HALT_PLAYER_LOSE = 'lose'

    _halt = None

    _snake = None
    _walls = ()
    _apples = ()

    def __init__(self):
        self._game_speed = self.START_SPEED
        self._snake = self.SnakeCls()

    @classmethod
    def get(cls):
        if not cls._controller:
            cls._controller = cls()
        return cls._controller

    @classmethod
    def destroy(cls):
        cls._controller = None

    def exit(self):
        sys.exit()

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

    def _check_collision_self(self):
        if self._snake.get_head() in self._snake.get_tail():
            self._halt = self.HALT_PLAYER_LOSE

    def _check_collision_wall(self):
        if self._snake.get_head() in self._walls:
            self._halt = self.HALT_PLAYER_LOSE

    def _check_collision_apple(self):
        if self._snake.get_head() in self._apples:
            index = self._apples.index(self._snake.get_head())
            self._apples.pop(index)
            self._snake.add_length(self.PER_APPLE)
            self._game_speed -= self.DIFFICULTY

        if not self._apples:
            self._halt = self.HALT_PLAYER_WIN

    @classmethod
    def _generate_level(cls, level):
        level -= 1  # convert to 0 base

        def _gen_apples(walls):
            apples = []
            for i in range(0, cls.MAX_APPLES):
                while True:
                    apple = cls.AppleCls(randint(1, 99), randint(1, 99))
                    if apple not in walls and apple not in apples:
                        apples.append(apple)
                        break
            return apples

        def _level_1():
            outer_walls = \
                [cls.WallCls(i, 0) for i in range(1, 99)] + \
                [cls.WallCls(i, 99) for i in range(1, 99)] + \
                [cls.WallCls(0, i) for i in range(1, 99)] + \
                [cls.WallCls(99, i) for i in range(1, 99)]
            inner_walls = \
                [cls.WallCls(i, 48) for i in range(48, 52)] + \
                [cls.WallCls(i, 51) for i in range(48, 52)] + \
                [cls.WallCls(48, i) for i in range(49, 51)] + \
                [cls.WallCls(51, i) for i in range(49, 51)] + \
                [cls.WallCls(49, i) for i in range(49, 51)] + \
                [cls.WallCls(50, i) for i in range(49, 51)]
            return outer_walls + inner_walls

        def _level_2():
            outer_walls = \
                [cls.WallCls(i, 0) for i in range(1, 99)] + \
                [cls.WallCls(i, 99) for i in range(1, 99)] + \
                [cls.WallCls(0, i) for i in range(1, 99)] + \
                [cls.WallCls(99, i) for i in range(1, 99)]
            inner_walls = \
                [cls.WallCls(i, 49) for i in range(10, 90)] + \
                [cls.WallCls(i, 50) for i in range(10, 90)]
            return outer_walls + inner_walls

        available_levels = [_level_1, _level_2]#, _level_3]

        if level in range(0, len(available_levels)):
            level_walls = available_levels[level]()
            return level_walls, _gen_apples(level_walls)

        raise LevelNotFoundException()

    def get_halt_reason(self):
        return self._halt

    def start(self, starting_level):
        self._walls, self._apples = self._generate_level(starting_level)

        while not self._halt:
            self.main_loop()
            sleep(self._game_speed)

    def main_loop(self):
        self._snake.move()
        self._check_collision_self()
        self._check_collision_wall()
        self._check_collision_apple()
        self.render()

