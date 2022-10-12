import math


class Circle:
    def __init__(self):
        self.type = 'circle'
    def create(self, canvas, first_x, first_y, last_x, last_y, **kwargs):
        r = self.length_between_points(first_x, first_y, last_x, last_y)
        self.shape = canvas.create_oval(first_x - r, first_y - r, first_x + r, first_y + r, tags="circle", **kwargs)
        return self.shape

    def length_between_points(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

    def move(self, x, y):
        self.shape.move(x, y)
