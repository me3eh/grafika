import math


class Circle:
    def __init__(self):
        self.type = 'circle'

    def create(self, canvas, *points, **kwargs):
        r = self.length_between_points(*points)
        points = points[0]
        self.shape = canvas.create_oval(points[0] - r, points[1] - r, points[0] + r, points[1] + r,
                                        tags=self.type, **kwargs)
        return self.shape

    def create_after_serialize(self, canvas, *points, **kwargs):
        self.shape = canvas.create_oval(*points, tags=self.type, **kwargs)
        return self.shape

    def length_between_points(self, points):
        # points = points[0]

        return math.sqrt(math.pow(points[2] - points[0], 2) + math.pow(points[3] - points[1], 2))

    def move(self, x, y):
        self.shape.move(x, y)
