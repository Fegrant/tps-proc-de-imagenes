import cv2
import matplotlib.pyplot as plt
import os
import numpy as np

if not os.path.exists('results'):
    os.makedirs('results')

image = cv2.imread('../image_sources/onedollar.jpg', cv2.IMREAD_GRAYSCALE)
num_bits = 8
bitplanes_to_use = [0, 4, 5, 6, 7]

bit_planes = [((image >> i) & 1) * 255 for i in range(num_bits)]
overlayed_image = np.zeros(image.shape, dtype=np.uint8)

for i, bit_plane in enumerate(bit_planes):
    if i in bitplanes_to_use:
        original_bitplane = (bit_plane & 1) << i
        overlayed_image += original_bitplane

overlayed_image = np.uint8(overlayed_image)

fig, ax = plt.subplots(2, 1, figsize=(15, 10))
ax[0].imshow(image, cmap='gray')
ax[0].set_title('Original image')
ax[1].imshow(overlayed_image, cmap='gray')
ax[1].set_title(f'Copy made of bitplanes {bitplanes_to_use}')
plt.savefig(f'results/bitplanes_overlay.png')
plt.show()