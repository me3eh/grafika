from tkinter import *
from PIL import Image, ImageTk

win = Tk()

win.geometry("700x350")

canvas = Canvas(win, width=600, height=400, bg="white")
canvas.pack(pady=20)

# Add Images to Canvas widget
image = ImageTk.PhotoImage(Image.open('logo.png'))
img = canvas.create_image(250, 120, anchor=NW, image=image)

def move(e):
   global image
   image = ImageTk.PhotoImage(Image.open('logo.png'))
   canvas.create_image(e.x, e.y, image=image)

# Bind the move function
canvas.bind("<B1-Motion>", move)

win.mainloop()