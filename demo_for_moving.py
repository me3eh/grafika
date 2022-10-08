
import json
from tkinter import Tk, Canvas


class Circle:
    def __init__(self, parent: "Canvas", x, y):
        self.parent = parent
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.type = 'circle'
        self.allow_move = False
        self.move_offset_x = 0
        self.move_offset_y = 0

        self.circle = self.parent.create_oval(self.x, self.y, self.x + self.width, self.y + self.height, fill='black')

    def move(self, x, y):
        x, y = x - self.move_offset_x, y - self.move_offset_y
        self.x, self.y = x, y
        self.parent.coords(self.circle, x, y, x + self.width, y + self.height)


def check_coords(event=None):
    for obj in obj_lst:
        if obj.x < event.x < obj.x + obj.width and obj.y < event.y < obj.y + obj.width:
            obj.allow_move = True
            obj.move_offset_x = event.x - obj.x
            obj.move_offset_y = event.y - obj.y
            break


def move(event=None):
    for obj in obj_lst:
        if obj.allow_move:
            obj.move(event.x, event.y)


def set_moving_false(event=None):
    for obj in obj_lst:
        if obj.allow_move:
            obj.allow_move = False


def create_obj(event=None):
    obj_lst.append(Circle(canvas, event.x, event.y))


def save(event=None):
    with open('untitled.canvas', 'w') as file:
        obj_dict = {f'{obj.type} {id}': (obj.x, obj.y) for id, obj in enumerate(obj_lst)}
        json.dump(obj_dict, file)


root = Tk()

canvas = Canvas(root, width=500, height=400)
canvas.pack()


obj_type_dict = {'circle': Circle}

try:
    with open('untitled.canvas') as file:
        obj_dict = json.load(file)
        obj_lst = []
        for obj_type, attributes in obj_dict.items():
            obj = obj_type_dict[obj_type.split()[0]](canvas, attributes[0], attributes[1])
            obj_lst.append(obj)

except FileNotFoundError:
    with open('untitled.canvas', 'w') as file:
        pass
    obj_lst = []


canvas.bind('<Button-1>', check_coords)
canvas.bind('<B1-Motion>', move)
canvas.bind('<ButtonRelease-1>', set_moving_false)

canvas.bind('<Button-3>', create_obj)

root.bind('<Control-s>', save)

root.mainloop()