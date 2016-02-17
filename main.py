import pygame
import sys

from controller import GameController
from snake import Snake, SnakeSegment
from wall import Wall
from apple import Apple

pygame.init()

SCALE = 2 # 1 for 1080p 2 for 2160p
SIZE = WIDTH, HEIGHT = (800*SCALE, 800*SCALE)
SQUARE_SCALE = 8*SCALE # size of squares

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

MAX_APPLES = 15
STARTING_LEVEL = 1

screen = pygame.display.set_mode(SIZE)


def render_obj(self):
    x, y = self
    pygame.draw.rect(screen, self.color, [x*SQUARE_SCALE, y*SQUARE_SCALE, SQUARE_SCALE, SQUARE_SCALE])


class PySnakeSegment(SnakeSegment):
    color = GREEN
    render = render_obj


class PyWall(Wall):
    color = BLUE
    render = render_obj


class PyApple(Apple):
    color = YELLOW
    render = render_obj


class PySnake(Snake):
    SnakeSegmentCls = PySnakeSegment


class PyGameController(GameController):
    SnakeCls = PySnake
    WallCls = PyWall
    AppleCls = PyApple

    MAX_APPLES = MAX_APPLES

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
        screen.fill(BLACK)
        super(PyGameController, self).render()
        pygame.display.flip()


def render_string(string, color):
    screen.fill(BLACK)
    PyGameController.get().render()
    font = pygame.font.Font(None, 36*SCALE)
    text = font.render(string, 1, color)
    textpos = text.get_rect(centerx=WIDTH/2, centery=HEIGHT/4)
    screen.blit(text, textpos)
    pygame.display.flip()


def pause_until_esc_or_exit():
    new_game = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                new_game = True

        if new_game:
            break

level = STARTING_LEVEL
while True:
    ctrl = PyGameController.get()
    ctrl.start(level)
    halt_reason = ctrl.get_halt_reason()
    if halt_reason == PyGameController.HALT_PLAYER_WIN:
        render_string('You Win! - Press ESC for next level', GREEN)
        level += 1
    else:
        render_string('You Lose! - Press ESC for new game', RED)
        level = STARTING_LEVEL
    pause_until_esc_or_exit()
    PyGameController.destroy()


