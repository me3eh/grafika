from tkinter import ROUND, TRUE


class Line:
    def __init__(self):
        self.type = 'line'
    def create(self, canvas, *points, **kwargs):
        return canvas.create_line(*points, capstyle=ROUND, smooth=TRUE, splinesteps=36,
                                  tags='line', **kwargs)
