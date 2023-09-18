import cv2
import numpy as np

image = cv2.imread('../image_sources/blurry_moon.tif', cv2.IMREAD_GRAYSCALE)

normal_mask = np.array([[1, 1, 1],
                        [1, -8, 1],
                        [1, 1, 1]], dtype=np.float32)

borders_mask = np.array([[-1, -1, -1],
                                [-1, 9, -1],
                                [-1, -1, -1]], dtype=np.float32)

height, width = image.shape
normal_laplacian = np.zeros((height, width), dtype=np.float32)
borders_laplacian = np.zeros((height, width), dtype=np.float32)

# Guardamos en una matriz la imagen con la máscara normal, y en otra con la máscara con diagonales
for i in range(1, height - 1):
    for j in range(1, width - 1):
        region = image[i-1:i+2, j-1:j+2]
        normal_value = np.sum(region * normal_mask)
        normal_laplacian[i, j] = normal_value
        borders_value = np.sum(region * borders_mask)
        borders_laplacian[i, j] = borders_value

normal_laplacian = np.clip(normal_laplacian, 0, 255).astype(np.uint8)
borders_laplacian = np.clip(borders_laplacian, 0, 255).astype(np.uint8)
# Cambio de escala al laplaciano normal, que sino satura
normal_laplacian_scaled_down = np.clip(normal_laplacian * 0.5, 0, 255).astype(np.uint8)
normal_laplacian_scaled_up = np.clip(normal_laplacian * 1.5, 0, 255).astype(np.uint8)

image_with_normal_mask = cv2.subtract(image, normal_laplacian)
image_with_borders_mask = cv2.subtract(image, borders_laplacian)
image_with_normal_mask_scaled_down = cv2.subtract(image, normal_laplacian_scaled_down)
image_with_normal_mask_scaled_up = cv2.subtract(image, normal_laplacian_scaled_up)

cv2.imwrite('results/original_image.png', image)
cv2.imwrite('results/normal_laplacian.png', normal_laplacian)
cv2.imwrite('results/borders_laplacian.png', borders_laplacian)
cv2.imwrite('results/image_with_normal_laplacian.png', image_with_normal_mask)
cv2.imwrite('results/image_with_normal_laplacian_scaled_down.png', image_with_normal_mask_scaled_down)
cv2.imwrite('results/image_with_normal_laplacian_scaled_up.png', image_with_normal_mask_scaled_up)
cv2.imwrite('results/image_with_borders_laplacian.png', image_with_borders_mask)