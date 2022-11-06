from PIL import Image, ImageTk
import PySimpleGUI as sg
import pathlib
import numpy as np
import math
import statistics
import copy

# im = Image.open('/home/me3eh/grafika/zadanie_4/ppm-obrazy-testowe/ppm-obrazy-testowe/ppm-test-01-p3.ppm')
def get_info_from_photo(image):
    pixels = list(image.getdata())
    width, height = image.size
    return pixels, width, height
#
def convert_into_normal_array(pixels, width, height):
    return [pixels[i * width:(i + 1) * width] for i in range(height)]
#
def check_pixel_border(pixel):
    if pixel > 255:
        return 255
    if pixel < 0:
        return 0
    return pixel

def add_to_arrays(pixels, width, height, change_pixel):
    new_pixels = pixels.copy()
    for i in range(height):
        for j in range(width):
            rgb_array = [0] * 3
            for x in range(3):
                rgb_array[x] = pixels[i][j][x] + change_pixel[x]
                rgb_array[x] = check_pixel_border(int(rgb_array[x]))

            new_pixels[i][j] = (rgb_array[0], rgb_array[1], rgb_array[2])
    return new_pixels

def multiply_pixels(pixels, width, height, change_pixel):
    new_pixels = pixels.copy()
    for i in range(height):
        for j in range(width):
            rgb_array = [0] * 3
            for x in range(3):
                rgb_array[x] = pixels[i][j][x] * change_pixel[x]
                rgb_array[x] = check_pixel_border(int(rgb_array[x]))

            new_pixels[i][j] = (rgb_array[0], rgb_array[1], rgb_array[2])
    return new_pixels

def divide_pixels(pixels, width, height, change_pixel):
    new_pixels = pixels.copy()
    for i in range(height):
        for j in range(width):
            rgb_array = [0] * 3
            for x in range(3):
                if change_pixel[x] == 0:
                    rgb_array[x] = 0
                else:
                    rgb_array[x] = pixels[i][j][x] / change_pixel[x]
                    rgb_array[x] = check_pixel_border(int(rgb_array[x]))

            new_pixels[i][j] = (rgb_array[0], rgb_array[1], rgb_array[2])
    return new_pixels

def grascale_averaging(pixels, width, height):
    new_pixels = pixels.copy()
    for i in range(height):
        for j in range(width):
            rgb_sum = 0
            for x in range(3):
                rgb_sum += pixels[i][j][x]
            new_pixels[i][j] = (int(rgb_sum / 3), int(rgb_sum / 3), int(rgb_sum / 3))
    return new_pixels

def grascale_desaturation(pixels, width, height):
    new_pixels = pixels.copy()
    for i in range(height):
        for j in range(width):
            gray = (max(pixels[i][j][0], pixels[i][j][1], pixels[i][j][2]) + min(pixels[i][j][0], pixels[i][j][1], pixels[i][j][2])) / 2
            new_pixels[i][j] = (int(gray), int(gray), int(gray))
    return new_pixels

def pixels_into_image(pixels):
    array = np.array(pixels, dtype=np.uint8)
    asd = Image.fromarray(array)
    image = ImageTk.PhotoImage(image=asd)
    return image

def image_from_file(path):
    img = Image.open(path)
    size = (1920, 1080)
    img.thumbnail(size)
    image = ImageTk.PhotoImage(image=img)
    return image, img

def validation_on_input(values, event, window):
    full_value_from_input = values[event]
    if len(full_value_from_input) > 0:
        last_character = values[event][-1]
        if last_character not in ('-0123456789.'):
            window[event].update(values[event][:-1])
            return
        try:
            float(full_value_from_input)
        except ValueError:
            window[event].update(values[event][:-1])
            return
        if not (255 >= float(full_value_from_input) >= -255):
            return

def get_neighbours(pixels, index, width, height):
    neighbours = []
    index_to_check = [-1, 0, 1]
    for i in index_to_check:
        neighbour_x = index[0] + i
        if neighbour_x < 0 or neighbour_x >= height:
            continue
        for j in index_to_check:
            neighbour_y = index[1] + j
            if neighbour_y < 0 or neighbour_y >= width:
                continue
            neighbours.append(pixels[neighbour_x][neighbour_y])
    return neighbours

def get_neighbours_for_mask(pixels, index, width, height):
    neighbours = []
    index_to_check = [-1, 0, 1]
    for i in index_to_check:
        neighbour_x = index[0] + i
        if neighbour_x < 0 or neighbour_x >= height:
            for x in range(3):
                neighbours.append(None)
            continue
        for j in index_to_check:
            neighbour_y = index[1] + j
            if neighbour_y < 0 or neighbour_y >= width:
                neighbours.append(None)
                continue
            neighbours.append(pixels[neighbour_x][neighbour_y])
    return neighbours

def mean_filter(pixels, width, height):
    pixels_copy = pixels.copy()
    for i in range(height):
        for j in range(width):
            neighbours = get_neighbours(pixels, (i, j), width, height)
            red = 0
            green = 0
            blue = 0
            for neighbour in neighbours:
                red += neighbour[0]
                green += neighbour[1]
                blue += neighbour[2]
            mean = (red / len(neighbours), green / len(neighbours), blue / len(neighbours))

            pixels_copy[i][j] = mean
    return pixels_copy

def median_filter(pixels, width, height):
    pixels_copy = pixels.copy()
    for i in range(height):
        for j in range(width):
            neighbours = get_neighbours(pixels, (i, j), width, height)
            red = []
            green = []
            blue = []
            for neighbour in neighbours:
                red.append(neighbour[0])
                green.append(neighbour[1])
                blue.append(neighbour[2])
            pixels_copy[i][j] = (statistics.median(red), statistics.median(green), statistics.median(blue))
    return pixels_copy

def rgb_add(first, second, third):
    red = first[0] + 2 * second[0] + third[0]
    green = first[1] + 2 * second[1] + third[1]
    blue = first[2] + 2 * second[2] + third[2]
    return (red, green, blue)

def rgb_subtract(first, second):
    red = abs(first[0] - second[0])
    green = abs(first[1] - second[1])
    blue = abs(first[2] - second[2])
    return (red, green, blue)

def rgb_add_two(first, second):
    red = abs(first[0] + second[0])
    green = abs(first[1] + second[1])
    blue = abs(first[2] + second[2])
    return (red, green, blue)

def sobel_filter(pixels, width, height, threshold):
    pixels_copy = pixels.copy()
    h1 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    h2 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    dd = np.asarray(pixels)
    for i in range(height):
        for j in range(width):
            if i == 0 or j == 0 or i == height - 1 or j == width - 1:
                pixels_copy[i][j] = (0, 0, 0)
            else:
                this_slice = dd[i - 1:i + 2, j - 1:j + 2]
                g1 = this_slice * h1
                g2 = this_slice * h2
                g1_sum = np.sum(g1)
                g2_sum = np.sum(g2)
                g = math.sqrt((g1_sum ** 2) + (g2_sum ** 2))

                pixels_copy[i][j] = (g, g, g)
    return pixels_copy

def multiply_tuple(pixels, mask):
    c = [0] * 3
    for i in range(3):
        c[i] = pixels[i] * mask
    return (c[0], c[1], c[2])

# def gaussian_blur(pixels, width, height, threshold):
#     values = [-1, 0, 1]
#     pixels_copy = pixels.copy()
#     h1 = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
#
#     # dd = np.asarray(pixels)
#     for i in range(width):
#         for j in range(height):
#             neighbours = get_neighbours_for_mask(pixels, (i, j), width, height)
#             temp_mask = [[0] * 3] * 3
#             for index_x, x in enumerate(values):
#                 value_after_adding_x = x + i
#                 if value_after_adding_x < 0 or value_after_adding_x > width:
#                     continue
#                 for index_y, y in enumerate(values):
#                     value_after_adding_y = y + j
#                     if value_after_adding_y < 0 or value_after_adding_y > height:
#                         continue
#                     if neighbours[index_x * 3 + index_y] is not None:
#                         temp_mask[index_x][index_y] = multiply_tuple(neighbours[index_x*3 + index_y], h1[index_x][index_y])
#             sum = [0, 0, 0]
#             amount_of_non_none = sum(x != 0 for x in temp_mask)
#
#             for c in temp_mask:
#                 for value in c:
#                     print(value)
#                     print(temp_mask)
#                     print(type(value))
#                     if value != 0:
#                         print("wartosc to", value)
#                         sum[0] += value[0]
#                         sum[1] += value[1]
#                         sum[2] += value[2]
#                         pixels_copy[i][j] = (sum[0] / amount_of_non_none, sum[1] / amount_of_non_none, sum[2] / amount_of_non_none)
#                 # if i == 0 or j == 0 or i == height - 1 or j == width - 1:
#             #     pixels_copy[i][j] = (0, 0, 0)
#             # else:
#             #     this_slice = dd[i - 1:i + 2, j - 1:j + 2]
#             #     g1 = this_slice * h1
#             #     g1_sum = np.sum(g1)
#             #     g = abs(g1_sum)
#
#                 # pixels_copy[i][j] = (255, 255, 255) if g >= threshold else (0, 0, 0)
#     return pixels_copy

def gaussian_blur(pixels, width, height, threshold):
    pixels_copy = pixels.copy()
    h1 = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    dd = np.asarray(pixels)
    for i in range(height):
        for j in range(width):
            if i == 0 or j == 0 or i == height - 1 or j == width - 1:
                pixels_copy[i][j] = pixels[i][j]
            else:
                this_slice = dd[i - 1:i + 2, j - 1:j + 2]
                g1 = this_slice * h1
                g1_sum = np.sum(g1)
                g = math.sqrt((g1_sum ** 2))

                pixels_copy[i][j] = pixels[i][j] if g >= threshold else (0, 0, 0)
    return pixels_copy


DEFAULT_IMAGE = f'{pathlib.Path(__file__).parent.resolve()}/ppm-obrazy-testowe/ppm-test-06-p6.ppm'

layout = [
    [
        sg.Input(key='-HUHI-', visible=False, enable_events=True),
        sg.Column(
            [
                [
                    sg.Button("Adding", key='-FILTER-ADD-')
                ],
                [
                    sg.Button("Subtracting", key='-FILTER-SUBTRACT-')
                ],
                [
                    sg.Button("Multiplying", key='-FILTER-MULTIPLY-')
                ],
                [
                    sg.Button("Dividing", key='-FILTER-DIVIDE-')
                ],
                [
                    sg.Button("Change brightness", key='-FILTER-BRIGHT-')
                ],
                [
                    sg.Button("Grayscale #1", key='-FILTER-GRAYSCALE-1-')
                ],
                [
                    sg.Button("Grayscale #2", key='-FILTER-GRAYSCALE-2-')
                ],
                [
                    sg.HorizontalSeparator()
                ],
                [
                    sg.Button("Mean filter", key='-FILTER-MEAN-')
                ],
                [
                    sg.Button("Sobel filter", key='-FILTER-SOBEL-')
                ],
                [
                    sg.Button("Median filter", key='-FILTER-MEDIAN-')
                ],
                # [
                #     sg.Button("Gaussian Blur", key='-FILTER-GAUSSIAN-')
                # ],
                [
                    sg.Button("RESET IMAGE", key='-RESET-', button_color='red')
                ],
            ]
        ),
        sg.Column(
            [
                [
                    sg.Input(0, size=(5,5), key='-PIXEL-INPUT-0-', enable_events=True)
                ],
                [
                    sg.Input(1, size=(5,5), key='-PIXEL-INPUT-1-', enable_events=True)
                ],
                [
                    sg.Input(255, size=(5,5), key='-PIXEL-INPUT-2-', enable_events=True)
                ]
            ]
        ),
        sg.FileBrowse(file_types=(('PPM files', '*.ppm PPM'),
                                  ('JPG files', '*.jpg JPG'),
                                  ('PNG files', '*.png PNG'),
                                  ('JPEG files', '*.png JPEG')
                                  ),
                      target='-HUHI-'
                      ),
        sg.Image(size=(1920, 1080), key='-IMAGE-')
    ]
]
actual_image = None
real_image = None



def gui_for_image():
    window = sg.Window('Window Title', layout, finalize=True)
    image_to_show, image_to_modify = image_from_file(DEFAULT_IMAGE)
    window['-IMAGE-'].update(data=image_to_show)
    pixels, width, height = get_info_from_photo(image_to_modify)
    pixels = convert_into_normal_array(pixels, width, height)
    changed_pixels = copy.deepcopy(pixels)
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == '-HUHI-':
            if values[event] is not None:
                image_to_show, image_to_modify = image_from_file(values[event])
                window['-IMAGE-'].update(data=image_to_show)
                pixels, width, height = get_info_from_photo(image_to_modify)
                pixels = convert_into_normal_array(pixels, width, height)
                changed_pixels = copy.deepcopy(pixels)
        elif '-PIXEL-INPUT-' in event:
            validation_on_input(values, event, window)
        elif 'FILTER' in event:
            first_input = float(window['-PIXEL-INPUT-0-'].get())
            second_input = float(window['-PIXEL-INPUT-1-'].get())
            third_input = float(window['-PIXEL-INPUT-2-'].get())

            if 'ADD' in event:
                new_pixels = add_to_arrays(changed_pixels, width, height, (first_input, second_input, third_input))
            elif 'SUBTRACT' in event:
                new_pixels = add_to_arrays(changed_pixels, width, height, (-1 * first_input, -1 * second_input, -1 * third_input))
            elif 'MULTIPLY' in event:
                new_pixels = multiply_pixels(changed_pixels, width, height,(first_input, second_input, third_input))
            elif 'DIVIDE' in event:
                new_pixels = divide_pixels(changed_pixels, width, height,(first_input, second_input, third_input))
            elif 'BRIGHT' in event:
                new_pixels = add_to_arrays(changed_pixels, width, height, (second_input, second_input, second_input))
            elif 'GRAYSCALE-1' in event:
                new_pixels = grascale_averaging(changed_pixels, width, height)
            elif 'GRAYSCALE-2' in event:
                new_pixels = grascale_desaturation(changed_pixels, width, height)
            elif 'MEAN' in event:
                new_pixels = mean_filter(changed_pixels, width, height)
            elif 'MEDIAN' in event:
                new_pixels = median_filter(changed_pixels, width, height)
            elif 'SOBEL' in event:
                new_pixels = sobel_filter(changed_pixels, width, height, threshold=int(second_input))
            elif 'GAUSSIAN' in event:
                new_pixels = gaussian_blur(changed_pixels, width, height, threshold=int(second_input))

            image = pixels_into_image(new_pixels)
            window['-IMAGE-'].update(data=image)
            changed_pixels = new_pixels
        elif event == '-RESET-':
            changed_pixels = copy.deepcopy(pixels)
            image = pixels_into_image(pixels)
            window['-IMAGE-'].update(data=image)
    window.close()


gui_for_image()

