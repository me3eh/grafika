from tkinter import ROUND, TRUE


class Rectangle:
    def __init__(self):
        self.type = 'rectangle'
    def create(self, canvas, first_x, first_y, last_x, last_y, **kwargs):
        return canvas.create_rectangle(first_x, first_y, last_x, last_y, tags='rectangle', **kwargs)
