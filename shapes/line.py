from tkinter import ROUND, TRUE


class Line:
    def __init__(self):
        self.type = 'line'
    def create(self, canvas, first_x, first_y, last_x, last_y, **kwargs):
        return canvas.create_line(first_x, first_y, last_x, last_y, capstyle=ROUND, smooth=TRUE, splinesteps=36,
                                  tags='line', **kwargs)

# print(Line().type)
