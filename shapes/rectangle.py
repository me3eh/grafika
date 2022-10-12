from tkinter import ROUND, TRUE


class Rectangle:
    def __init__(self):
        self.type = 'rectangle'
    def create(self, canvas, *points, **kwargs):
        return canvas.create_rectangle(*points, tags=self.type, **kwargs)
