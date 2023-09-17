import cv2
import numpy as np

image = cv2.imread('../image_sources/blurry_moon.tif', cv2.IMREAD_GRAYSCALE)

normal_mask = np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]], dtype=np.float32)

mask_with_diagonals = np.array([[-1, -1, -1],
                                [-1, 9, -1],
                                [-1, -1, -1]], dtype=np.float32)

height, width = image.shape
normal_laplacian = np.zeros((height, width), dtype=np.float32)
laplacian_with_diagonals = np.zeros((height, width), dtype=np.float32)

# Guardamos en una matriz la imagen con la máscara normal, y en otra con la máscara con diagonales
for i in range(1, height - 1):
    for j in range(1, width - 1):
        region = image[i-1:i+2, j-1:j+2]
        normal_laplacian[i, j] = np.sum(region * normal_mask)
        laplacian_with_diagonals[i, j] = np.sum(region * mask_with_diagonals)

normal_laplacian = np.uint8(np.absolute(normal_laplacian))
laplacian_with_diagonals = np.uint8(np.absolute(laplacian_with_diagonals))

image_with_normal_mask = cv2.subtract(image, normal_laplacian)
image_with_diagonal_mask = cv2.subtract(image, laplacian_with_diagonals)

cv2.imwrite('results/laplacian_90deg.png', normal_laplacian)
cv2.imwrite('results/laplacian_diagonals.png', laplacian_with_diagonals)
cv2.imwrite('results/laplacian_90deg_result.png', image_with_normal_mask)
cv2.imwrite('results/laplacian_diagonals_result.png', image_with_diagonal_mask)