import pygame

from controller import GameController
from snake import Snake, SnakeSegment
from wall import Wall
from apple import Apple

pygame.init()

SCALE = 2 # 1 for 1080p 2 for 2160p
SIZE = WIDTH, HEIGHT = (800*SCALE, 800*SCALE)
SQUARE_SCALE = 8*SCALE # size of squares

DIFFICULTY_PER_APPLE = 0.0065 # higher = harder...
LENGTH_PER_APPLE = 10

screen = pygame.display.set_mode(SIZE)


class PySnakeSegment(SnakeSegment):
    def render(self):
        x, y = self
        pygame.draw.rect(screen, PyGameController.GREEN, [x*SQUARE_SCALE, y*SQUARE_SCALE, SQUARE_SCALE, SQUARE_SCALE])


class PySnake(Snake):
    SnakeSegmentCls = PySnakeSegment


class PyWall(Wall):
    def render(self):
        x, y = self
        pygame.draw.rect(screen, PyGameController.BLUE, [x*SQUARE_SCALE, y*SQUARE_SCALE, SQUARE_SCALE, SQUARE_SCALE])


class PyApple(Apple):
    def render(self):
        x, y = self
        pygame.draw.rect(screen, PyGameController.YELLOW, [x*SQUARE_SCALE, y*SQUARE_SCALE, SQUARE_SCALE, SQUARE_SCALE])


class PyGameController(GameController):
    SnakeCls = PySnake
    WallCls = PyWall
    AppleCls = PyApple

    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    KEY_MAP = {
        pygame.K_UP: GameController.KEY_UP,
        pygame.K_DOWN: GameController.KEY_DOWN,
        pygame.K_LEFT: GameController.KEY_LEFT,
        pygame.K_RIGHT: GameController.KEY_RIGHT,
        pygame.K_ESCAPE: GameController.KEY_ESC,
    }

    def main_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

            if event.type == pygame.KEYDOWN and event.key in PyGameController.KEY_MAP:
                self.key_down(PyGameController.KEY_MAP[event.key])

        super(PyGameController, self).main_loop()

    def render(self):
        screen.fill(self.BLACK)
        super(PyGameController, self).render()
        pygame.display.flip()


# while True:
ctrl = PyGameController.get()
ctrl.start()

