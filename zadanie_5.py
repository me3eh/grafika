from PIL import Image, ImageTk
import PySimpleGUI as sg
import pathlib
import numpy as np
import math
import statistics
import copy
import matplotlib.pyplot as plt

def get_info_from_photo(image):
    pixels = list(image.getdata())
    width, height = image.size
    return pixels, width, height
#
def convert_into_normal_array(pixels, width, height):
    return [pixels[i * width:(i + 1) * width] for i in range(height)]

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


def get_histogram(pixels, height, width):
    a = np.zeros((256,), dtype=np.float16)
    for i in range(height):
        for j in range(width):
            g = pixels[i][j][0]
            a[g] = a[g] + 1

    return a

def find_highest_lowest_pixel(original_pixels, width, height):
    lowest = 255
    highest = 0
    for i in range(height):
        for j in range(width):
            if original_pixels[i][j][0] < lowest:
                lowest = original_pixels[i][j][0]

            if original_pixels[i][j][0] > highest:
                highest = original_pixels[i][j][0]
    return highest, lowest

def histogram_stretching(original_pixels, width, height):
    pixels = copy.deepcopy(original_pixels)
    highest_pixel, lowest_pixel = find_highest_lowest_pixel(original_pixels, width, height)
    ratio = (255 / (highest_pixel - lowest_pixel))
    pixels = copy.deepcopy(original_pixels)
    for i in range(height):
        for j in range(width):
            final_brightness = round(ratio * (original_pixels[i][j][0] - lowest_pixel))
            pixels[i][j] = (final_brightness, final_brightness, final_brightness)
    return pixels

def histogram_equalization(original_pixels, width, height):
    pixels = copy.deepcopy(original_pixels)

    a = get_histogram(pixels, height, width)
    tmp = 1.0 / (height * width)
    b = np.zeros((256,), dtype=np.float16)

    for i in range(256):
        for j in range(i + 1):
            b[i] += a[j] * tmp
        b[i] = round(b[i] * 255)
    b = b.astype(np.uint8)

    for i in range(height):
        for j in range(width):
            g = pixels[i][j]
            pixels[i][j] = (b[g[0]], b[g[0]], b[g[0]])
    return pixels

def plot_histogram(pixels, height, width):
    data = get_histogram(pixels, height, width)
    histogram_counts = list(map(int, data))
    histogram_values = np.arange(256)
    # print(histogram_counts)
    print(histogram_values)
    print(histogram_counts)
    plt.hist(histogram_values, weights=histogram_counts, range=(0, 256), density=False, bins=256)
    plt.ylabel('Count')
    plt.xlabel('Pixel brightness')
    plt.show()

def binarization(original_pixels, width, height, threshold=70):
    pixels = copy.deepcopy(original_pixels)
    lut = np.concatenate((np.zeros(threshold), 255 * np.ones(255 - threshold)))

    for i in range(height):
        for j in range(width):
            pixel_value = int(lut[pixels[i][j][0]])
            pixels[i][j] = (pixel_value, pixel_value, pixel_value)
    return pixels

def black_percent_threshold(original_pixels, width, height, percent):
    amount_of_pixels = width * height * (percent / 100)
    amount_of_pixels_summed = 0
    data = get_histogram(original_pixels, height, width)
    histogram_counts = list(map(int, data))
    for i in range(256):
        print(f"{i}: {amount_of_pixels_summed}")
        print(f"final: {amount_of_pixels}")
        amount_of_pixels_summed += histogram_counts[i]
        if amount_of_pixels_summed >= amount_of_pixels:
            return i
    return 255


def selection_iterative(original_pixels, height, width, initial_threshold=127, iterations=3):
    data = get_histogram(original_pixels, height, width)
    histogram = list(map(int, data))
    threshold = initial_threshold
    print(f"Initial threshold: {threshold}")
    for i in range(iterations):
        threshold = selection_iterative_iteration(histogram, threshold)
        print(f"{i} threshold: {threshold}")

    return threshold


def selection_iterative_iteration(histogram, prev_estimation):
    ul = bl = ur = br = 0

    for i in range(0, prev_estimation - 1):
        ul += histogram[i] * i
        bl += histogram[i]

    for j in range(prev_estimation - 1, len(histogram)):
        ur += histogram[j] * j
        br += histogram[j]
    if bl == 0 or br == 0:
        new_estimation = prev_estimation
    else:
        new_estimation = round((ul / (bl * 2)) + (ur / (2 * br)))

    return new_estimation

DEFAULT_IMAGE = f'{pathlib.Path(__file__).parent.resolve()}/obrazy/Lenna_(test_image).png'

layout = [
    [
        sg.Input(key='-HUHI-', visible=False, enable_events=True),
        sg.Column(
            [
                [
                    sg.Button("Histogram equalization", key='-HISTOGRAM-EQ-')
                ],
                [
                    sg.Button("Histogram stretching", key='-HISTOGRAM-STRETCHING-')
                ],
                [
                    sg.Button("Show histogram", key='-HISTOGRAM-SHOW-', button_color='green')
                ],
                [
                    sg.HorizontalSeparator()
                ],
                [
                    sg.Button("Manual binarization", key='-BINARIZATION-MANUAL-')
                ],
                [
                    sg.Button("Percent binarization", key='-BINARIZATION-PERCENT-')
                ],
                [
                    sg.Button("Mean Iterative binarization", key='-BINARIZATION-MEAN-ITERATIVE-')
                ],
                [
                    sg.Button("RESET IMAGE", key='-RESET-', button_color='red')
                ],
            ]
        ),
        sg.Column(
            [
                [
                    sg.Text("Binarization Input"),
                    sg.Text("Binarization iterative")
                ],
                [
                    sg.Input(100, size=(5,5), key='-PIXEL-INPUT-1-', enable_events=True),
                    sg.Column([[]], expand_x=True),
                    sg.Input(10, size=(5, 5), key='-ITERATIONS-', enable_events=True)
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
    window = sg.Window('Window Title', layout, finalize=True, location=(500, 500))
    image_to_show, image_to_modify = image_from_file(DEFAULT_IMAGE)
    window['-IMAGE-'].update(data=image_to_show)
    pixels, width, height = get_info_from_photo(image_to_modify)
    pixels = convert_into_normal_array(pixels, width, height)
    pixels = grascale_desaturation(pixels, width, height)
    image = pixels_into_image(pixels)
    window['-IMAGE-'].update(data=image)
    changed_pixels = copy.deepcopy(pixels)
    while True:
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == '-HUHI-':
            if values[event] is not None:
                image_to_show, image_to_modify = image_from_file(values[event])
                window['-IMAGE-'].update(data=image_to_show)
                pixels, width, height = get_info_from_photo(image_to_modify)
                pixels = convert_into_normal_array(pixels, width, height)

                pixels = grascale_desaturation(pixels, width, height)

                image = pixels_into_image(pixels)
                window['-IMAGE-'].update(data=image)
                changed_pixels = copy.deepcopy(pixels)
        elif '-HISTOGRAM-' in event:
            if '-EQ-' in event:
                new_pixels = histogram_equalization(changed_pixels, width, height)
                image = pixels_into_image(new_pixels)
                window['-IMAGE-'].update(data=image)
                changed_pixels = copy.deepcopy(new_pixels)
            elif '-SHOW-' in event:
                plot_histogram(changed_pixels, height, width)
            elif '-STRETCHING-' in event:
                new_pixels = histogram_stretching(changed_pixels, width, height)
                image = pixels_into_image(new_pixels)
                window['-IMAGE-'].update(data=image)
                changed_pixels = copy.deepcopy(new_pixels)
        elif '-BINARIZATION-' in event:
            pixel_value = window['-PIXEL-INPUT-1-'].get()
            iterations = window['-ITERATIONS-'].get()
            if '-MANUAL-' in event:
                new_pixels = binarization(pixels, width, height, threshold=int(pixel_value))
                image = pixels_into_image(new_pixels)
                window['-IMAGE-'].update(data=image)
                changed_pixels = copy.deepcopy(new_pixels)
            elif '-PERCENT-' in event:
                threshold = black_percent_threshold(pixels, width, height, int(pixel_value))
                print(f'THRESHOLD: {threshold}')
                new_pixels = binarization(pixels, width, height, threshold=threshold)
                image = pixels_into_image(new_pixels)
                window['-IMAGE-'].update(data=image)
                changed_pixels = copy.deepcopy(new_pixels)
            elif '-MEAN-ITERATIVE-' in event:
                threshold = selection_iterative(pixels, width, height, int(pixel_value), int(iterations))
                print(f'THRESHOLD: {threshold}')
                new_pixels = binarization(pixels, width, height, threshold=threshold)
                image = pixels_into_image(new_pixels)
                window['-IMAGE-'].update(data=image)
                changed_pixels = copy.deepcopy(new_pixels)


        elif event == '-RESET-':
            changed_pixels = copy.deepcopy(pixels)
            image = pixels_into_image(pixels)
            window['-IMAGE-'].update(data=image)
    window.close()


gui_for_image()

