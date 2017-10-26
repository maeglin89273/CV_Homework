from collections import deque

from scipy.misc import imread, imsave
import numpy as np

import matplotlib.pyplot as plt

class ComponentInfo:
    def __init__(self):
        self.min_x = float('inf')
        self.min_y = float('inf')
        self.max_x = -1
        self.max_y = -1
        self.pixel_num = 0

    def update(self, y, x):
        if x < self.min_x:
            self.min_x = x

        if x > self.max_x:
            self.max_x = x

        if y < self.min_y:
            self.min_y = y

        if y > self.max_y:
            self.max_y = y

        self.pixel_num += 1


def threshold(image, t=128):
    thresholded_img = np.zeros_like(image)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] >= t:
                thresholded_img[y, x] = 255

    return thresholded_img

def histogram(image):
    statistic = np.zeros(256)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            statistic[image[y, x]] += 1

    plt.bar(range(0, 256), statistic, width=1)
    plt.savefig('histogram.jpg')
    return statistic

def connected_components(thresholded_image, connectivity=4):
    image = thresholded_image.astype('int32')
    new_label = 1
    forward_neighbor_labels = forward_neighbor_4_labels if connectivity == 4 else forward_neighbor_8_labels
    backward_neighbor_labels = backward_neighbor_4_labels if connectivity == 4 else backward_neighbor_8_labels

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] > 0:
                image[y, x] = new_label
                new_label += 1

    changed = True
    while changed:
        changed = False
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                yx_label = image[y, x]
                if yx_label > 0:
                    labels = forward_neighbor_labels(image, y, x)
                    labels.append(yx_label)
                    min_label = min(labels)
                    if min_label != yx_label:
                        image[y, x] = min_label
                        changed = True

        for y in range(image.shape[0] - 1, -1, -1):
            for x in range(image.shape[1] - 1, -1, -1):
                yx_label = image[y, x]
                if yx_label > 0:
                    labels = backward_neighbor_labels(image, y, x)
                    labels.append(yx_label)
                    min_label = min(labels)
                    if min_label != yx_label:
                        image[y, x] = min_label
                        changed = True


    return image

def forward_neighbor_4_labels(image, y, x):
    labels = []
    up_y = y - 1
    left_x = x - 1
    if up_y >= 0 and image[up_y, x]: # 'and image[up_y, x]' means 'and image[up_y, x] != 0'
        labels.append(image[up_y, x])

    if left_x >= 0 and image[y, left_x]:
        labels.append(image[y, left_x])

    return labels


def forward_neighbor_8_labels(image, y, x):
    labels = []
    up_y = y - 1
    left_x = x - 1
    if up_y >= 0 and image[up_y, x]: # 'and image[up_y, x]' means 'and image[up_y, x] != 0'
        labels.append(image[up_y, x])

    if left_x >= 0 and image[y, left_x]:
        labels.append(image[y, left_x])

    if up_y >= 0 and left_x >= 0 and image[up_y, left_x]:
        labels.append(image[up_y, left_x])

    return labels

def backward_neighbor_4_labels(image, y, x):
    labels = []
    bottom_y = y + 1
    right_x = x + 1
    if bottom_y < image.shape[0] and image[bottom_y, x]: # 'and image[up_y, x]' means 'and image[up_y, x] != 0'
        labels.append(image[bottom_y, x])

    if right_x < image.shape[1] and image[y, right_x]:
        labels.append(image[y, right_x])

    return labels



def backward_neighbor_8_labels(image, y, x):
    labels = []
    bottom_y = y + 1
    right_x = x + 1
    if bottom_y < image.shape[0] and image[bottom_y, x]:  # 'and image[up_y, x]' means 'and image[up_y, x] != 0'
        labels.append(image[bottom_y, x])

    if right_x < image.shape[1] and image[y, right_x]:
        labels.append(image[y, right_x])

    if bottom_y < image.shape[0] and right_x < image.shape[1] and image[bottom_y, right_x]:
        labels.append(image[bottom_y, right_x])

    return labels


CROSS_HALF_SIZE = 5
def box_components(img, labeled_img):
    con_comps = {}
    for y in range(labeled_img.shape[0]):
        for x in range(labeled_img.shape[1]):
            if labeled_img[y, x] > 0:
                con_comps.setdefault(labeled_img[y, x], ComponentInfo()).update(y, x)

    components = filter(lambda comp: comp.pixel_num >= 500, con_comps.values())

    boxed_img = np.copy(img)
    for comp in components:
        #draw cross
        cent_y = (comp.min_y + comp.max_y) // 2
        cent_x = (comp.min_x + comp.max_x) // 2

        for y in range(cent_y - CROSS_HALF_SIZE, cent_y + CROSS_HALF_SIZE + 1):
            if y >= 0 and y < img.shape[0]:
                boxed_img[y, cent_x] = 0 if img[y, cent_x] > 0 else 255

        for x in range(cent_x - CROSS_HALF_SIZE, cent_x + CROSS_HALF_SIZE + 1):
            if x >= 0 and x < img.shape[1]:
                boxed_img[cent_y, x] = 0 if img[cent_y, x] > 0 else 255

        # draw box
        for y in range(comp.min_y, comp.max_y + 1):
            boxed_img[y, comp.max_x] = 255
        for y in range(comp.min_y, comp.max_y + 1):
            boxed_img[y, comp.min_x] = 255

        for x in range(comp.min_x, comp.max_x + 1):
            boxed_img[comp.max_y, x] = 255

        for x in range(comp.min_x, comp.max_x + 1):
            boxed_img[comp.min_y, x] = 255

    return boxed_img

if __name__ == '__main__':
    lena = imread('lena.bmp')

    thresholded_lena = threshold(lena)
    imsave('thershold.jpg', thresholded_lena)
    histogram(lena)

    thresholded_lena = threshold(lena, t=200)
    labeled_img = connected_components(thresholded_lena)
    boxed_lena = box_components(thresholded_lena, labeled_img)

    imsave('connected_components.jpg', boxed_lena)