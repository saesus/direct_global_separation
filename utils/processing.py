import cv2
import numpy as np
from PIL import Image
from p5 import PImage


def combine_images(img1, img2):
    """Combines direct and global light
    Adds together direct and global light images
    :param img1, img2: Images to combine
    :type class:numpy.ndarray
    :returns: Combined image
    :rtype: :class:`numpy.ndarray`
    """
    img1 = img1.astype('uint16')
    img2 = img2.astype('uint16')

    img = cv2.add(img1, img2)
    norm_img = img.astype(np.float64) / img.max()  # normalize the data to 0 - 1
    norm_img = 255 * norm_img # Now scale by 255

    img = norm_img.astype(np.uint8)

    return img


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


def direct_global_separation(video, video_name, width, height):
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

    frames_list.append(cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA))
    # frames_counter = 1

    while ret:
        ret, frame = video.read()
        # frames_counter = frames_counter + 1
        if ret:
            frames_list.append(cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA))
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


def scaling_ratio(frame_size, height, width):
    """Returns a ratio to scale an image to 255 pixels
    wide/high
    :param video: The incoming cv2 video to be converted
    to a direct and a global cv2 image
    :type video: cv2.VideoCapture
    :returns: A pair of cv2 images
    :rtype: :class:`numpy.ndarray`
    """
    return frame_size/max(height, width)


# Creates 4 Images - RGB and Tone
def generate_color(width, height):
    """Returns a list of gradients - RGB and intensity
    :param width: Width of the full image
    height: height of the gradient arrays
    :type video: cv2.VideoCapture
    :returns: A list of cv2 images
    :rtype: :class:`numpy.ndarray`
    """
    r = np.zeros((height, width, 3), np.uint8)
    g = np.zeros((height, width, 3), np.uint8)
    b = np.zeros((height, width, 3), np.uint8)
    intensity = np.zeros((height, width, 3), np.uint8)

    for pos in range(width - 1):
        r[:,pos,0] = 255*(pos/width)
        r[:,pos,1] = 255*(pos/width)
        r[:,pos,2] = 255
    for pos in range(width - 1):
        g[:,pos,0] = 255*(pos/width)
        g[:,pos,1] = 255
        g[:,pos,2] = 255*(pos/width)
    for pos in range(width - 1):
        b[:,pos,0] = 255
        b[:,pos,1] = 255*(pos/width)
        b[:,pos,2] = 255*(pos/width)
    for pos in range(width - 1):
        intensity[:,pos,0] = 255*(pos/width)
        intensity[:,pos,1] = 255*(pos/width)
        intensity[:,pos,2] = 255*(pos/width)

    rgb = [convert_cv2_image(r, 'BGR'), convert_cv2_image(g, 'BGR'), convert_cv2_image(b, 'BGR'), convert_cv2_image(intensity, 'BGR')]
    return rgb

