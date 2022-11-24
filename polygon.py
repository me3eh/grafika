import tkinter as tk
import math as math
from scipy.spatial import distance
import numpy as np

class Paint(object):
    DEFAULT_PEN_SIZE = 5.0

    def __init__(self):
        self.width = 600
        self.height = 600
        self.choice2 = None
        self.polygons = []
        self.shapes = []
        self.clicks = []
        self.ovals = []
        self.vertices_of_polygon = {}
        self.last_clicked_x = self.last_clicked_y = self.defined_point = None
        self.active_button = None
        # self.selected = None
        # self.preview = None
        # self.first_clicked_point = None
        # self.second_clicked_point = None
        # self.previews = []
        # self.doing = None
        self.root = tk.Tk()
        self.creating_button = tk.Button(self.root, text='create polygons', command=self.creating_points_for_polygon)
        self.creating_button.grid(row=0, column=0)

        self.selecting_button = tk.Button(self.root, text='select shape', command=self.selecting_shape)
        self.selecting_button.grid(row=0, column=1)

        self.translating_button = tk.Button(self.root, text='translate', command=self.translating_polygons)
        self.translating_button.grid(row=0, column=2)

        self.scaling_button = tk.Button(self.root, text='scale', command=self.scaling_polygons, width=12)
        self.scaling_button.grid(row=0, column=3)

        self.rotating_button = tk.Button(self.root, text='rotate', command=self.rotate, width=12)
        self.rotating_button.grid(row=0, column=4)

        self.defining_point_button = tk.Button(self.root, text='define point', command=self.define_point)
        self.defining_point_button.grid(row=0, column=5)

        self.first_entry = tk.Entry(self.root, width=12)
        self.first_entry.grid(row=1, column=3)

        self.second_entry = tk.Entry(self.root, width=12)
        self.second_entry.grid(row=1, column=4)

        self.submit = tk.Button(self.root, width=12, text='Submit')
        self.submit.grid(row=1, column=5)

        self.canvas = tk.Canvas(self.root, bg='white', width=self.width, height=self.height)
        self.canvas.grid(row=2, rowspan=6, column=0, columnspan=10)
        # self.canvas.bind('<Button-1>', self.click)

        self.root.mainloop()

    def reset_clicked(self):
        self.last_clicked_x = None
        self.last_clicked_y = None

    def create_point_with_keyboard(self, event):
        first_input = int(self.first_entry.get())
        second_input = int(self.second_entry.get())
        self.create_point([first_input, second_input])

    def translate_point_with_keyboard(self, event):
        first_input = int(self.first_entry.get())
        second_input = int(self.second_entry.get())
        self.translate_polygon(first_input, second_input)

    def scale_polygon_with_keyboard(self, event):
        first_input = float(self.first_entry.get())
        second_input = float(self.second_entry.get())
        self.scale_polygon(first_input, second_input)

    def rotate_polygon_with_keyboard(self, event):
        first_input = float(self.first_entry.get())
        angle = first_input * np.pi / 180
        self.rotate_polygon(angle)

    def set_point_for_rotating_and_scaling_with_keyboard(self, event):
        first_input = float(self.first_entry.get())
        second_input = float(self.second_entry.get())
        self.set_point_for_rotating_and_scaling([first_input, second_input])

    def creating_points_for_polygon(self):
        self.activate_button(self.creating_button)
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<B1-Motion>')
        self.submit.unbind('<Button-1>')
        self.submit.bind('<Button-1>', self.create_point_with_keyboard)
        self.submit.bind('<Button-3>', self.create_polygon)

        self.canvas.bind('<Button-1>', self.create_point_with_mouse)
        self.canvas.bind('<Button-3>', self.create_polygon)

    def selecting_shape(self):
        self.submit.unbind('<Button-1>')

        self.reset_all_ovals()
        self.activate_button(self.selecting_button)

        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<B1-Motion>')
        self.submit.unbind('<Button-1>')

        self.canvas.bind('<Button-1>', self.selecting_shape_by_click)

    def translating_polygons(self):
        self.reset_all_ovals()
        self.activate_button(self.translating_button)

        self.reset_clicked()
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')
        self.submit.unbind('<Button-1>')
        self.canvas.bind('<B1-Motion>', self.translating)
        self.submit.bind('<Button-1>', self.translate_point_with_keyboard)

        # self.canvas.bind('<Button-3>', self.create_polygon)

    def scaling_polygons(self):
        self.reset_all_ovals()
        self.activate_button(self.scaling_button)

        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<B1-Motion>')
        self.submit.unbind('<Button-1>')
        self.canvas.bind('<B1-Motion>', self.scaling)
        self.submit.bind('<Button-1>', self.scale_polygon_with_keyboard)

    def define_point(self):
        self.reset_all_ovals()
        self.activate_button(self.defining_point_button)

        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<B1-Motion>')
        self.submit.unbind('<Button-1>')

        self.canvas.bind('<Button-1>', self.set_point_for_rotating_and_scaling_with_mouse)
        self.submit.bind('<Button-1>', self.set_point_for_rotating_and_scaling_with_keyboard)

    def rotate(self):
        self.reset_all_ovals()
        self.activate_button(self.rotating_button)

        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.bind('<B1-Motion>', self.rotating)
        self.submit.bind('<Button-1>', self.rotate_polygon_with_keyboard)

    def create_point_with_mouse(self, event):
        self.create_point([event.x, event.y])

    def create_point(self, point):
        self.clicks.append((point[0] - 1, point[1] - 1))
        self.ovals.append(self.canvas.create_oval(point[0] - 2, point[1] - 2, point[0] + 2, point[1] + 2))
        # pt = (event.x - self.width // 2, self.height // 2 - event.y)
        # self.canvas.create_text(event.x - 4, event.y - 10, fill="black", font="Times 10",
        #                         text="(" + str(pt[0]) + ", " + str(pt[1]) + ")")


    def create_polygon(self, event):
        self.polygons.append(self.canvas.create_polygon(self.clicks, outline="black", fill="", tags=['polygon_2']))
        self.vertices_of_polygon[self.polygons[-1]] = self.clicks
        self.clicks = []
        self.reset_all_ovals()

    def selecting_shape_by_click(self, event):
        closest = self.canvas.find_closest(event.x, event.y)

        for object in self.canvas.find_withtag("polygon_2"):
                self.canvas.itemconfig(object, outline='black')

        if self.canvas.type(closest) == 'polygon':
            self.canvas.itemconfig(closest[0], outline='red')
            self.canvas.selected = closest[0]
        else:
            self.canvas.selected = None

    def translating(self, event):
        if self.last_clicked_x is None:
            self.last_clicked_x = event.x
            self.last_clicked_y = event.y
            return
        tx, ty = event.x - self.last_clicked_x, self.last_clicked_y - event.y
        self.translate_polygon(tx, ty)
        self.last_clicked_x = event.x
        self.last_clicked_y = event.y

    def rotating(self, event):
        defined_point_coords = self.canvas.coords(self.defined_point)
        polygon_vertix = self.vertices_of_polygon[self.canvas.selected][0]
        angle = self.get_angle(p1=(event.x, event.y),
                               p2=(int(defined_point_coords[0]), int(defined_point_coords[1])),
                               p3=(polygon_vertix[0], polygon_vertix[1]))
        self.rotate_polygon(angle)

    def scaling(self, event):
        mouse_coords = (event.x, event.y)
        defined_point_coords = self.canvas.coords(self.defined_point)
        polygon_vertix = self.vertices_of_polygon[self.canvas.selected][0]
        distance_between_mouse_and_defined = self.distance_between_two_points(mouse_coords, defined_point_coords)
        distance_between_polygon_and_defined = self.distance_between_two_points(polygon_vertix, defined_point_coords)

        if distance_between_polygon_and_defined[0] != 0.0 and distance_between_polygon_and_defined[1] != 0.0:
            sx = distance_between_mouse_and_defined[0] / distance_between_polygon_and_defined[0]
            sy = distance_between_mouse_and_defined[1] / distance_between_polygon_and_defined[1]
            self.scale_polygon(sx, sy)


    def translate_polygon(self, tx, ty):
        transation_matris = np.asarray([[1, 0, tx],
                            [0, 1, -ty, ],
                            [0, 0, 1]])

        new_vertices = []
        for polygon_vertices in self.vertices_of_polygon[self.canvas.selected]:
            new_vertices.append([polygon_vertices[0], polygon_vertices[1], 1])

        transposed_vertices = np.transpose(np.asarray(new_vertices))

        output_matrix = np.transpose(transation_matris.dot(transposed_vertices))

        new_vertices = []
        for vertix in output_matrix:
            new_vertices.append((vertix[0], vertix[1]))

        # self.clicks = new_vertices

        for i in self.vertices_of_polygon[self.canvas.selected]:
            self.canvas.delete(i)

        self.canvas.delete(self.canvas.selected)
        self.polygons.remove(self.canvas.selected)
        self.vertices_of_polygon.pop(self.canvas.selected)

        self.polygons.append(self.canvas.create_polygon(new_vertices, outline="black", fill="", tags=['polygon_2']))
        self.vertices_of_polygon[self.polygons[-1]] = new_vertices
        self.canvas.selected = self.polygons[-1]
        self.canvas.itemconfig(self.canvas.selected, outline='red')

    def rotate_polygon(self, theta):
        coords = self.canvas.coords(self.defined_point)
        xr = coords[0]
        yr = coords[1]

        rotation = np.asarray([[np.cos(theta), -np.sin(theta), xr * (1 - np.cos(theta)) + yr * np.sin(theta)],
                               [np.sin(theta), np.cos(theta), yr * (1 - np.cos(theta)) - xr * np.sin(theta)],
                               [0, 0, 1]])

        new_vertices = []
        # vertices_of_selected_polygon = self.canvas.coords(self.canvas.selected)
        for polygon_vertices in self.vertices_of_polygon[self.canvas.selected]:
            new_vertices.append([polygon_vertices[0], polygon_vertices[1], 1])

        transposed_vertices = np.transpose(np.asarray(new_vertices))
        output_matrix = np.transpose(rotation.dot(transposed_vertices))

        new_vertices = []
        for vertix in output_matrix:
            new_vertices.append((vertix[0], vertix[1]))

        self.canvas.delete(self.canvas.selected)
        self.polygons.remove(self.canvas.selected)
        self.vertices_of_polygon.pop(self.canvas.selected)

        self.polygons.append(self.canvas.create_polygon(new_vertices, outline="black", fill="", tags=['polygon_2']))
        self.vertices_of_polygon[self.polygons[-1]] = new_vertices
        self.canvas.selected = self.polygons[-1]
        self.canvas.itemconfig(self.canvas.selected, outline='red')
        # self.vertices = new_vertices
        # print(self.vertices)


    def set_point_for_rotating_and_scaling_with_mouse(self, event):
        self.set_point_for_rotating_and_scaling([event.x, event.y])

    def set_point_for_rotating_and_scaling(self, position):
        if self.defined_point is not None:
            self.canvas.delete(self.defined_point)
        self.defined_point = self.canvas.create_oval(position[0], position[1], position[0]+2, position[1]+2, fill='black')

    def get_angle(self, p1, p2, p3):
        angle = math.atan2(p3[1] - p1[1], p3[0] - p1[0]) - math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        return angle

    def scale_polygon(self, sx, sy):
        coords = self.canvas.coords(self.defined_point)
        xr = coords[0]
        yr = coords[1]

        scale = np.asarray([[sx, 0, xr * (1 - sx)],
                            [0, sy, yr * (1 - sy)],
                            [0, 0, 1]])

        new_vertices = []

        for polygon_vertices in self.vertices_of_polygon[self.canvas.selected]:
            new_vertices.append([polygon_vertices[0], polygon_vertices[1], 1])

        transposed_vertices = np.transpose(np.asarray(new_vertices))

        output_matrix = np.transpose(scale.dot(transposed_vertices))

        new_vertices = []
        for vertix in output_matrix:
            new_vertices.append((vertix[0], vertix[1]))

        self.canvas.delete(self.canvas.selected)
        self.polygons.remove(self.canvas.selected)
        self.vertices_of_polygon.pop(self.canvas.selected)

        self.polygons.append(self.canvas.create_polygon(new_vertices, outline="black", fill="", tags=['polygon_2']))
        self.vertices_of_polygon[self.polygons[-1]] = new_vertices
        self.canvas.selected = self.polygons[-1]
        self.canvas.itemconfig(self.canvas.selected, outline='red')

    def distance_between_two_points(self, first_point, second_point):
        return first_point[0] - second_point[0], first_point[1] - second_point[1]

    def activate_button(self, some_button):
        if self.active_button is not None:
            self.active_button.config(relief=tk.RAISED)
        some_button.config(relief=tk.SUNKEN)
        self.active_button = some_button

    def reset_all_ovals(self):
        for i in self.ovals:
            self.canvas.delete(i)
        self.clicks.clear()
        self.ovals.clear()
Paint()
