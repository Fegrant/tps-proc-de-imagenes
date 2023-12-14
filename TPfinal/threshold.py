import cv2
import numpy as np

# Load the image
image = cv2.imread('results/contrast1.5.jpg')

# Calculate the threshold value as a percentage of the maximum pixel value
percentage_threshold = 25
max_pixel_value = 255  # Assuming 8-bit grayscale image
threshold_value = (percentage_threshold / 100) * max_pixel_value

# Apply thresholding
_, thresholded_image = cv2.threshold(image, threshold_value, max_pixel_value, cv2.THRESH_BINARY)

# Save the thresholded image
cv2.imwrite('./results/thresholded_image.jpg', thresholded_image)

