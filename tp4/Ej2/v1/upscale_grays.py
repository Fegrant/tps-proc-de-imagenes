import cv2
import numpy as np
import os

from matplotlib import pyplot as plt

if not os.path.exists('results'):
    os.makedirs('results')

low_threshold = 70
high_threshold = 110

slicing_result = np.copy(imagen)

for i in range(len(slicing_result)):
    for j in range(len(slicing_result[0])):
        if slicing_result[i,j] >= low_threshold and slicing_result[i,j] <= high_threshold:
            slicing_result[i,j] *= 0.7

slicing_result = np.uint8(slicing_result)

cv2.imwrite('results/original_image.jpg', imagen)
cv2.imwrite('results/upscaled_image.jpg', slicing_result)