

class Wall(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_coord(self):
        return (self._x, self._y)

    def render(self):
        raise NotImplementedError



