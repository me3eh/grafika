import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image
import cv2

root = tk.Tk()
less_go = tk.IntVar()
loaded_image = None
filename = None


def open_image():
    if filename:
        print(less_go.get())
        if less_go:
            cv2.namedWindow("image window", cv2.WINDOW_NORMAL)
        else:
            cv2.namedWindow("image window")
        image = cv2.imread(filename)
        if less_go:
            image = cv2.resize(image, (960, 540))
        cv2.imshow('image window', image)
        asd = 1
        # while asd:
        cv2.waitKey(0)
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        cv2.waitKey(1)


def open_file():
    global loaded_image
    global filename
    filename = fd.askopenfilename(filetypes=[("JPG", "*.jpg"), ("PPM", "*.ppm"), ("JPEG", "*.jpeg")])
    if filename:
        file_name = filename.split('/')[-1]
        label_for_image_info.config(text=file_name)
        loaded_image = Image.open(filename)


def save_to_directory_file():
    filename = fd.asksaveasfilename(filetypes=[("Plik tekstowy", "*.jpeg")], defaultextension="*.jpeg")
    if filename:
        if loaded_image:
            number = scale.get()
            print(number)
            loaded_image.save(filename, quality=int(number), format='jpeg')


import_button = tk.Button(root, text ="Import image", command=open_file)
label_for_image_info = tk.Label(root, text ="No image loaded")
jpeg_conversion = tk.Label(root, text ="Jpeg compression")
save_button = tk.Button(root, text ="Save image as JPEG", command=save_to_directory_file)
open_image_button = tk.Button(root, text ="Open image", command=open_image)
scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
scale.set(100)

checkbox_for_boundings_in_c2 = tk.Checkbutton(root, text="Less go", variable=less_go, onvalue=1, offvalue=0)
open_image_button.grid(row=1, column=0)
import_button.grid(row=1, column=1)
save_button.grid(row=1, column=2)
scale.grid(row=1, column=3)
checkbox_for_boundings_in_c2.grid(row=1, column=4)
label_for_image_info.grid(row=0, column=1)
jpeg_conversion.grid(row=0, column=2)
root.mainloop()
