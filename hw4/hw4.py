import numpy as np
import scipy.misc as misc
import matplotlib.pyplot as plt
disc_se = np.array([[False, True, False], [True, True, True], [False, True, False]], dtype=np.bool)

def dilation(binary_img, structure_element=disc_se):
    dialated = np.zeros_like(binary_img)
    cent_y = structure_element.shape[0] // 2
    cent_x = structure_element.shape[1] // 2

    for y in range(binary_img.shape[0]):
        for x in range(binary_img.shape[1]):

            if binary_img[y, x]:
                for sy in range(structure_element.shape[0]):
                    for sx in range(structure_element.shape[1]):
                        if structure_element[sy, sx]:
                            safe_set(dialated, y + sy - cent_y, x + sx - cent_x, 255)

    return dialated

def erosion(binary_img, structure_element=disc_se):
    erosed = np.zeros_like(binary_img)
    cent_y = structure_element.shape[0] // 2
    cent_x = structure_element.shape[1] // 2

    for y in range(binary_img.shape[0]):
        for x in range(binary_img.shape[1]):

            if binary_img[y, x] and erosion_check(binary_img, y, x, structure_element, cent_y, cent_x):
                erosed[y, x] = 255

    return erosed



def opening(binary_img, structure_element=disc_se):
    dilation(erosion(binary_img,structure_element), structure_element)

def closing(binary_img, structure_element=disc_se):
    erosion(dilation(binary_img, structure_element), structure_element)

def hit_and_miss_transform(binary_img, j, k):
    return intersection(erosion(binary_img, j), erosion(complement(binary_img), k))

def complement(binary_img):
    comp = np.zeros_like(binary_img, np.uint8)
    for y in range(binary_img.shape[0]):
        for x in range(binary_img.shape[1]):
            comp[y, x] = 255 - binary_img[y, x]
    return comp

def intersection(img1, img2):
    intersect = np.zeros_like(img1, np.uint8)
    for y in range(img1.shape[0]):
        for x in range(img1.shape[1]):
            intersect[y, x] = 255 if img1[y, x] and img2[y, x] else 0
    return intersect

def erosion_check(binary_img, y, x, structure_element, cent_y, cent_x):
    for sy in range(structure_element.shape[0]):
        for sx in range(structure_element.shape[1]):
            if structure_element[sy, sx] and not safe_get(binary_img, y + sy - cent_y, x + sx - cent_x):
                return False
    return True

def safe_set(img, y, x, val):
    if 0 <= y < img.shape[0] and 0 <= x < img.shape[1]:
        img[y, x] = val

def safe_get(img, y, x):
    if 0 <= y < img.shape[0] and 0 <= x < img.shape[1]:
        return img[y, x]
    return 0

def threshold(image, t=128):
    thresholded_img = np.zeros_like(image)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] >= t:
                thresholded_img[y, x] = 255

    return thresholded_img


if __name__ == '__main__':
    lena = misc.imread('lena.bmp')
    thresholded_lena = threshold(lena)
    dilated_lena = erosion(thresholded_lena)

    misc.imsave('dilated.jpg', dilated_lena)