#laplaciano


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from scipy.fft import fft2
from scipy.ndimage import gaussian_filter
from skimage.filters import unsharp_mask
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
import cv2
import numpy as np


#Lapplaciano tp3 TARDA 20 MINUTOS
image = cv2.imread('homomorphicColor2.png')


# Definir las máscaras
normal_mask = np.array([[1, 1, 1],
                        [1, -8, 1],
                        [1, 1, 1]], dtype=np.float32)

borders_mask = np.array([[-1, -1, -1],
                         [-1, 9, -1],
                         [-1, -1, -1]], dtype=np.float32)

height, width, channels = image.shape

# Inicializar las matrices laplacianas por canal
normal_laplacian = np.zeros((height, width, channels), dtype=np.float32)
borders_laplacian = np.zeros((height, width, channels), dtype=np.float32)

# Aplicar las máscaras por canal
for i in range(1, height - 1):
    for j in range(1, width - 1):
        region = image[i-1:i+2, j-1:j+2, :]
        for channel in range(channels):
            normal_value = np.sum(region[:, :, channel] * normal_mask)
            normal_laplacian[i, j, channel] = normal_value
            borders_value = np.sum(region[:, :, channel] * borders_mask)
            borders_laplacian[i, j, channel] = borders_value

# Aplicar el clip y cambio de escala por canal
normal_laplacian = np.clip(normal_laplacian, 0, 255).astype(np.uint8)
borders_laplacian = np.clip(borders_laplacian, 0, 255).astype(np.uint8)

normal_laplacian_scaled_down = np.clip(normal_laplacian * 0.5, 0, 255).astype(np.uint8)
normal_laplacian_scaled_up = np.clip(normal_laplacian * 1.5, 0, 255).astype(np.uint8)

# Restar el laplaciano a la imagen original por canal
image_with_normal_mask = cv2.subtract(image, normal_laplacian)
image_with_normal_mask_scaled_down = cv2.subtract(image, normal_laplacian_scaled_down)
image_with_normal_mask_scaled_up = cv2.subtract(image, normal_laplacian_scaled_up)


# Especifica las rutas de guardado para cada imagen
path_normal_laplacian = 'normal_laplacian.png'
path_borders_laplacian = 'borders_laplacian.png'
path_normal_laplacian_scaled_down = 'normal_laplacian_scaled_down.png'
path_normal_laplacian_scaled_up = 'normal_laplacian_scaled_up.png'
path_image_with_normal_mask = 'image_with_normal_mask.png'
path_image_with_normal_mask_scaled_down = 'image_with_normal_mask_scaled_down.png'
path_image_with_normal_mask_scaled_up = 'image_with_normal_mask_scaled_up.png'

# Guardar las imágenes
cv2.imwrite(path_normal_laplacian, normal_laplacian)
cv2.imwrite(path_borders_laplacian, borders_laplacian)
cv2.imwrite(path_normal_laplacian_scaled_down, normal_laplacian_scaled_down)
cv2.imwrite(path_normal_laplacian_scaled_up, normal_laplacian_scaled_up)
cv2.imwrite(path_image_with_normal_mask, image_with_normal_mask)
cv2.imwrite(path_image_with_normal_mask_scaled_down, image_with_normal_mask_scaled_down)
cv2.imwrite(path_image_with_normal_mask_scaled_up, image_with_normal_mask_scaled_up)