class Renderable(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_coord(self):
        return (self._x, self._y)

    def render(self):
        raise NotImplementedError


class RenderableContainer(list):
    def __contains__(self, item):
        return item.get_coord() in [renderable.get_coord() for renderable in self]

    def index(self, item):
        return [renderable.get_coord() for renderable in self].index(item.get_coord())
