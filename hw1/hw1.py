
from scipy import misc
import numpy as np

def upside_down(image):
    copy = np.zeros_like(image)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            copy[y, x] = image[image.shape[0] - y - 1, x]

    return copy


def right_side_left(image):
    copy = np.zeros_like(image)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            copy[y, x] = image[y, image.shape[1] - x - 1]

    return copy


def diag_mirror(image):
    copy = np.zeros((image.shape[1], image.shape[0]))
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            copy[y, x] = image[x, y]
            
    return copy


lena = misc.imread('./lena.bmp')

misc.imsave('upside_down.jpg', upside_down(lena))
misc.imsave('right_side_left.jpg', right_side_left(lena))
misc.imsave('diag_mirror.jpg', diag_mirror(lena))