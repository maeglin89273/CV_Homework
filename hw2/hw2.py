

from scipy.misc import imread, imsave
import numpy as np

import matplotlib.pyplot as plt

def threshold(image, t=128):
    thresholded_img = np.zeros_like(image)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] >= t:
                thresholded_img[y, x] = 255

    plt.imshow(thresholded_img, cmap='gray')
    plt.show()
    return thresholded_img

def histogram(image):
    statistic = np.zeros(256)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            statistic[image[y, x]] += 1

    plt.bar(range(0, 256), statistic)
    plt.show()
    return statistic

def connected_components(image):
    pass

if __name__ == '__main__':
    lena = imread('lena.bmp')

    threshold(lena)
    histogram(lena)

    connected_components(lena)