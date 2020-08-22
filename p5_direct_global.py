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

size_mult = 100

def setup():
    global img

    global dir_img, glo_img

    global ld, lg

    global video_name
    global video
    global size_mult

    video_name = openfile()
    video = cv2.VideoCapture(video_name)

    video.set(1, 1)
    ret, init_frame = video.read()

    if(len(init_frame)) > 1000:
        size_mult = 50
        width = int(init_frame.shape[1] * size_mult / 100)
        height = int(init_frame.shape[0] * size_mult / 100)
        init_frame = cv2.resize(init_frame, (width, height), interpolation = cv2.INTER_AREA)

    blank_image = np.zeros((len(init_frame), len(init_frame[0]), 3), np.uint8)
    # Stack images horizontally
    for x in range(3):
        init_frame = np.concatenate((init_frame, blank_image), axis=1)

    # buttons = np.zeros((100, len(init_frame[0]), 3), np.uint8)
    # init_frame = np.concatenate((init_frame, buttons), axis=0)

    img = convert_cv2_image(init_frame, 'BGR')
    size(img.width, img.height)

    lg, ld = direct_global_separation(video, video_name)
    lg = lg.astype('uint8')
    ld = ld.astype('uint8')
    dir_img = convert_cv2_image(ld, 'BGR')
    glo_img = convert_cv2_image(lg, 'BGR')

    no_loop()


def draw():
    global mouse_pos
    global currentposf
    global currentposs

    global height
    global width

    background(img)
    # image(img, (0, 0))

    width = int(dir_img.width * size_mult / 100)
    height = int(dir_img.height * size_mult / 100)
    image(dir_img, (width, 0),
          (width, height))
    image(glo_img, (width * 2, 0),
          (width, height))


def mouse_pressed():
    # Relighting - No Adjustment
    if mouse_x < width:
        result = processing.combine_images(ld, lg)
        combined_image = convert_cv2_image(result.astype('uint8'), 'BGR')
        image(combined_image, (width * 3, 0),
              (width, height))
    # Relighting - Red tint on direct
    elif mouse_x < (width * 2):
        red_img = np.full((len(ld), len(ld[0]), 3), (0, 0, 255), np.uint8)
        fused_img = cv2.addWeighted(ld, 0.8, red_img, 0.2, 0)
        result = processing.combine_images(fused_img, lg)
        combined_image = convert_cv2_image(result.astype('uint8'), 'BGR')
        image(combined_image, (width * 3, 0),
              (width, height))
    # Relighting - Red tint on global
    else:
        red_img = np.full((len(ld), len(ld[0]), 3), (0, 0, 255), np.uint8)
        fused_img = cv2.addWeighted(lg, 0.8, red_img, 0.2, 0)
        result = processing.combine_images(fused_img, ld)
        combined_image = convert_cv2_image(result.astype('uint8'), 'BGR')
        image(combined_image, (width * 3, 0),
              (width, height))


def convert_cv2_image(cv2_image, colorspace):
    """Convert a cv2 image to a PImage
    Loads a cv2 image into a variable of type PImage.
    The incoming image must be in the RGB colorspace.
    :param cv2_image: The incoming numpy array to be converted into a
    PImage
    :type cv2_image: numpy.ndarray
    :returns: An :class:`p5.PImage` instance with the given image data
    :rtype: :class:`p5.PImage`
    """

    w = int(cv2_image.shape[1])
    h = int(cv2_image.shape[0])

    if colorspace == 'BGR':
        cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        colorspace = 'RGB'

    c_image = Image.fromarray(cv2_image.astype('uint8'), colorspace)

    temp_img = PImage(w, h)
    temp_img._img = c_image
    return temp_img


def direct_global_separation(video, video_name):
    """Separates direct and global light
    Loads a cv2 video into a list of frame images.
    :param video: The incoming cv2 video to be converted
    to a direct and a global cv2 image
    :type video: cv2.VideoCapture
    :returns: A pair of cv2 images
    :rtype: :class:`numpy.ndarray`
    """
    # start_time = time.time()
    w = int(video.get(3))
    h = int(video.get(4))

    frames_list = []

    ret, frame = video.read()

    frames_list.append(frame)
    # frames_counter = 1

    while ret:
        ret, frame = video.read()
        # frames_counter = frames_counter + 1
        if ret:
            frames_list.append(frame)
        else:
            break

    # frames_list = frames_list[0:int(len(frames_list)/2)]
    lmax = np.maximum.reduce(frames_list)
    lmin = np.minimum.reduce(frames_list)

    # Lmax = Ld +βLg
    # Lmin = βLg
    # α = 1

    beta = 0.75
    lg = lmin / beta
    ld = lmax - ( beta * lg )

    return(ld, lg)


def openfile():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


if __name__ == '__main__':
    run()