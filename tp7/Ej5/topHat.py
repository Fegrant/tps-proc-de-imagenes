import cv2
import numpy as np

image = cv2.imread('a.png', 0)

kernel = np.ones((2, 2), np.uint8)

# Aplica la operación de Top-Hat
tophat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)

# Muestra la imagen original y el resultado Top-Hat
cv2.imshow('Imagen Original', image)
cv2.imshow('Top-Hat', tophat)
cv2.waitKey(0)
cv2.destroyAllWindows()