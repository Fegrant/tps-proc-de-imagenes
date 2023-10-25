import cv2
import numpy as np
import os

results_dir = 'results/'

if not os.path.exists(results_dir):
    os.makedirs(results_dir)

image = cv2.imread('../image_sources/Lincoln from penny.tif', cv2.IMREAD_GRAYSCALE)

kernel_size = 3
kernel = np.ones((kernel_size, kernel_size), np.uint8)
eroded_image = cv2.erode(image, kernel, iterations=1)

edge_image = cv2.absdiff(image, eroded_image)

cv2.imwrite(results_dir + 'original.jpg', image)
cv2.imwrite(results_dir + 'borde.jpg', edge_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
