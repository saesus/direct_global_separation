import numpy as np
import cv2

import sys
import os.path
from argparse import ArgumentParser, FileType

# Deprecated imports
# from PIL import Image
# import time

videos = []
videos_list = []


def main():
    # videos_list = ['Curtain.mpg', 'Nook.mpg', 'Red_Leaves.mpg', 'ShowerCurtain.mpg']
    list(map(direct_global_separation, videos, videos_list))


# Loads the videos and their names into their respective lists
def load_videos(args):
    global videos
    global videos_list

    for f in args.file:
        videos_list.append(f.name)
    for v in videos_list:
        videos.append(cv2.VideoCapture(v))


def direct_global_separation(video, video_name):
    w = int(video.get(3))
    h = int(video.get(4))

    frames_list = []

    ret, frame = video.read()

    frames_list.append(frame)

    while ret:
        ret, frame = video.read()
        if ret:
            frames_list.append(frame)
        else:
            break

    lmax = np.maximum.reduce(frames_list)
    lmin = np.minimum.reduce(frames_list)

    # Lmax = Ld +βLg
    # Lmin = βLg
    # α = 1

    beta = 0.75
    lg = lmin / beta
    ld = lmax - (beta * lg)

    cv2.imwrite('images/d-' + os.path.splitext(video_name)[0] + '.png', ld)
    cv2.imwrite('images/g-' + os.path.splitext(video_name)[0] + '.png', lg)

    # end_time = time.time()


# Checks if the file exists, else errors out
def check_file(parser, fn):
    try:
        open(fn, 'r')
        videos_list.append(fn)
    except:
        parser.error('The file %s does not exist' % fn)
        return 0


if __name__ == '__main__':
    parser = ArgumentParser(description='Separates direct and global lighting in a scene given an occluder')
    parser.add_argument('file', help="input file", metavar='', type=FileType('r'), nargs='+')
    args = parser.parse_args()
    load_videos(args)

    main()
