import cv2
import numpy as np
import matplotlib.pyplot as plt

image_a = cv2.imread('image_sources/dog1ss.jpg', cv2.IMREAD_GRAYSCALE)
image_b = cv2.imread('image_sources/dog2ss.jpg', cv2.IMREAD_GRAYSCALE)

dft_a = np.fft.fft2(image_a)
I_a = np.fft.fftshift(dft_a)

dft_b = np.fft.fft2(image_b)
dft_shifted_b = np.fft.fftshift(dft_b)
I_b = np.conjugate(dft_shifted_b)

Ruv = I_a * I_b / np.abs(I_a * I_b)
ruv = np.real(np.fft.ifft2(Ruv))

delta_center = (0, 0)
delta_value = 0

for i in range(len(ruv)):
    for j in range(len(ruv[0])):
        # Busca el centro de la delta
        if ruv[i][j] > delta_value:
            delta_center = (i, j)
            delta_value = ruv[i][j]

print(delta_center)

# Representación visual de la delta
plt.figure(figsize=(12, 6))
plt.subplot(121), plt.imshow(ruv, cmap='gist_gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

plt.show()