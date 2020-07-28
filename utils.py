import cv2
import numpy as np


def get_minmax(frame, lmax, lmin, lmax_g, lmin_g):
    frame_g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for x in range(len(frame_g)):
        for y in range(len(frame_g[0])):
            if frame_g[x][y] > lmax_g[x][y]:
                lmax[x][y] = frame[x][y]
            elif frame_g[x][y] < lmin_g[x][y]:
                lmin[x][y] = frame[x][y]



    return lmax, lmin


def display_image(image):
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def compare_images(image1, image2):
    if np.array_equal(image1, image2):
        return True
    return False