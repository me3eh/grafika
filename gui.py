import tkinter as tk

root = tk.Tk()

def int_to_hex(number):
    number = hex(number)[2:]
    if len(str(number)) == 1:
        return f'0{number}'
    return number

def change_color_of_canvas(event):
    red = red_scale.get()
    blue = blue_scale.get()
    green = green_scale.get()
    print(f'#{int_to_hex(red)}{int_to_hex(blue)}{int_to_hex(green)}')
    canvas.configure(bg=f'#{int_to_hex(red)}{int_to_hex(blue)}{int_to_hex(green)}')

def cmyk_reconfiguration(event):
    red = red_scale.get()
    blue = blue_scale.get()
    green = green_scale.get()
    black = (1 - max(max(red, green), blue)/255)
    black_scale.set(black * 100)
    if black != 1:
        cyan = (1 - red/255 - black) / (1 - black)
        cyan_scale.set(cyan * 100)

        magenta = (1 - green/255 - black) / (1 - black)
        magenta_scale.set(magenta * 100)

        yellow = (1 - blue/255 - black) / (1 - black)
        yellow_scale.set(yellow * 100)

def rgb_reconfiguration(event):
    cyan = cyan_scale.get()
    yellow = yellow_scale.get()
    black = black_scale.get()
    magenta = magenta_scale.get()
    red = 255 * (1 - cyan/100) * (1 - black/100)
    red_scale.set(red)
    green = 255 * (1 - magenta/100) * (1 - black/100)
    green_scale.set(green)
    blue = 255 * (1 - yellow/100) * (1 - black/100)
    blue_scale.set(blue)

def actions_for_rgb(event):
    change_color_of_canvas(event)
    cmyk_reconfiguration(event)

def actions_for_cmyk(event):
    change_color_of_canvas(event)
    rgb_reconfiguration(event)

def define_color_slider(place, max_limit, default):
    slider = tk.Scale(root, from_=0, to=max_limit, orient=tk.HORIZONTAL)
    slider.set(default)
    slider.grid(row=place[0], column=place[1])
    return slider

def define_color_label(place, color):
    label = tk.Label(root, text=color)
    label.grid(row=place[0], column=place[1])
    return label

red_label = define_color_label((0, 0), 'Red')
red_scale = define_color_slider((1, 0), 255, 0)

blue_label = define_color_label((2, 0), 'Blue')
blue_scale = define_color_slider((3, 0), 255, 0)

green_label = define_color_label((4, 0), 'Green')
green_scale = define_color_slider((5, 0), 255, 0)

yellow_label = define_color_label((0, 2), 'Yellow')
yellow_scale = define_color_slider((1, 2), 100, 0)

cyan_label = define_color_label((2, 2), 'Cyan')
cyan_scale = define_color_slider((3, 2), 100, 0)

magenta_label = define_color_label((4, 2), 'Magenta')
magenta_scale = define_color_slider((5, 2), 100, 0)

black_label = define_color_label((6, 2), 'Black')
black_scale = define_color_slider((7, 2), 100, 100)

yellow_scale.bind('<B1-Motion>', actions_for_cmyk)
cyan_scale.bind('<B1-Motion>', actions_for_cmyk)
magenta_scale.bind('<B1-Motion>', actions_for_cmyk)
black_scale.bind('<B1-Motion>', actions_for_cmyk)
red_scale.bind('<B1-Motion>', actions_for_rgb)
blue_scale.bind('<B1-Motion>', actions_for_rgb)
green_scale.bind('<B1-Motion>', actions_for_rgb)

canvas = tk.Canvas(root, bg='black')
canvas.grid(row=2, rowspan=4, column=1)

root.mainloop()
