from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from skimage.util import random_noise
import matplotlib

matplotlib.use('TkAgg')

# Leer la imagen con PIL
image = cv2.imread('results/contrast1.5.jpg')
image = np.array(image)

# Filtrar con filtro pasa bajos (average)
kernel = np.ones((3, 3)) / 9
filtered_image = convolve2d(image, kernel, mode='same', boundary='wrap')

cv2.imwrite('./results/filtered_image.jpg', filtered_image)

# Filtrar con filtro mediana (tamaño del kernel 3x3)
median_filtered_image = cv2.medianBlur(image, ksize=3)

cv2.imwrite('./results/median_filtered_image.jpg', filtered_image)
