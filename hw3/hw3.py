from scipy import misc
import numpy as np

def histogram_equalization(image):
    s = [0] * 256
    pdf = [0] * 256
    copy = np.zeros_like(image)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            pdf[image[y, x]] += 1

    N = image.size
    sum_j_k = 0
    for k, pixel_num in enumerate(pdf):
        sum_j_k += pixel_num
        s[k] = np.uint8(255 * (sum_j_k / N))

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            copy[y, x] = s[image[y, x]]

    return copy


lena = misc.imread('./lena.bmp')
lena = (lena / 3).astype('uint8')
misc.imsave('lena3.jpg', lena)

eq_lena = histogram_equalization(lena)
misc.imsave('eq_lena.jpg', eq_lena)

