from tkinter import ROUND, TRUE


class Triangle:
    def __init__(self):
        self.type = 'triangle'

    def create(self, canvas, first_x, first_y, last_x, last_y, **kwargs):
        return canvas.create_rectangle(first_x, first_y, last_x, last_y, **kwargs)
