#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    # Tkinter for Python 2.xx
    import Tkinter as tk
except ImportError:
    # Tkinter for Python 3.xx
    import tkinter as tk

APP_TITLE = "Drag & Drop Tk Canvas Images"
APP_XPOS = 100
APP_YPOS = 100
APP_WIDTH = 300
APP_HEIGHT = 200

IMAGE_PATH = "/home/me3eh/grafika/zadanie_2/"


class CreateCanvasObject(object):
    def __init__(self, canvas, image_name, xpos, ypos):
        self.canvas = canvas
        self.image_name = image_name
        self.xpos, self.ypos = xpos, ypos

        self.tk_image = tk.PhotoImage(
            file="{}{}".format(IMAGE_PATH, image_name))
        self.image_obj = canvas.create_image(
            xpos, ypos, image=self.tk_image)

        canvas.tag_bind(self.image_obj, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.image_obj, '<ButtonRelease-1>', self.release)
        self.move_flag = False

    def move(self, event):
        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y

            self.canvas.move(self.image_obj,
                             new_xpos - self.mouse_xpos, new_ypos - self.mouse_ypos)

            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.image_obj)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y

    def release(self, event):
        self.move_flag = False


class Application(tk.Frame):

    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Frame.__init__(self, master)

        self.canvas = tk.Canvas(self, width=400, height=400, bg='steelblue',
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.image_1 = CreateCanvasObject(self.canvas, "./ppm-test-05-p6.ppm", 100, 100)
        self.image_2 = CreateCanvasObject(self.canvas, "ppm-test-05-p6.ppm", 200, 100)

    def close(self):
        print("Application-Shutdown")
        self.master.destroy()


def main():
    app_win = tk.Tk()
    app_win.title(APP_TITLE)
    app_win.geometry("+{}+{}".format(APP_XPOS, APP_YPOS))
    # app_win.geometry("{}x{}".format(APP_WIDTH, APP_HEIGHT))

    app = Application(app_win).pack(fill='both', expand=True)

    app_win.mainloop()


if __name__ == '__main__':
    main()