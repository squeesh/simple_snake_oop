from collections import deque


class Snake(object):
    UP = 'u'
    DOWN = 'd'
    LEFT = 'l'
    RIGHT = 'r'

    _OPPOSITE_MAP = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT,
    }

    _segments = ()
    _length = 0

    def __init__(self, x=1, y=1, direction=RIGHT, length=5):
        self._dir_buffer = deque([direction])
        self._segments = [(x, y)]
        self.add_length(length)

    def add_length(self, new_length):
        for i in range(0, new_length):
            self._length += 1
            self._segments.append((-1, -1))  # Add just off screen

    def set_direction(self, new_direction):
        if self._dir_buffer[-1] != new_direction and self._OPPOSITE_MAP[self._dir_buffer[-1]] != new_direction:
            self._dir_buffer.append(new_direction)

    def move(self):
        if len(self._dir_buffer) > 1:
            self._dir_buffer.popleft()

        direction = self._dir_buffer[0]

        snake_x, snake_y = self._segments[0]
        if direction == self.RIGHT:
            snake_x += 1
        elif direction == self.LEFT:
            snake_x -= 1
        elif direction == self.DOWN:
            snake_y += 1
        elif direction == self.UP:
            snake_y -= 1

        for i in range(self._length-2, -1, -1):
            self._segments[i+1] = self._segments[i]

        self._segments[0] = (snake_x, snake_y)

    def get_coord(self):  # Minor hack until SnakeSegment implemented as Renderable
        return self._segments[0]

    def get_head(self):
        return self._segments[0]

    def get_tail(self):
        return self._segments[1:]

    def render(self):
        raise NotImplementedError


# class SnakeSegment(object):
#     pass
