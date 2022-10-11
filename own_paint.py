from tkinter import *
from tkinter.colorchooser import askcolor
import math
import json
import sys

from shapes.line import Line
from shapes.circle import Circle
from shapes.rectangle import Rectangle
from shapes.triangle import Triangle
from shapes.point import Point


def only_numbers_between_0_and_1000(char, whole_number):
    digit = char.isdigit()
    if not digit:
        return digit
    return 1000 > int(whole_number) >= 0

def select_shape(canvas, shape, shape_type):
    tags = canvas.gettags(shape)

    if tags[0] != 'line':
        canvas.itemconfig(shape, outline='red', width=5)
    else:
        canvas.itemconfig(shape, fill='red')

def unselect_shape(canvas, shape, shape_type, color):
    tags = canvas.gettags(shape)

    if tags[0] != 'line':
        canvas.itemconfig(shape, outline='')
    else:
        canvas.itemconfig(shape, fill=color)


def find_closest_point(main_point_x, main_point_y, array_of_points):
    local_max = sys.maxsize
    index_min = 0
    for index in range(0, int(len(array_of_points)), 2):
        print('twoj index', index)
        x = array_of_points[index]
        y = array_of_points[index + 1]
        distance_between = math.sqrt(math.pow(x - main_point_x, 2) + math.pow(y - main_point_y, 2))
        if distance_between <= local_max:
            local_max = distance_between
            index_min = index
    if len(array_of_points) == 0:
        return array_of_points[index_min]

    return (array_of_points[index_min], array_of_points[index_min + 1], index_min)


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.choice2 = None
        self.selected = None
        self.preview = None
        self.first = False
        self.second = False
        self.previews = []
        self.doing = None
        self.root = Tk()
        self.shapes = []
        self.shape_line = Button(self.root, text='line', command=self.use_pen)
        self.shape_line.grid(row=0, column=0)

        self.shape_circle = Button(self.root, text='circle', command=self.use_brush)
        self.shape_circle.grid(row=0, column=1)

        self.shape_triangle = Button(self.root, text='triangle', command=self.use_eraser)
        self.shape_triangle.grid(row=0, column=2)

        self.shape_rectangle = Button(self.root, text='rectangle', command=self.rectangle_shape)
        self.shape_rectangle.grid(row=0, column=3)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=4)

        self.moving = Button(self.root, text='move', command=self.move)
        self.moving.grid(row=0, column=5)

        self.scaling = Button(self.root, text='scale', command=self.scale)
        self.scaling.grid(row=0, column=6)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=7)

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, rowspan=6, column=0, columnspan=10)

        self.label = Label(self.root, text="First x")
        self.label.grid(row=0, rowspan=2,  column=11)

        validation = self.root.register(only_numbers_between_0_and_1000)

        self.inputing_first_x = Entry(self.root, validate="all", validatecommand=(validation, '%S', '%P'))
        self.inputing_first_x.grid(row=1, column=11)

        self.second_label = Label(self.root, text="First y")
        self.second_label.grid(row=0, rowspan=2,  column=12)

        self.inputing_first_y = Entry(self.root, validate="key", validatecommand=(validation, '%S', '%P'))
        self.inputing_first_y.grid(row=1, column=12)

        self.label = Label(self.root, text="Second x")
        self.label.grid(row=1, rowspan=2,  column=11)

        self.inputing_second_x = Entry(self.root, validate="key", validatecommand=(validation, '%S', '%P'))
        self.inputing_second_x.grid(row=2, column=11)

        self.second_label = Label(self.root, text="Second y")
        self.second_label.grid(row=1, rowspan=2, column=12)

        self.inputing_second_y = Entry(self.root, validate="key", validatecommand=(validation, '%S', '%P'))
        self.inputing_second_y.grid(row=2, column=12)

        self.saving = Button(self.root, text='Save', command=self.create_shape)
        self.saving.grid(row=2, column=13)

        self.c.selected = None
        self.c.dot = None

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.choice = None
                           # width=self.line_width, fill=paint_color, capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.shape_line
        self.c.bind('<Return>', self.asdf)

        self.c.bind('<Button-1>', self.paint)
        # self.c.bind('<Button-1>', self.on_click)
        self.c.bind('<Button-3>', self.stop_preview)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.c.bind('<Motion>', self.motion)
        self.c.bind('<B1-Motion>', self.on_drag)
        self.c.bind('<Control-s>', self.save)

    def use_pen(self):
        self.activate_button(self.shape_line)
        self.choice = 'line'
        self.choice2 = Line()
        self.stop_preview()

    def use_brush(self):
        self.activate_button(self.shape_circle)
        self.choice = 'circle'
        self.choice2 = Circle()
        self.stop_preview()


    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]
        self.stop_preview()


    def use_eraser(self):
        self.activate_button(self.shape_triangle)
        self.choice = 'triangle'
        self.choice2 = Triangle()
        self.stop_preview()

    def rectangle_shape(self):
        self.activate_button(self.shape_rectangle)
        self.choice = 'rectangle'
        self.choice2 = Rectangle()
        self.stop_preview()

    def activate_button(self, some_button):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button

    def move(self):
        self.activate_button(self.moving)
        self.choice = 'move'
        self.stop_preview()

    def scale(self):
        self.activate_button(self.scaling)
        self.choice = 'scale'
        self.stop_preview()

    def create_shape(self):
        # print(self.inputing)
        # print(self.second_inputing)
        first_point = Point(int(self.inputing_first_x.get()), int(self.inputing_first_y.get()))
        second_point = Point(int(self.inputing_second_x.get()), int(self.inputing_second_y.get()))
        if self.choice2:
            self.choice2.create(self.c, first_point.x, first_point.y, second_point.x, second_point.y,
                                 fill=self.color, width=self.line_width)

    def paint(self, event):
        self.line_width = self.choose_size_button.get()

        if self.choice in ['line', 'circle', 'rectangle']:
            if not self.first:
                self.first_x = event.x
                self.first_y = event.y
                self.first = True
            else:
                self.shapes.append(self.choice2.create(self.c, self.first_x, self.first_y, event.x, event.y,
                                    fill=self.color, width=self.line_width, tags=self.choice2.type))
                self.first = False
        if self.choice == 'triangle':
            if not self.first:
                self.first_x = event.x
                self.first_y = event.y
                self.first = True
            elif not self.second:
                self.second_x = event.x
                self.second_y = event.y
                self.doing = self.c.create_line(self.first_x, self.first_y, self.second_x, self.second_y,
                                                      width=self.line_width, fill=self.color,
                                                      capstyle=ROUND, smooth=TRUE, splinesteps=36)
                self.second = True
            else:
                self.c.create_polygon(self.first_x, self.first_y, self.second_x, self.second_y, event.x, event.y,
                                      fill=self.color, tags=self.choice2.type)
                self.second = False
                self.first = False

        if self.choice in ['move', 'scale']:
            self.on_click(event)
        else:
            self.selected = None
        self.c.focus_set()

    def on_click(self, event):
        self.selected = self.c.find_overlapping(event.x - 10, event.y - 10, event.x + 10, event.y + 10)
        print('zaznaczone', self.selected)
        if self.selected:
            if self.c.selected:
                unselect_shape(self.c, self.c.selected, self.choice2, self.color)
                self.c.selected = None
            self.c.selected = self.selected[-1]
            select_shape(self.c, self.c.selected, self.choice2)

            # if self.c.selected
            self.c.startxy = (event.x, event.y)
        else:
            if self.c.selected:
                unselect_shape(self.c, self.c.selected, self.choice2, self.color)
                self.c.selected = None

    def on_drag(self, event):
        if self.choice == 'move':
            if self.c.selected:
                dx, dy = event.x - self.c.startxy[0], event.y - self.c.startxy[1]
                self.c.move(self.c.selected, dx, dy)
                self.c.startxy = (event.x, event.y)
        if self.choice == 'scale':
            if self.c.selected:
                coords = self.c.coords(self.c.selected)
                tags = self.c.gettags('dot')
                print(self.c.coords(tags))
                closest = self.c.find_closest(event.x, event.y)
                print('twoj punkt', tags)
                print('najblizej', closest)
                self.c.coords(self.selected, event.x, event.y, coords[0], coords[1])

    def motion(self, event):
        if self.c.dot:
            self.c.delete(self.c.dot)
        if self.previews != []:
            for preview in self.previews:
                self.c.delete(preview)
            self.previews.clear()
        if self.choice == 'triangle':
            if not self.first:
                if self.doing:
                    self.c.delete(self.doing)
            if self.first:
                self.previews.append(Line().create(self.c, self.first_x, self.first_y, event.x, event.y,
                                    fill=self.color))
            if self.second:
                self.previews.append(Line().create(self.c, self.second_x, self.second_y, event.x, event.y,
                                             fill=self.color))
        elif self.choice == 'scale':
            if self.c.selected:
                coords = self.c.coords(self.c.selected)
                print("koordy", coords)
                point = find_closest_point(event.x, event.y, coords)
                print("punkt", point)
        else:
            if self.first:
                self.previews.append(self.choice2.create(self.c, self.first_x, self.first_y, event.x, event.y,
                                                         fill=self.color))

        self.c.focus_set()

    def stop_preview(self):
        for preview in self.previews:
            self.c.delete(preview)
        self.c.delete(self.doing)
        self.first = False
        self.second = False

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def asdf(self, event):
        # print("di[a")
        self.c.move(self.preview, 10, 0)   #  for x += 10

    def save(self, event, obj_lst=None):
        with open('untitled.canvas', 'w') as file:
            obj_dict = {f'{obj.type} {id}': (obj.x, obj.y) for id, obj in enumerate(obj_lst)}
            json.dump(obj_dict, file)
if __name__ == '__main__':
    Paint()
