from tkinter import *
from tkinter.colorchooser import askcolor
import math
import json
import sys

from shapes.line import Line
from shapes.circle import Circle
from shapes.rectangle import Rectangle
from shapes.triangle import Triangle
def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

def find_closest_point(main_point_x, main_point_y, array_of_points):
    local_max = sys.maxsize
    index_min = 0
    for index in range(0, len(array_of_points), 2):
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
        self.pen_button = Button(self.root, text='line', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='circle', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.eraser_button = Button(self.root, text='triangle', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=2)

        self.rectangle = Button(self.root, text='rectangle', command=self.rectangle_shape)
        self.rectangle.grid(row=0, column=3)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=4)

        self.moving = Button(self.root, text='move', command=self.move)
        self.moving.grid(row=0, column=5)

        self.scaling = Button(self.root, text='scale', command=self.scale)
        self.scaling.grid(row=0, column=6)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=7)

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, rowspan=2, column=0, columnspan=10)

        self.label = Label(self.root, text="First x")
        self.label.grid(row=0, rowspan=2,  column=11)

        self.inputing = Entry(self.root)
        self.inputing.grid(row=1, column=11)

        self.second_label = Label(self.root, text="First y")
        self.second_label.grid(row=0, rowspan=2,  column=13)

        self.second_inputing = Entry(self.root)
        self.second_inputing.grid(row=1, column=13)

        self.saving = Button(self.root, text='Save')
        self.saving.grid(row=1, column=14)

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
        self.active_button = self.pen_button
        self.c.bind('<Return>', self.asdf)

        self.c.bind('<Button-1>', self.paint)
        # self.c.bind('<Button-1>', self.on_click)
        self.c.bind('<Button-3>', self.stop_preview)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.c.bind('<Motion>', self.motion)
        self.c.bind('<B1-Motion>', self.on_drag)
        self.c.bind('<Control-s>', self.save)

    def use_pen(self):
        self.activate_button(self.pen_button)
        self.choice = 'line'
        self.choice2 = Line()
        self.stop_preview()

    def use_brush(self):
        self.activate_button(self.brush_button)
        self.choice = 'circle'
        self.choice2 = Circle()
        self.stop_preview()


    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]
        self.stop_preview()


    def use_eraser(self):
        self.activate_button(self.eraser_button)
        self.choice = 'triangle'
        self.choice2 = Triangle()
        self.stop_preview()

    def rectangle_shape(self):
        self.activate_button(self.rectangle)
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

    def paint(self, event):

        self.line_width = self.choose_size_button.get()
        paint_color = self.color
        self.click_x = event.x
        self.click_y = event.y
        if self.choice in ['line', 'circle', 'rectangle']:
            if not self.first:
                self.first_x = event.x
                self.first_y = event.y
                self.first = True
            else:
                self.shapes.append(self.choice2.create(self.c, self.first_x, self.first_y, event.x, event.y,
                                    fill=paint_color, width=self.line_width))
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
                                                      width=self.line_width, fill=paint_color,
                                                      capstyle=ROUND, smooth=TRUE, splinesteps=36)
                self.second = True
            else:
                self.c.create_polygon(self.first_x, self.first_y, self.second_x, self.second_y, event.x, event.y,
                                      fill=paint_color)
                self.second = False
                self.first = False

        # print(self.choice)
        if self.choice in ['move', 'scale']:
            self.on_click(event)
        else:
            self.selected = None
        self.c.focus_set()

    def on_click(self, event):
        self.selected = self.c.find_overlapping(event.x - 10, event.y - 10, event.x + 10, event.y + 10)
        if self.selected:
            self.c.selected = self.selected[-1]  # select the top-most item
            self.c.startxy = (event.x, event.y)
        else:
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
                print('ilosc', len(coords))
                print(coords)
                coords_of_point = self.c.coords(self.c.dot)
                x, c, ll = find_closest_point(coords_of_point[0], coords_of_point[1], coords)
                number_of_coords = [a for a in range(int(len(coords) / 2))]
                index_of_closest_point = number_of_coords.index(ll)
                del number_of_coords[index_of_closest_point]
                array_for_scaling = []
                for point in number_of_coords:
                        array_for_scaling.append(coords[point])
                        array_for_scaling.append(coords[point + 1])
                array_for_scaling.append(event.x)
                array_for_scaling.append(event.y)
                self.c.coords(self.selected, array_for_scaling)
                # self.c.delete(self.dot)

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
                point = find_closest_point(event.x, event.y, coords)
                self.c.dot = self.c.create_oval(point[0], point[1], point[0]+5, point[1]+5, fill='#ff0000')
                # breakpoint()
                # coords = self.c.coords(self.c.selected)
                # event.x event.y
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
