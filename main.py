from PIL import Image
import numpy as np
import cv2

videos = []


def main():
    load_videos()
    direct_global_separation(videos[0])


def load_videos():
    global videos
    # videos.append(cv2.VideoCapture('Curtain.mpg'))
    videos.append(cv2.VideoCapture('Nook.mpg'))
    videos.append(cv2.VideoCapture('Red_Leaves.mpg'))
    videos.append(cv2.VideoCapture('ShowerCurtain.mpg'))


def direct_global_separation(video):
    count = 0
    w = int(video.get(3))
    h = int(video.get(4))

    ret, frame = video.read()
    lmax = np.copy(frame)
    lmin = np.copy(frame)

    frames_counter = 1

    while ret:
        ret, frame = video.read()
        frames_counter = frames_counter + 1
        if ret:
            for color_channel in range(0,3):
                for x in range(len(frame)):
                    for y in range(len(frame[0])):
                        if frame[x][y][color_channel] > lmax[x][y][color_channel]:
                            lmax[x][y][color_channel] = frame[x][y][color_channel]
                        elif frame[x][y][color_channel] < lmin[x][y][color_channel]:
                            lmin[x][y][color_channel] = frame[x][y][color_channel]
        else:
            break

    # Lmax = Ld +βLg
    # Lmin = βLg
    # α = 1

    beta = 0.5
    lg = lmin / beta
    ld = lmax - ( beta * lg )

    cv2.imwrite('05direct.png', ld)
    cv2.imwrite('05global.png', lg)

if __name__ == '__main__':
    main()