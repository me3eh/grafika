import math


class Circle:
    def __init__(self):
        self.type = 'circle'

    def create(self, canvas, *points, **kwargs):
        print(points)
        r = self.length_between_points(*points)
        points = points[0]
        print(points)
        self.shape = canvas.create_oval(points[0] - r, points[1] - r, points[0] + r, points[1] + r,
                                        tags=self.type, **kwargs)
        return self.shape

    def length_between_points(self, *points):
        print(points)
        points = points[0]
        print(points)

        return math.sqrt(math.pow(points[2] - points[0], 2) + math.pow(points[3] - points[1], 2))

    def move(self, x, y):
        self.shape.move(x, y)
