import numpy as np
import cv2
image = cv2.imread('montion-blur.jpg')

kernel_size = 15


kernel = np.zeros((kernel_size, kernel_size))
kernel[int((kernel_size-1)/2), :] = 1.0 / kernel_size  # Desenfoque lineal

motion_blurred_image = cv2.filter2D(image, -1, kernel)


cv2.imshow('Imagen Original', image)
cv2.imshow('Imagen con Motion Blur', motion_blurred_image)

mse_motion_blur = np.mean((image - motion_blurred_image) ** 2)

#MSE
print(f'MSE entre la imagen original y la imagen con Motion Blur: {mse_motion_blur}')

cv2.waitKey(0)
cv2.destroyAllWindows()