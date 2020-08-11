from p5 import *
from tkinter import filedialog
import tkinter as tk

img = None # Declare a variable of type PImage
img2 = None

mouse_pos = []
currentposf = ()
currentposs = ()

def setup():
    file = openfile()
    global img
    global img2
    # Make a new instance of a PImage by loading an image file
    img = load_image("spacewalk.jpg")
    img2 = load_image("spacewalk.jpg")
    size(img.width, img.height)


def draw():
    global mouse_pos
    global currentposf
    global currentposs

    background(img)
    # Draw the image to the screen at coordinate (0,0)
    # image(img, (0, 0))

    if mouse_is_pressed:
        # Append mouse position
        mouse_pos.append((mouse_x, mouse_y))
    elif len(mouse_pos) > 0:
        currentposf = mouse_pos[0]
        currentposs = mouse_pos[len(mouse_pos) - 1]

        minx = 0
        maxx = 0
        miny = 0
        maxy = 0
        if currentposf[0] < currentposs[0]:
            minx = int(currentposf[0])
            maxx = int(currentposs[0])
        else:
            minx = int(currentposs[0])
            maxx = int(currentposf[0])
        if currentposf[1] < currentposs[1]:
            miny = int(currentposf[1])
            maxy = int(currentposs[1])
        else:
            miny = int(currentposs[1])
            maxy = int(currentposf[1])

        ratio = scaling_ratio(minx, maxx, miny, maxy)

        # Tints the image , second argument is opacity
        # 3 arguments will range RGB brightness
        # 4 arguments will be RGB then tint
        # range is 0-255
        tint(255, 0, 0, 255)
        # print((int((maxx - minx) * ratio), int((maxy - miny) * ratio)))
        image(img2[minx:maxx, miny:maxy], (img.width/2, 0), (int((maxx - minx) * ratio), int((maxy - miny) * ratio)))


def scaling_ratio(minx, maxx, miny, maxy):
    x_scaling = ( img.width/2 ) / ( maxx - minx)
    y_scaling = ( img.height) / (maxy - miny)
    return min(x_scaling, y_scaling)


def openfile():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


if __name__ == '__main__':
    run()