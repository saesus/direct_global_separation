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
    lmax_g = cv2.cvtColor(lmax, cv2.COLOR_BGR2GRAY)
    lmin = np.copy(frame)
    lmin_g = cv2.cvtColor(lmin, cv2.COLOR_BGR2GRAY)

    print(len(lmax_g), len(lmax_g[0]))

    frames_counter = 1

    while ret:
        ret, frame = video.read()
        frames_counter = frames_counter + 1
        if ret:
            frame_g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #for color_channel in range(0,3):
            for x in range(len(frame_g)):
                for y in range(len(frame_g[0])):
                    if frame_g[x][y] > lmax_g[x][y]:
                        lmax_g[x][y] = frame_g[x][y]
                    elif frame_g[x][y] < lmin_g[x][y]:
                        lmin_g[x][y] = frame_g[x][y]
        else:
            break
        '''
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        '''

    # Calculate Ld and Lg from Lmax and Lmin at the end

    print("Number of frames in the video: ", frames_counter)
    video.release()
    cv2.destroyAllWindows()

    cv2.imshow('max', lmax_g)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imshow('min', lmin_g)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite('max gray.png',  lmax_g)
    cv2.imwrite('min gray.png', lmin_g)
    # Lmax = Ld + Lg
    # Lmin = Lg
    # Lmax = Ld +βLg
    # Lmin = βLg
    # α = 1

    # How to calculate max brightness for rgb image


if __name__ == '__main__':
    main()