import cv2

def get_minmax(frame, lmax, lmin, lmax_g, lmin_g):
    frame_g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for x in range(len(frame_g)):
        for y in range(len(frame_g[0])):
            if frame_g[x][y] > lmax_g[x][y]:
                lmax[x][y] = frame[x][y]
            elif frame_g[x][y] < lmin_g[x][y]:
                lmin[x][y] = frame[x][y]



    return lmax, lmin