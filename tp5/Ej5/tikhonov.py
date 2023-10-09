import numpy as np
import matplotlib.pyplot as plt
from skimage import data, color, img_as_ubyte
from skimage.restoration import (denoise_tv_chambolle, denoise_bilateral,
                                 denoise_wavelet, estimate_sigma)
from skimage import io
from skimage.util import random_noise

# Cargar la imagen "coins" de skimage
coins = data.coins()

# Agregar ruido gaussiano a la imagen
coins_noisy = random_noise(coins, mode='gaussian', var=0.01)

# Aplicar la restauración con regularización (en este caso, Tikhonov)
coins_denoised = denoise_tv_chambolle(coins_noisy, weight=0.01, max_num_iter=2000)

# Mostrar las imágenes original, con ruido y restaurada
plt.figure(figsize=(12, 4))
plt.subplot(131)
plt.imshow(coins, cmap='gray')
plt.title('Imagen Original')

plt.subplot(132)
plt.imshow(coins_noisy, cmap='gray')
plt.title('Imagen con Ruido')

plt.subplot(133)
plt.imshow(coins_denoised, cmap='gray')
plt.title('Imagen Restaurada con Regularización')

plt.tight_layout()
plt.show()