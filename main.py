from PIL import Image
import numpy as np
import cv2
import time

videos = []


def main():
    load_videos()
    direct_global_separation2(videos[0])


def load_videos():
    global videos
    # videos.append(cv2.VideoCapture('Curtain.mpg'))
    videos.append(cv2.VideoCapture('Nook.mpg'))
    videos.append(cv2.VideoCapture('Red_Leaves.mpg'))
    videos.append(cv2.VideoCapture('ShowerCurtain.mpg'))


def direct_global_separation2(video):
    start_time = time.time()
    count = 0
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

    lmax = np.maximum.reduce(frames_list)
    lmin = np.minimum.reduce(frames_list)

    # Lmax = Ld +βLg
    # Lmin = βLg
    # α = 1

    beta = 0.5
    lg = lmin / beta
    ld = lmax - ( beta * lg )

    cv2.imwrite('05direct2.png', ld)
    cv2.imwrite('05global2.png', lg)

    end_time = time.time()
    print('runtime:', end_time - start_time)

if __name__ == '__main__':
    main()