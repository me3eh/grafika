from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog as fd
import math
import json
import sys

from shapes.line import Line
from shapes.circle import Circle
from shapes.rectangle import Rectangle
from shapes.triangle import Triangle
from shapes.point import Point

def set_text_in_entry(entry, text):
    entry.delete(0, END)
    entry.insert(0, text)
    return


def only_numbers_between_0_and_1000(char, whole_number):
    digit = char.isdigit()
    if not digit:
        return digit
    return 10000 > int(whole_number) >= 0


def select_shape(canvas, shape, shape_type):
    tags = canvas.gettags(shape)

    if tags[0] == 'line':
        canvas.itemconfig(shape, fill='red')
    else:
        canvas.itemconfig(shape, outline='red', width=5)

def deserialize(self, file_inside):
    for shape in self.shapes:
        self.c.delete(shape)
    self.shapes.clear()

    array_full_of_shapes = eval(file_inside)
    print(array_full_of_shapes)

    for shape in array_full_of_shapes:
        type_of_shape = list(shape.keys())[0]
        shape_object = eval(f"{type_of_shape.capitalize()}()")
        self.shapes.append(shape_object.create(self.c, list(list(shape.values())[0])))

def serialize(self):
    shapes_in_json = []
    for f in self.shapes:
        shapes_in_json.append({ self.c.gettags(f)[0]: self.c.coords(f)})
    print(shapes_in_json)
    return shapes_in_json

def unselect_shape(canvas, shape, shape_type, color):
    tags = canvas.gettags(shape)

    if tags[0] != 'line':
        canvas.itemconfig(shape, outline='black')
    else:
        canvas.itemconfig(shape, fill=color)


def find_closest_point(main_point_x, main_point_y, array_of_points):
    if len(array_of_points) == 0:
        return None

    local_max = sys.maxsize
    index_min = 0

    for index in range(0, int(len(array_of_points)), 2):
        x = array_of_points[index]
        y = array_of_points[index + 1]
        distance_between = math.sqrt(math.pow(x - main_point_x, 2) + math.pow(y - main_point_y, 2))
        if distance_between < local_max:
            local_max = distance_between
            index_min = index

    return index_min


class Paint(object):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.choice2 = None
        self.selected = None
        self.preview = None
        self.first_clicked_point = None
        self.second_clicked_point = None
        self.second = False
        self.previews = []
        self.doing = None
        self.root = Tk()
        self.shapes = []
        self.shape_line = Button(self.root, text='line', command=self.line_shape)
        self.shape_line.grid(row=0, column=0)

        self.shape_circle = Button(self.root, text='circle', command=self.circle_shape)
        self.shape_circle.grid(row=0, column=1)

        self.shape_triangle = Button(self.root, text='triangle', command=self.triangle_shape)
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
        self.label.grid(row=0, rowspan=2, column=11)

        validation = self.root.register(only_numbers_between_0_and_1000)

        self.inputing_first_x = Entry(self.root, validate="all", validatecommand=(validation, '%S', '%P'))
        self.inputing_first_x.insert(END, 0)
        self.inputing_first_x.grid(row=1, column=11)

        self.second_label = Label(self.root, text="First y")
        self.second_label.grid(row=0, rowspan=2, column=12)

        self.inputing_first_y = Entry(self.root, validate="key", validatecommand=(validation, '%S', '%P'))
        self.inputing_first_y.insert(END, 0)
        self.inputing_first_y.grid(row=1, column=12)

        self.label = Label(self.root, text="Second x")
        self.label.grid(row=1, rowspan=2, column=11)

        self.inputing_second_x = Entry(self.root, validate="key", validatecommand=(validation, '%S', '%P'))
        self.inputing_second_x.insert(END, 0)
        self.inputing_second_x.grid(row=2, column=11)

        self.second_label = Label(self.root, text="Second y")
        self.second_label.grid(row=1, rowspan=2, column=12)

        self.inputing_second_y = Entry(self.root, validate="key", validatecommand=(validation, '%S', '%P'))
        self.inputing_second_y.insert(END, 0)
        self.inputing_second_y.grid(row=2, column=12)

        self.label = Label(self.root, text="Third x")
        self.label.grid(row=2, rowspan=2, column=11)

        self.inputing_third_x = Entry(self.root, validate="key", validatecommand=(validation, '%S', '%P'))
        self.inputing_third_x.insert(END, 0)
        self.inputing_third_x.grid(row=3, column=11)

        self.second_label = Label(self.root, text="Third y")
        self.second_label.grid(row=2, rowspan=2, column=12)

        self.inputing_third_y = Entry(self.root, validate="key", validatecommand=(validation, '%S', '%P'))
        self.inputing_third_y.insert(END, 0)
        self.inputing_third_y.grid(row=3, column=12)

        self.saving = Button(self.root, text='Save', command=self.create_shape)
        self.saving.grid(row=2, column=13)

        self.opening_file = Button(self.root, text='Open file', command=self.open_file)
        self.opening_file.grid(row=4, column=11, columnspan=2)

        self.saving_file = Button(self.root, text='Save file', command=self.save_file)
        self.saving_file.grid(row=4, column=12)

        self.c.selected = None
        self.c.dot = None

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.choice = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.active_button = self.shape_line
        self.c.bind('<Return>', self.asdf)

        self.c.bind('<Button-1>', self.paint)
        self.c.bind('<Button-3>', self.stop_preview)
        self.c.bind('<Motion>', self.motion)
        self.c.bind('<B1-Motion>', self.on_drag)

    def line_shape(self):
        self.activate_button(self.shape_line)
        self.choice = 'line'
        self.choice2 = Line()
        self.stop_preview()

    def circle_shape(self):
        self.activate_button(self.shape_circle)
        self.choice = 'circle'
        self.choice2 = Circle()
        self.stop_preview()

    def choose_color(self):
        self.color = askcolor(color=self.color)[1]
        self.stop_preview()

    def triangle_shape(self):
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
        if self.choice == 'move':
            if self.c.selected:
                self.c.move(self.c.selected, int(self.inputing_first_x.get()), int(self.inputing_first_y.get()))
        elif self.choice == 'scale':
            if self.c.selected:
                self.c.move(self.c.selected, int(self.inputing_first_x.get()), int(self.inputing_first_y.get()))
                sh = []
                tag = self.c.gettags(self.c.selected)[0]
                sh.append(self.inputing_first_x.get())
                sh.append(self.inputing_first_y.get())
                sh.append(self.inputing_second_x.get())
                sh.append(self.inputing_second_y.get())
                if tag == 'triangle':
                    sh.append(self.inputing_third_x.get())
                    sh.append(self.inputing_third_y.get())
                self.c.coords(self.c.selected, sh)
        else:
            if self.choice2:
                first_point = Point(int(self.inputing_first_x.get()), int(self.inputing_first_y.get()))
                second_point = Point(int(self.inputing_second_x.get()), int(self.inputing_second_y.get()))
                coordinats = first_point.values() + second_point.values()
                if self.choice2.type == 'triangle':
                    third_point = Point(int(self.inputing_third_x.get()), int(self.inputing_third_y.get()))
                    coordinats.append(third_point.x)
                    coordinats.append(third_point.y)
                self.shapes.append(self.choice2.create(self.c, coordinats, fill=self.color, width=self.line_width))

    def open_file(self):
        print(serialize(self))

        filename = fd.askopenfilename(filetypes=[("Plik tekstowy", "*.canvas")])
        if filename:
            with open(filename, "r", -1, "utf-8") as file:
                deserialize(self, file.read())
                # file.read(serialize(self))


    def save_file(self):
        filename = fd.asksaveasfilename(filetypes=[("Plik tekstowy", "*.canvas")], defaultextension="*.canvas")
        print(serialize(self))
        if filename:
            with open(filename, "w", -1, "utf-8") as file:
                file.write(repr(serialize(self)))

    def paint(self, event):
        self.line_width = self.choose_size_button.get()

        if self.choice in ['line', 'circle', 'rectangle']:
            if not self.first_clicked_point:
                self.first_clicked_point = Point(event.x, event.y)
            else:
                self.shapes.append(self.choice2.create(self.c, [self.first_clicked_point.x, self.first_clicked_point.y,
                                                       event.x, event.y], fill=self.color, width=self.line_width))
                self.first_clicked_point = None
        if self.choice == 'triangle':
            if not self.first_clicked_point:
                self.first_clicked_point = Point(event.x, event.y)
            elif not self.second_clicked_point:
                self.second_clicked_point = Point(event.x, event.y)
                self.doing = self.c.create_line(self.first_clicked_point.x, self.first_clicked_point.y,
                                                self.second_clicked_point.x, self.second_clicked_point.y,
                                                width=self.line_width, fill=self.color, capstyle=ROUND, smooth=TRUE,
                                                splinesteps=36)
            else:
                self.shapes.append(self.c.create_polygon(self.first_clicked_point.x, self.first_clicked_point.y,
                                                         self.second_clicked_point.x, self.second_clicked_point.y,
                                                         event.x, event.y, tags='triangle', fill=self.color))
                self.second_clicked_point = None
                self.first_clicked_point = None

        if self.choice in ['move', 'scale']:
            self.on_click(event)
        else:
            self.selected = None
        self.c.focus_set()

    def on_click(self, event):
        self.selected = self.c.find_overlapping(event.x - 10, event.y - 10, event.x + 10, event.y + 10)
        if self.selected:
            if self.c.selected:
                unselect_shape(self.c, self.c.selected, self.choice2, self.color)
                self.c.selected = None
            self.c.selected = self.selected[-1]
            select_shape(self.c, self.c.selected, self.choice2)

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
                point = find_closest_point(event.x, event.y, coords)
                if point != None:
                    other_points_than_closest = [a for a in range(int(len(coords) / 2))]
                    other_points_than_closest.pop(int(point / 2))
                    shape = []
                    for points in other_points_than_closest:
                        shape.append(coords[points * 2])
                        shape.append(coords[points * 2 + 1])
                    shape.append(event.x)
                    shape.append(event.y)
                    self.c.coords(self.c.selected, *shape)

    def motion(self, event):
        if self.c.dot:
            self.c.delete(self.c.dot)
        if self.previews != []:
            for preview in self.previews:
                self.c.delete(preview)
            self.previews.clear()
        if self.choice == 'triangle':
            if not self.first_clicked_point:
                if self.doing:
                    self.c.delete(self.doing)
            if self.first_clicked_point:
                self.previews.append(Line().create(self.c, self.first_clicked_point.x,
                                                   self.first_clicked_point.y, event.x, event.y, fill=self.color))
            if self.second_clicked_point:
                self.previews.append(Line().create(self.c, self.second_clicked_point.x, self.second_clicked_point.y,
                                                   event.x, event.y, fill=self.color))
        # elif self.choice == 'move':
            # print("ruszanko")
            # if self.c.selected:
            #     coords = self.c.coords(self.c.selected)
            #     print("less go")
            #     print("koordynaty", coords)
            #     print("probka", coords[0])
            #     print("probka w intcie", int(coords[0]))
            #     set_text_in_entry(self.inputing_first_x, int(coords[0]))
            #     set_text_in_entry(self.inputing_first_y, int(coords[1]))
            #     set_text_in_entry(self.inputing_second_x, int(coords[2]))
            #     set_text_in_entry(self.inputing_second_y, int(coords[3]))
            #     if len(coords) == 6:
            #         set_text_in_entry(self.inputing_third_x, int(coords[4]))
            #         set_text_in_entry(self.inputing_third_y, int(coords[5]))
        else:
            if self.first_clicked_point:
                self.previews.append(self.choice2.create(self.c, [self.first_clicked_point.x, self.first_clicked_point.y,
                                                         event.x, event.y], fill=self.color))

        self.c.focus_set()

    def stop_preview(self):
        for preview in self.previews:
            self.c.delete(preview)
        self.c.delete(self.doing)
        self.first_clicked_point = None
        self.second_clicked_point = None

    def asdf(self, event):
        self.c.move(self.preview, 10, 0)

if __name__ == '__main__':
    Paint()
