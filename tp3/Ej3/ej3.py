from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from skimage.util import random_noise

# Leer la imagen con PIL
image = Image.open('../image_sources/eight.tif').convert('L')
image = np.array(image)

# Mostrar la imagen original
plt.imshow(image, cmap='gray')
plt.axis('off') 
plt.show()

# Aplicar ruido "sal y pimienta" con una probabilidad del 2%
noisy_image = random_noise(image, mode='s&p', amount=0.02)
# Convertir la imagen ruidosa a uint8
noisy_image = (noisy_image * 255).astype(np.uint8)

# Mostrar la imagen con ruido
plt.imshow(noisy_image, cmap='gray')
plt.axis('off') 
plt.show()

# Filtrar con filtro pasa bajos (average)
kernel = np.ones((3, 3)) / 9
filtered_image = convolve2d(noisy_image, kernel, mode='same', boundary='wrap')

# Mostrar la imagen filtrada
plt.imshow(filtered_image, cmap='gray')
plt.axis('off') 
plt.show()

# Filtrar con filtro mediana (tamaño del kernel 3x3)
median_filtered_image = cv2.medianBlur(noisy_image, ksize=3)

# Mostrar la imagen filtrada con filtro mediana
plt.imshow(median_filtered_image, cmap='gray')
plt.axis('off') 
plt.show()

