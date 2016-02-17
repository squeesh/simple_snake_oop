import pygame
from controller import GameController
from snake import Snake
from wall import Wall
pygame.init()

SCALE = 2 # 1 for 1080p 2 for 2160p
SIZE = WIDTH, HEIGHT = (800*SCALE, 800*SCALE)
SQUARE_SCALE = 8*SCALE # size of squares

DIFFICULTY_PER_APPLE = 0.0065 # higher = harder...
LENGTH_PER_APPLE = 10

screen = pygame.display.set_mode(SIZE)


class PySnake(Snake):
    def render(self):
        for i in range(0, self._length):
            seg_x, seg_y = self._segments[i]
            pygame.draw.rect(screen, PyGameController.GREEN, [seg_x*SQUARE_SCALE, seg_y*SQUARE_SCALE, SQUARE_SCALE, SQUARE_SCALE])


class PyWall(Wall):
    def render(self):
        pygame.draw.rect(screen, PyGameController.BLUE, [self._x*SQUARE_SCALE, self._y*SQUARE_SCALE, SQUARE_SCALE, SQUARE_SCALE])


class PyGameController(GameController):
    SnakeCls = PySnake
    WallCls = PyWall

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

    # START_SPEED = 0.5

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
ctrl.run()

