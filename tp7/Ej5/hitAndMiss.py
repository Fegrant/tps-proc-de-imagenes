import numpy as np
import cv2
from matplotlib import pyplot as plt

# Creating the input image (regions)
regions = np.zeros((10, 10), dtype=np.uint8)
regions[1, :2] = 255
regions[5:8, 6:8] = 255
regions[8, 0] = 255

# Showing the input image
print("Image")
plt.imshow(regions, cmap='gray', interpolation='nearest')
plt.show()

# Define the hit-miss template
template = np.array([
    [0, 1, 1],
    [0, 1, 1],
    [0, 1, 1]
], dtype=np.uint8)
# Print the template (kernel) as an image
print("Hit-Miss Kernel")
plt.imshow(template, cmap='gray', interpolation='nearest')
plt.show()
# Perform the hit-miss transform using OpenCV
result = cv2.morphologyEx(regions, cv2.MORPH_HITMISS, template)

# Showing the transformed image
print("Image after hit-miss transform")
plt.imshow(result, cmap='gray', interpolation='nearest')
plt.show()




