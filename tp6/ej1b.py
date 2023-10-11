import cv2
import numpy as np

import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D  # noqa
from matplotlib.colors import hsv_to_rgb

bird = cv2.imread("imagenes/bird.jpg")

img_blur = cv2.blur(bird, ksize=(5, 5))
img_median = cv2.medianBlur(img_blur, 5)
img_gaussian = cv2.GaussianBlur(img_median, (5, 5), 0)
img2 = cv2.bilateralFilter(img_gaussian, 9, 75, 75)

img_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
H, S, V = cv2.split(img_hsv)

low = np.array([50, 0, 0])
high = np.array([120, 255, 255])
mask = cv2.inRange(img_hsv, low, high)

res = cv2.bitwise_and(bird, bird, mask=mask)
s = np.hstack((bird, res))
s = cv2.pyrDown(s)

cv2.imwrite("results/cut_Bird.jpg", s)
