from tkinter import ROUND, TRUE


class Triangle:
    def __init__(self):
        self.type = 'triangle'

    def create(self, canvas, *points, **kwargs):
        return canvas.create_polygon(*points, tags=self.type, **kwargs)
