import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread("../image_sources/Noisy_Squares.tif", cv2.IMREAD_GRAYSCALE)

# Definir un kernel cuadrado de 13x13 para la erosión
kernel_size = 13
kernel = np.ones((kernel_size, kernel_size), np.uint8)

# Aplicar la erosión a la imagen
erosion = cv2.erode(image, kernel, iterations=1)

cv2.imwrite('results/eroded.jpg', erosion)

# Realizar la dilatación con el mismo elemento estructurante
dilation = cv2.dilate(erosion, kernel, iterations=1)

cv2.imwrite('results/dilated.jpg', dilation)