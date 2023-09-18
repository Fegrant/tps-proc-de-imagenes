import cv2
import numpy as np

image = cv2.imread('../image_sources/high_boost_source.png', cv2.IMREAD_GRAYSCALE)

# Oscurecemos la imagen previo al high-boost
factor_oscurecimiento = 0.4
image = (image * factor_oscurecimiento).astype(np.uint8)

# Valor a usar para el high-boost
A = 1.5

mask = np.array([[-1, -1, -1],
                 [-1, A + 8, -1],
                 [-1, -1, -1]], dtype=np.float32)

height, width = image.shape
hb_laplacian = np.zeros((height, width), dtype=np.float32)

for i in range(1, height - 1):
    for j in range(1, width - 1):
        region = image[i-1:i+2, j-1:j+2]
        hb_laplacian[i, j] = np.sum(region * mask)

# Para limitar los valores máximos de brillo (>255 ya satura)
hb_laplacian = np.clip(hb_laplacian, 0, 255).astype(np.uint8)
hb_image = cv2.add(image, hb_laplacian)

cv2.imwrite('results/original_image.png', image)
cv2.imwrite('results/high_boosted_image.png', hb_image)