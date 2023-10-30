import cv2
import numpy as np

image = cv2.imread('a.png', 0)


kernel = np.array([[1, 1, 1],
                  [1, 1, 1],
                  [1, 1, 1]], dtype=np.uint8)

thickened_image = cv2.dilate(image, kernel, iterations=1)

cv2.imshow('Imagen Original', image)
cv2.imshow('Imagen con Thickening', thickened_image)
cv2.waitKey(0)
cv2.destroyAllWindows()