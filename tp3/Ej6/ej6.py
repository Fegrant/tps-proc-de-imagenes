import numpy as np
import cv2

cutoff = 10
order = 2

image = cv2.imread('../image_sources/tun.jpg')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float64)

x, y = gray_image.shape

# Add a small offset to avoid division by zero
epsilon = 1e-8  # Small positive constant
gray_image_offset = gray_image + epsilon

# Calculate the logarithm
image_logued = np.log(1 + gray_image_offset)

# DFT
image_dft = np.fft.fft2(image_logued)

# Filter
A = np.zeros((x, y))
H = np.zeros((x, y))
d = cutoff
n = order

for i in range(x):
    for j in range(y):
        A[i, j] = np.sqrt((i - x / 2) ** 2 + (j - y / 2) ** 2)
        if A[i, j] == 0:
            H[i, j] = 0  # Handle division by zero by setting H to a default value (0 in this case)
        else:
            H[i, j] = 1 / (1 + ((d / A[i, j]) ** (2 * n)))

Yh = 0.0999
Yl = 1.01

H = ((Yl - Yh) * H) + Yh
H = 1 - H

image_f = H * image_dft

# Inverse DFT
image_n = np.abs(np.fft.ifft2(image_f))

# Inverse log
image_final = np.exp(image_n)

# Apply the full dynamic range display (similar to MATLAB's imshow(_, []))
min_val = np.min(image_final)
max_val = np.max(image_final)
image_adjusted = ((image_final - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# Display the final image
cv2.imwrite('./results/homomorphicImageLn.jpg', image_adjusted)
