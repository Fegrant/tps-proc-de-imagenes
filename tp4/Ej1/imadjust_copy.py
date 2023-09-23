import cv2
import numpy as np
import os

if not os.path.exists('results/b'):
    os.makedirs('results/b')


def imadjust(image, in_limits, out_limits):
    image = (image - in_limits[0]) / (in_limits[1] - in_limits[0])
    image *= (out_limits[1] - out_limits[0]) + out_limits[0]
    image = np.clip(image, 0, 255)
    image = np.uint8(image)
    return image


imagen = cv2.imread('../image_sources/lena_gray.tif', cv2.IMREAD_GRAYSCALE)

in_limits = [0.25 * 255, 0.5 * 255]
out_limits = [0, 255]

imagen_ajustada = imadjust(imagen, in_limits, out_limits)

cv2.imwrite('results/b/original.jpg', imagen)
cv2.imwrite('results/b/ajustada.jpg', imagen_ajustada)
