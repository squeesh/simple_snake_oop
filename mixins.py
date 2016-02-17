class Renderable(list):
    color = (255, 0, 0)

    def __init__(self, x, y):
        self.extend((x, y))

    def render(self):
        raise NotImplementedError
