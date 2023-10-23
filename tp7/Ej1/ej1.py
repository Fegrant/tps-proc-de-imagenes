import cv2
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')
import numpy as np

img2 = cv2.imread("../image_sources/Broken_Text.tif", 0)
p, q = img2.shape

# Define new image to store the pixels of dilated image
imgDilate = np.zeros((p, q), dtype=np.uint8)

# Define the structuring element
SED = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
constant1 = 1

# Dilation operation
for i in range(constant1, p - constant1):
    for j in range(constant1, q - constant1):
        temp = img2[i - constant1:i + constant1 + 1, j - constant1:j + constant1 + 1]
        product = temp * SED
        imgDilate[i, j] = np.max(product)
plt.imshow(imgDilate, cmap="gray")

cv2.imwrite("results/Dilated.png", imgDilate)
