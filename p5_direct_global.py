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

    no_loop()


def draw():
    global mouse_pos
    global currentposf
    global currentposs

    global height
    global width
    global gradient_height

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


def mouse_pressed():
    # Relighting - No Adjustment
    if mouse_y < height:
        if mouse_x < width:
            result = processing.combine_images(ld, lg)
            combined_image = processing.convert_cv2_image(result.astype('uint8'), 'BGR')
            image(combined_image, (width * 3, 0),
                  (width, height))
        # Relighting - Red tint on direct
        elif mouse_x < (width * 2):
            red_img = np.full((len(ld), len(ld[0]), 3), (0, 0, 255), np.uint8)
            fused_img = cv2.addWeighted(ld, 0.8, red_img, 0.2, 0)
            result = processing.combine_images(fused_img, lg)
            combined_image = processing.convert_cv2_image(result.astype('uint8'), 'BGR')
            image(combined_image, (width * 3, 0),
                  (width, height))
        # Relighting - Red tint on global
        else:
            red_img = np.full((len(ld), len(ld[0]), 3), (0, 0, 255), np.uint8)
            fused_img = cv2.addWeighted(lg, 0.8, red_img, 0.2, 0)
            result = processing.combine_images(fused_img, ld)
            combined_image = processing.convert_cv2_image(result.astype('uint8'), 'BGR')
            image(combined_image, (width * 3, 0),
                  (width, height))
    else:
        # Recolor based on the gradients
        if mouse_y < height + gradient_height:

        if mouse_y < height + (2 * gradient_height):
        if mouse_y < height + (3 * gradient_height):
        if mouse_y < height + (4 * gradient_height):


def openfile():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


if __name__ == '__main__':
    run()