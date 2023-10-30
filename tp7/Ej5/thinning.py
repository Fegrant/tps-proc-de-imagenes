import numpy as np
import cv2
from skimage.morphology import skeletonize
from skimage.util import invert

# Cargar la imagen en escala de grises
image = cv2.imread("a.png", cv2.IMREAD_GRAYSCALE)

# Binarizar la imagen
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

# Realizar el adelgazamiento en la imagen binarizada
thinned_image = skeletonize(binary_image)

# Guardar la imagen adelgazada
cv2.imwrite('imagen_adelgazada.jpg', thinned_image.astype(np.uint8) * 255)

# Mostrar la imagen original y la imagen adelgazada (solo para fines de visualización)
cv2.imshow('Imagen Original', image)
cv2.imshow('Imagen Adelgazada', thinned_image.astype(np.uint8) * 255)
cv2.waitKey(0)
cv2.destroyAllWindows()