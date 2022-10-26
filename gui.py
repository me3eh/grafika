import tkinter as tk

root = tk.Tk()


def only_numbers_between_0_and_255(char, whole_number):
    digit = char.isdigit()
    if not digit:
        return digit
    if whole_number == '':
        whole_number = 0
    return 255 >= int(whole_number) >= 0


def only_numbers_between_0_and_100(char, whole_number):
    digit = char.isdigit()
    if not digit:
        return digit
    if whole_number == '':
        whole_number = 0
    return 100 >= int(whole_number) >= 0


def int_to_hex(number):
    number = hex(number)[2:]
    if len(str(number)) == 1:
        return f'0{number}'
    return number


def change_color_of_canvas(event):
    red = red_scale.get()
    blue = blue_scale.get()
    green = green_scale.get()
    print(f'kolor: #{int_to_hex(red)}{int_to_hex(green)}{int_to_hex(blue)}')
    canvas.configure(bg=f'#{int_to_hex(red)}{int_to_hex(green)}{int_to_hex(blue)}')


def cmyk_reconfiguration(event):
    red = red_scale.get()
    blue = blue_scale.get()
    green = green_scale.get()
    black = (1 - max(max(red, green), blue)/255)
    black_scale.set(black * 100)
    black_input.delete(0, tk.END)
    black_input.insert(0, int(black))

    if black != 1:
        cyan = (1 - red/255 - black) / (1 - black)
        cyan_scale.set(cyan * 100)

        cyan_input.delete(0, tk.END)
        cyan_input.insert(0, int(cyan))

        magenta = (1 - green/255 - black) / (1 - black)
        magenta_scale.set(magenta * 100)

        magenta_input.delete(0, tk.END)
        magenta_input.insert(0, int(magenta))

        yellow = (1 - blue/255 - black) / (1 - black)
        yellow_scale.set(yellow * 100)
        yellow_input.delete(0, tk.END)
        yellow_input.insert(0, int(yellow))

def rgb_reconfiguration(event):
    cyan = cyan_scale.get()
    yellow = yellow_scale.get()
    black = black_scale.get()
    magenta = magenta_scale.get()
    red = 255 * (1 - cyan/100) * (1 - black/100)
    red_scale.set(red)
    red_input.delete(0, tk.END)
    red_input.insert(0, int(red))

    green = 255 * (1 - magenta/100) * (1 - black/100)
    green_scale.set(green)
    green_input.delete(0, tk.END)
    green_input.insert(0, int(green))

    blue = 255 * (1 - yellow/100) * (1 - black/100)
    blue_scale.set(blue)
    blue_input.delete(0, tk.END)
    blue_input.insert(0, int(blue))


def set_sliders(colors):
    for color in colors:
        color_value = eval(f'{color}_input.get()')
        eval(f"{color}_scale.set(int({color_value}))")


def slider_and_input_update():
    colors = ['cyan', 'yellow', 'black', 'magenta', 'red', 'blue', 'green']
    for color in colors:
        color_value = eval(f'{color}_scale.get()')
        eval(f'{color}_input.delete(0, tk.END)')
        eval(f'{color}_input.insert(0, int({color_value}))')


def actions_for_rgb(event):
    change_color_of_canvas(event)
    cmyk_reconfiguration(event)
    slider_and_input_update()


def actions_for_cmyk(event):
    change_color_of_canvas(event)
    rgb_reconfiguration(event)
    slider_and_input_update()


def keyboard_click_rgb(event):
    set_sliders(['red', 'blue', 'green'])
    cmyk_reconfiguration(event)
    change_color_of_canvas(event)


def keyboard_click_cmyk(event):
    set_sliders(['cyan', 'magenta', 'yellow', 'black'])
    rgb_reconfiguration(event)
    change_color_of_canvas(event)


def define_color_slider(place, max_limit, default):
    slider = tk.Scale(root, from_=0, to=max_limit, orient=tk.HORIZONTAL, showvalue=False)
    slider.set(default)
    slider.grid(row=place[0], column=place[1])
    return slider


def define_color_label(place, color):
    label = tk.Label(root, text=color)
    label.grid(row=place[0], column=place[1])
    return label


validation_rgb = root.register(only_numbers_between_0_and_255)
validation_cmyk = root.register(only_numbers_between_0_and_100)


def define_color_input(place, type, default):
    validation = validation_rgb if type == 'RGB' else validation_cmyk
    input = tk.Entry(root, validate="all", validatecommand=(validation, '%S', '%P'), width=10)
    input.insert(0, default)

    input.grid(row=place[0], column=place[1])
    return input


red_label = define_color_label((0, 0), 'Red')
red_input = define_color_input((1, 0), 'RGB', 0)
red_scale = define_color_slider((2, 0), 255, 0)

green_label = define_color_label((3, 0), 'Green')
green_input = define_color_input((4, 0), 'RGB', 0)
green_scale = define_color_slider((5, 0), 255, 0)

blue_label = define_color_label((6, 0), 'Blue')
blue_input = define_color_input((7, 0), 'RGB', 0)
blue_scale = define_color_slider((8, 0), 255, 0)


yellow_label = define_color_label((0, 2), 'Yellow')
yellow_input = define_color_input((1, 2), 'CMYK', 0)
yellow_scale = define_color_slider((2, 2), 100, 0)

cyan_label = define_color_label((3, 2), 'Cyan')
cyan_input = define_color_input((4, 2), 'CMYK', 0)
cyan_scale = define_color_slider((5, 2), 100, 0)

magenta_label = define_color_label((6, 2), 'Magenta')
magenta_input = define_color_input((7, 2), 'CMYK', 0)
magenta_scale = define_color_slider((8, 2), 100, 0)

black_label = define_color_label((9, 2), 'Black')
black_input = define_color_input((10, 2), 'CMYK', 100)
black_scale = define_color_slider((11, 2), 100, 100)


cmyk_values = ['yellow', 'cyan', 'magenta', 'black']
for cmyk_value in cmyk_values:
    eval(f"{cmyk_value}_scale.bind('<B1-Motion>', actions_for_cmyk)")

rgb_values = ['red', 'green', 'blue']
for rgb in rgb_values:
    eval(f"{rgb}_scale.bind('<B1-Motion>', actions_for_rgb)")

for value in cmyk_values:
    eval(f"{value}_input.bind('<KeyRelease>', keyboard_click_cmyk)")

for value in rgb_values:
    eval(f"{value}_input.bind('<KeyRelease>', keyboard_click_rgb)")

canvas = tk.Canvas(root, bg='black')
canvas.grid(row=2, rowspan=4, column=1)

root.mainloop()
