from utils import *


def main():
    direct = cv2.imread('05direct.png')
    direct2 = cv2.imread('05direct2.png')

    globall = cv2.imread('05global.png')
    globall2 = cv2.imread('05global2.png')
    print(compare_images(direct, direct2), compare_images(globall, globall2))

def test_minmax():
    lmax = cv2.imread('blackandwhite.jpeg')
    lmin = np.copy(lmax)
    lmax_g = cv2.cvtColor(lmax, cv2.COLOR_RGB2GRAY)
    lmin_g = cv2.cvtColor(lmin, cv2.COLOR_RGB2GRAY)
    frame = cv2.imread('whiteandblack.jpeg')

    cv2.imshow('Elephant', lmax)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

    lmax, lmin = get_minmax(frame, lmax, lmin, lmax_g, lmin_g)

    cv2.imshow('lmax', lmax)
    cv2.waitKey(0)
    cv2.imshow('lmin', lmin)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
