from utils import *


def main():
    img1 = cv2.imread('d-eggs_tomatoes.png')
    img2 = cv2.imread('g-eggs_tomatoes.png')

    # Red tinted image, .8 to .2 ratio of adding
    # https://amehta.github.io/posts/2019/09/create-and-apply-simple-filters-to-an-image-using-opencv-and-python/
    red_img = np.full((len(img1), len(img1[0]), 3), (0, 0, 255), np.uint8)
    fused_img = cv2.addWeighted(img1, 0.8, red_img, 0.2, 0)

    result = combine_images(fused_img, img2)
    print(result[0][0], np.amax(result))
    cv2.imwrite('testcombine.png', result)


def minmax_t1():
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
