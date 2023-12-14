import numpy as np
import cv2

color_image = cv2.imread('IMG_6932.png').astype(np.float64)

# Parameters
cutoff = 10
order = 2
Yh = 0.0999
Yl = 1.01

homomorphic_image = np.zeros(color_image.shape)

for i in range(color_image.shape[2]):
    color_channel = color_image[:, :, i]

    # Add a small offset to avoid division by zero
    epsilon = 1e-8
    color_channel_offset = color_channel + epsilon

    # Calculate the logarithm
    color_channel_logued = np.log(1 + color_channel_offset)

    # DFT
    color_channel_dft = np.fft.fft2(color_channel_logued)

    # Filter
    x, y = color_channel.shape
    A = np.zeros((x, y))
    H = np.zeros((x, y))
    d = cutoff
    n = order

    for j in range(x):
        for k in range(y):
            A[j, k] = np.sqrt((j - x / 2) ** 2 + (k - y / 2) ** 2)
            if A[j, k] == 0:
                H[j, k] = 0
            else:
                H[j, k] = 1 / (1 + ((d / A[j, k]) ** (2 * n)))

    H = ((Yl - Yh) * H) + Yh
    H = 1 - H

    color_channel_f = H * color_channel_dft

    # Inverse DFT
    color_channel_n = np.abs(np.fft.ifft2(color_channel_f))

    # Inverse log
    color_channel_final = np.exp(color_channel_n)

    # Update the original color channel with the processed values
    homomorphic_image[:, :, i] = color_channel_final


homomorphic_image = ((homomorphic_image - np.min(homomorphic_image)) / (np.max(homomorphic_image) - np.min(homomorphic_image)) * 255).astype(np.uint8)

cv2.imwrite('homomorphicColor.png', homomorphic_image)
