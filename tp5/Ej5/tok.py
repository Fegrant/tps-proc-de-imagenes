import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from scipy.optimize import minimize
import cv2
from skimage import data

# Definir el operador laplaciano en 2D (C)
laplacian_operator = np.array([[0, 1, 0],
                               [1, -4, 1],
                               [0, 1, 0]])

# Función de costo para el método de Tikhonov-Miller
def cost_function(f_hat, g, H, alpha):
    f_hat_2d = f_hat.reshape(g.shape)
    residual = np.linalg.norm(g - convolve2d(f_hat_2d, H, 'same'))**2
    regularization = alpha * np.linalg.norm(convolve2d(f_hat_2d, laplacian_operator, 'same'))**2
    return residual + regularization

# Función para restaurar la imagen usando Tikhonov-Miller con reducción de tamaño
def restore_image_tikhonov_miller(g, H, alpha, scale_factor=0.5):
    # Reducir el tamaño de la imagen
    g_small = cv2.resize(g, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    # Inicializar la imagen restaurada como una copia de la imagen observada reducida
    f_hat_small = np.copy(g_small).flatten()

    # Minimizar la función de costo para obtener la imagen restaurada reducida
    result = minimize(cost_function, f_hat_small, args=(g_small, H, alpha), method='BFGS')
    f_hat_restored_small = result.x

    # Restaurar la imagen reducida a su forma original
    f_hat_restored = f_hat_restored_small.reshape(g_small.shape)

    # Ampliar la imagen restaurada a su tamaño original
    f_hat_restored = cv2.resize(f_hat_restored, g.shape[::-1], interpolation=cv2.INTER_LINEAR)

    return f_hat_restored

# Crear una imagen de ejemplo (puedes cargar tu propia imagen observada 'g')
# En este ejemplo, utilizamos una imagen sintética
np.random.seed(0)
original_image = data.coins()
H = np.ones((5, 5)) / 25  # Kernel de degradación (filtro promedio)

# Agregar ruido gaussiano a la imagen observada 'g'
g = original_image + 0.1 * np.random.randn(*original_image.shape)

# Parámetro de regularización (ajústalo según tus necesidades)
alpha = 0.01

# Restaurar la imagen observada 'g' utilizando Tikhonov-Miller con reducción de tamaño
restored_image = restore_image_tikhonov_miller(g, H, alpha)

# Mostrar las imágenes
plt.figure(figsize=(12, 4))
plt.subplot(131)
plt.imshow(original_image, cmap='gray')
plt.title('Imagen Original')
plt.axis('off')

plt.subplot(132)
plt.imshow(g, cmap='gray')
plt.title('Imagen Observada con Ruido')
plt.axis('off')

plt.subplot(133)
plt.imshow(restored_image, cmap='gray')
plt.title('Imagen Restaurada (Tikhonov-Miller)')
plt.axis('off')

plt.show()

