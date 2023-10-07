import numpy as np
import cv2
import matplotlib.pyplot as plt

image = cv2.imread('clown.jpg', cv2.IMREAD_GRAYSCALE)

f_transform = np.fft.fft2(image)
f_transform_shifted = np.fft.fftshift(f_transform) 

magnitude_spectrum = np.log(np.abs(f_transform_shifted) + 1) 
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Espectro de Frecuencia')
plt.colorbar()
plt.show()

interference_coordinates = [(190, 122), (104, 171), (126, 134),(168, 159), (104,23),(105,24), (189,11), (104,281), (189,267), (30,171),(287,171),(6,122)]

# Mascar con 1s
mask = np.ones_like(f_transform)

for x, y in interference_coordinates[:4]:
    mask[y-10:y+10, x-10:x+10] *= 0  
#mascara más suave
for x, y in interference_coordinates[8:]:
    mask[y-5:y+5, x-5:x+5] = 0.5 

f_transform_filtered = f_transform_shifted * mask

filtered_image = np.abs(np.fft.ifft2(np.fft.ifftshift(f_transform_filtered)))

plt.imshow(filtered_image.astype(np.uint8), cmap='gray')
plt.title('Filtered Image')
plt.show()


filtered_image = cv2.medianBlur(filtered_image.astype(np.uint8), 7)
plt.imshow(filtered_image.astype(np.uint8), cmap='gray')
plt.title('Filtered Image with median blur')
plt.show()


plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

