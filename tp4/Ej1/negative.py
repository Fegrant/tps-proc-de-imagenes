import cv2
import os

if not os.path.exists('results/a'):
    os.makedirs('results/a')

imagen = cv2.imread('../image_sources/lena_gray.tif', cv2.IMREAD_GRAYSCALE)

negative = 255 - imagen

cv2.imwrite('results/a/original.png', imagen)
cv2.imwrite('results/a/negative.png', negative)