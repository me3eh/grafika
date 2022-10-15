from tkinter import *
from PIL import Image as PIL_image
from PIL import ImageTk as PIL_imagetk
image = '/home/me3eh/grafika/zadanie_2/ppm-test-06-p6.ppm'
window =Tk()
window.geometry('400x400')
zoom_in=1
zoom_out=1
max_num=1
min_num=1
level_zoom =0
def zoom(level, image):
    print('level', level)
    if level == 0:
        return image
    if level > 0:
        return image._PhotoImage__photo.zoom(level+1)
    # elif level == 0:
    #     return image._PhotoImage__photo.subsample(1)
    return image._PhotoImage__photo.subsample((level * - 1) + 1)

def ZoomIn(k):
    global img1
    global img2
    global zoom_in
    global max_num
    global level_zoom
    # if zoom_in > 1:
    img1 = PIL_imagetk.PhotoImage(file=image)
    max_num += 1
    level_zoom +=1
    print('typ przed', type(img1))
    img1 = zoom(level_zoom, img1)
    print('typ po', type(img1))
    # img1 = img1._PhotoImage__photo.zoom(max_num)
    label.config(image=img1)


    # img1 = PIL_imagetk.PhotoImage(file=image)
    zoom_in+=1


def ZoomOut(k):
    # global img2
    global img1
    global zoom_out
    global zoom_in
    global min_num
    global level_zoom
    # A condition which will let create image object in second execution
    # if zoom_out > 1:
    #     img2 = PIL_imagetk.PhotoImage(file=image)
    min_num += 1
    img1 = PIL_imagetk.PhotoImage(file=image)

    # if min_num<3:
    level_zoom -=1
    # zoom(level_zoom, img2)
    print('typ przed', type(img1))
    img1 = zoom(level_zoom, img1)
    print('typ po', type(img1))

    # img2 = img2._PhotoImage__photo.subsample(min_num)
    label.config(image=img1)
    # else:
    #     img2 = img2._PhotoImage__photo.subsample(3)
    #     label.config(image=img2)
    #     min_num=1

    # img1 = PIL_imagetk.PhotoImage(file=image)
    zoom_out+=1

def move(event):
    global my_image
img1 = PIL_imagetk.PhotoImage(file=image)
# image1 = r"C:\Python26\Lib\site-packages\pygame\examples\data\ADN_animation.gif"
photo1 = PhotoImage(file=image)
# img2 = PIL_imagetk.PhotoImage(file=image)
label =Label(window, image=img1)
label.pack()
window.bind('<Button-4>', ZoomIn)
window.bind('<Button-5>', ZoomOut)
# canvas = Canvas(window, height = 1500, width = 1000, bg = 'LightBlue3')
# canvas.pack()
# my_image = canvas.create_image(0, 0, image=photo1)
window.bind('<Motion>', move)

# my_image.pack
# label.pack()

# btn=Button(window,text='zoom in',command=ZoomIn)
# btn.pack()
#
# btn2=Button(window,text='zoom out',command=ZoomOut)
# btn2.pack()
window.mainloop()
