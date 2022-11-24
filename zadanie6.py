import math
from tkinter import *
from tkinter import ttk
from scipy.spatial import distance

ALL_STEPS = 2000

class Menu:
    root = Tk()
    w = Canvas(root, width=700, height=700, background='#ffffff')

    mode = 'none'
    mouse_move_selected_object = None

    control_points = []

    def __init__(self):
        maincolor = '#4169E1'

        self.root.configure(bg=maincolor)
        self.root.title('Bezier')
        self.root.minsize(width=700, height=600)
        self.action_buttons = []
        create_point_text = Button(self.root, width=10, command=self.add_point_text, text='Create', height=2)
        create_point_text.grid(row=0, column=0, sticky='N')
        self.action_buttons.append(create_point_text)

        edit_point_text = Button(self.root, width=10, command=self.edit_point_text, text='Edit', height=2)
        edit_point_text.grid(row=0, column=1, sticky='N')
        self.action_buttons.append(edit_point_text)

        separator = ttk.Separator(self.root, orient='vertical')
        separator.grid(row=0, column=2, rowspan=4, ipady=100, sticky='NE')

        create_point_mouse = Button(self.root, width=10, command=self.add_point_mouse, text='Create', height=2)
        create_point_mouse.grid(row=0, column=3, sticky='N')
        self.action_buttons.append(create_point_mouse)

        edit_point_mouse = Button(self.root, width=10, command=self.move_mouse, text='Edit', height=2)
        edit_point_mouse.grid(row=0, column=4, sticky='N')
        self.action_buttons.append(edit_point_mouse)

        reset_button = Button(self.root, width=10, bg='red', command=self.reset_canvas, text='Reset', height=2)
        reset_button.grid(row=1, column=4, sticky='N')

        info_about_clicked = Label(self.root, width=15, bg=maincolor, text='Element: ...')
        info_about_clicked.grid(row=1, column=3, sticky='N')
        self.info_about_clicked = info_about_clicked

        label_x = Label(self.root, bg=maincolor, width=15, text='X')
        label_x.grid(row=1, column=0, sticky='N')

        input_x = Entry(self.root, width=15)
        input_x.grid(row=2, column=0, sticky='N')

        label_y = Label(self.root, width=15, bg=maincolor, text='Y')
        label_y.grid(row=1, column=1, sticky='N')

        input_y = Entry(self.root, width=15)
        input_y.grid(row=2, column=1, sticky='N')
        self.input_x = input_x
        self.input_y = input_y

        self.set_input(input_x, 0)
        self.set_input(input_y, 0)


        submit = Button(self.root, width=10, text="Submit", command=self.manage_points)
        submit.grid(row=3, column=0, columnspan=2, sticky='N')

        self.w.grid(row=4, column=0, columnspan=5, sticky='NEWS')

        self.root.mainloop()

    def set_info_about_clicked(self):
        elem = self.last_clicked if self.last_clicked is not None else '...'
        self.info_about_clicked.configure(text=f'Element: {elem}')

    def reset_canvas(self):
        self.w.delete('all')
        self.control_points.clear()
        self.last_clicked = None
        self.set_info_about_clicked()

    def set_input(self, tkinter_input, data):
        tkinter_input.delete(0, END)
        tkinter_input.insert(0, data)

    def set_color_of_button(self, mode):
        for index, button in enumerate(self.action_buttons):
            if index == mode:
                button.configure(bg='white')
            else:
                button.configure(bg='grey')

    def add_point_text(self):
        self.mode = 0
        self.set_color_of_button(self.mode)

    def edit_point_text(self):
        self.mode = 1
        self.set_color_of_button(self.mode)

    def manage_points(self):
        point = (self.input_x.get(), self.input_y.get())

        if self.mode == 0:
            self.add_control_point(point[0], point[1])
        elif self.mode == 1:
            self.control_points[self.last_clicked] = (int(point[0]), int(point[1]))
            self.draw_bezier_curve()

    def add_point_mouse(self):
        self.mode = 2
        self.set_color_of_button(self.mode)
        self.w.unbind("<B1-Motion>")
        self.w.unbind('<ButtonRelease-1>')
        self.w.bind("<Button-1>", self.add_point_clicked)


    def edit_clicked_point(self, x, y):
        self.control_points[self.mouse_move_selected_object] = (int(x), int(y))
        self.draw_bezier_curve()

    def add_point_clicked(self, event):
        if self.mode == 2:
            self.add_control_point(event.x, event.y)

    def add_control_point(self, x, y):
        self.control_points.append((int(x), int(y)))
        self.last_clicked = len(self.control_points) - 1
        self.set_info_about_clicked()
        self.draw_bezier_curve()

    def draw_bezier_curve(self):
        self.w.delete('all')

        for index, point in enumerate(self.control_points):
            self.w.create_oval(point[0], point[1], point[0] + 5, point[1] + 5, fill='black')
            self.w.create_text(point[0]-3, point[1]-3, text=index)


        bezier_points = bezier_curve_points(ALL_STEPS, self.control_points)

        current_point = self.control_points[0]
        for point in bezier_points:
            self.w.create_line(point[0], point[1], current_point[0], current_point[1], fill='blue')
            current_point = point



    def move_mouse(self):
        self.mode = 3
        self.set_color_of_button(self.mode)
        self.w.unbind("<B1-Motion>")
        self.w.unbind('<ButtonRelease-1>')
        self.w.unbind("<Button-1>")

        self.w.bind("<B1-Motion>", self.mouse_held)
        self.w.bind('<ButtonRelease-1>', self.mouse_released)

    def mouse_held(self, event):
        if self.mode == 3:
            self.set_input(self.input_x, event.x)
            self.set_input(self.input_y, event.y)
            self.set_info_about_clicked()
            if self.mouse_move_selected_object is None:
                self.mouse_move_selected_object = self.get_closest_point(event.x, event.y)
                self.last_clicked = self.mouse_move_selected_object
            else:
                self.control_points[self.mouse_move_selected_object] = (event.x, event.y)
                self.last_clicked = self.mouse_move_selected_object
                self.draw_bezier_curve()

    def mouse_released(self, event):
        self.mouse_move_selected_object = None

    def closest_point(self, point, points):
        closest_index = distance.cdist([point], points).argmin()
        return closest_index

    def get_closest_point(self, clicked_point_x, clicked_point_y):
        # points = []
        # for index, value in enumerate(self.control_points):
        #     points.append({'id': index, 'x': value[0], 'y': value[1]})

        # point_coordinates = []
        # for value in points:
        # for index, value in enumerate(self.control_points):
        #     point_coordinates.append((value[0], value[1]))
        closest_point_index = self.closest_point((clicked_point_x, clicked_point_y), self.control_points)
        print("index", closest_point_index)
        return closest_point_index

# calculations
def fact(number):
    k = 1
    for i in range(1, number):
        k *= i
    return k
def binomial(i, n):
    return fact(n) / float(fact(i) * fact(n - i))


def bezier(t, points):
    n = len(points) - 1
    x = y = 0
    for i, pos in enumerate(points):
        bernstein = binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))
        x += pos[0] * bernstein
        # print(x)
        y += pos[1] * bernstein

    return x, y


def bezier_curve_points(n, points):
    new_points = []
    for i in range(n):
        t = i / float(n - 1)
        new_points.append(bezier(t, points))
    return new_points


Menu()
