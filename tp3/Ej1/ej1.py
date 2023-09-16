import cv2
import numpy as np

# Load the image
image = cv2.imread('../image_sources/Fig0448(a)(characters_test_pattern).tif')
sequence = [3, 5, 9, 15, 25, 35, 45, 55]
# Apply Gaussian blur to the image
for k in sequence:
    k_size = (k, k)  # Kernel size, adjust as needed
    blurred_image = cv2.GaussianBlur(image, k_size, 0)
    cv2.imwrite(f"./results/low_pass_filtered_image{k}.jpg", blurred_image)


