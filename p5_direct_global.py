import numpy as np
import cv2

from p5 import *
from PIL import Image
from tkinter import filedialog
import tkinter as tk
from utils import processing

# Global Variables

img = None # Declare a variable of type PImage
dir_img = None
glo_img = None

ld = None
lg = None

global video_name
global video

global height
global width
frame_size = 640

global gradient_height

global filter_red
global filter_green
global filter_blue
global filter_int
global filter_img

global red_elipse
global green_elipse
global blue_elipse
global int_elipse

comb = None

size_mult = 1

def setup():
    global img

    global dir_img, glo_img

    global ld, lg

    global video_name
    global video
    global size_mult

    global height
    global width

    video_name = openfile()
    video = cv2.VideoCapture(video_name)

    video.set(1, 1)
    ret, init_frame = video.read()
    if(len(init_frame) or len(init_frame[0])) > frame_size:
        size_mult = processing.scaling_ratio(frame_size, len(init_frame),len(init_frame[0]))
        width = int(init_frame.shape[1] * size_mult)
        height = int(init_frame.shape[0] * size_mult)
        print(width, height)
        init_frame = cv2.resize(init_frame, (width, height), interpolation = cv2.INTER_AREA)
    else:
        width = int(init_frame.shape[1] * size_mult)
        height = int(init_frame.shape[0] * size_mult)

    blank_image = np.zeros((len(init_frame), len(init_frame[0]), 3), np.uint8)
    # Stack images horizontally
    for x in range(3):
        init_frame = np.concatenate((init_frame, blank_image), axis=1)

    buttons = np.zeros((480, len(init_frame[0]), 3), np.uint8)
    init_frame = np.concatenate((init_frame, buttons), axis=0)

    img = processing.convert_cv2_image(init_frame, 'BGR')
    size(img.width, img.height)

    lg, ld = processing.direct_global_separation(video, video_name, width, height)
    lg = lg.astype('uint8')
    ld = ld.astype('uint8')
    dir_img = processing.convert_cv2_image(ld, 'BGR')
    glo_img = processing.convert_cv2_image(lg, 'BGR')

    global red_elipse
    global green_elipse
    global blue_elipse
    global int_elipse

    red_elipse = None
    green_elipse = None
    blue_elipse = None
    int_elipse = None

    init_filter()
    no_loop()


def draw():
    global comb

    global mouse_pos
    global currentposf
    global currentposs

    global height
    global width
    global gradient_height

    global red_elipse
    global green_elipse
    global blue_elipse
    global int_elipse

    background(img)
    image(dir_img, (width, 0),
          (width, height))
    image(glo_img, (width * 2, 0),
          (width, height))

    gradient_height = 120
    gradients = processing.generate_color(int(width * 4), gradient_height)
    image(gradients[0], (0, height))
    image(gradients[1], (0, height + gradient_height))
    image(gradients[2], (0, height + (gradient_height * 2)))
    image(gradients[3], (0, height + (gradient_height * 3)))

    # Combines the images for the resultant image based on user selection
    if comb:
        if comb == 1:
            result = processing.combine_images(ld, lg)
            combined_image = processing.convert_cv2_image(result.astype('uint8'), 'BGR')
            image(combined_image, (width * 3, 0),
                  (width, height))
        elif comb == 2:
            result = processing.combine_images(generate_filtered_image(ld), lg)
            combined_image = processing.convert_cv2_image(result.astype('uint8'), 'BGR')
            image(combined_image, (width * 3, 0),
                  (width, height))
        else:
            result = processing.combine_images(ld, generate_filtered_image(lg))
            combined_image = processing.convert_cv2_image(result.astype('uint8'), 'BGR')
            image(combined_image, (width * 3, 0),
                  (width, height))

    # Draws circles where the user has clicked on each of the gradients
    if red_elipse:
        ellipse((red_elipse[0], red_elipse[1]), 25, 25)
    if green_elipse:
        ellipse((green_elipse[0], green_elipse[1]), 25, 25)
    if blue_elipse:
        ellipse((blue_elipse[0], blue_elipse[1]), 25, 25)
    if int_elipse:
        ellipse((int_elipse[0], int_elipse[1]), 25, 25)

def mouse_pressed():
    global comb

    global filter_red
    global filter_green
    global filter_blue
    global filter_int
    global filter_img

    global red_elipse
    global green_elipse
    global blue_elipse
    global int_elipse

    if mouse_y < height:
        # Relighting - No Adjustment
        if mouse_x < width:
            comb = 1
            draw()
        # Relighting - Red tint on direct
        elif mouse_x < (width * 2):
            comb = 2
            draw()
        # Relighting - Red tint on global
        else:
            comb = 3
            draw()
    else:
        # Recolor based on the gradients
        if mouse_y < height + gradient_height:
            filter_red = 255 * (mouse_x/int(width * 4))
            red_elipse = [mouse_x, mouse_y]
            print(filter_red)
            draw()
        elif mouse_y < height + (2 * gradient_height):
            filter_green = 255 * (mouse_x / int(width * 4))
            green_elipse = [mouse_x, mouse_y]
            print(filter_green)
            draw()
        elif mouse_y < height + (3 * gradient_height):
            filter_blue = 255 * (mouse_x / int(width * 4))
            blue_elipse = [mouse_x, mouse_y]
            print(filter_blue)
            draw()
        elif mouse_y < height + (4 * gradient_height):
            filter_int = 1 - (mouse_x / int(width * 4))
            int_elipse = [mouse_x, mouse_y]
            print(filter_int)
            draw()

def generate_filtered_image(image):
    global filter_red
    global filter_green
    global filter_blue
    global filter_int
    global filter_img

    # Inits a filter image with no mixing
    filter_img = np.full((len(ld), len(ld[0]), 3), (filter_red, filter_green, filter_blue), np.uint8)
    fused_img = cv2.addWeighted(image, (1 - filter_int), filter_img, filter_int, 0)

    return fused_img


def init_filter():
    global filter_red
    global filter_green
    global filter_blue
    global filter_int
    global filter_img

    filter_red = 0
    filter_green = 0
    filter_blue = 0
    filter_int = 0.2
    filter_img = np.full((len(ld), len(ld[0]), 3), (filter_red, filter_green, filter_blue), np.uint8)


def openfile():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


if __name__ == '__main__':
    run()