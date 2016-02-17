class Renderable(list):
    def __init__(self, x, y):
        self.extend((x, y))

    def render(self):
        raise NotImplementedError
