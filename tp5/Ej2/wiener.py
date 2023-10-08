import os
import cv2
import numpy as np
from numpy.fft import fft2, ifft2
from scipy.signal import windows, convolve2d


def blur(img, kernel_size=3):
    dummy = np.copy(img)
    h = np.eye(kernel_size) / kernel_size
    dummy = convolve2d(dummy, h, mode='valid')
    return dummy


def add_gaussian_noise(img, sigma):
    gauss = np.random.normal(0, sigma, np.shape(img))
    noisy_img = img + gauss
    noisy_img[noisy_img < 0] = 0
    noisy_img[noisy_img > 255] = 255
    return noisy_img


def wiener_filter(img, kernel, K):
    kernel /= np.sum(kernel)
    dummy = np.copy(img)
    dummy = fft2(dummy)
    kernel = fft2(kernel, s=img.shape)
    kernel = np.conj(kernel) / (np.abs(kernel) ** 2 + K)
    dummy = dummy * kernel
    dummy = np.abs(ifft2(dummy))
    return dummy


def gaussian_kernel(kernel_size=3):
    h = windows.gaussian(kernel_size, kernel_size / 3).reshape(kernel_size, 1)
    h = np.dot(h, h.transpose())
    h /= np.sum(h)
    return h


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


if __name__ == '__main__':
    # Load image and convert it to gray scale
    img = cv2.imread("../image_sources/lena1000p.jpg", cv2.IMREAD_GRAYSCALE)

    # Blur the image
    blurred_img = blur(img, kernel_size=7)

    # Add Gaussian noise
    noisy_img = add_gaussian_noise(blurred_img, sigma=20)

    # Apply Wiener Filter
    kernel = gaussian_kernel(5)
    filtered_img = wiener_filter(noisy_img, kernel, K=10)

    # Display results
    display = [img, blurred_img, noisy_img, filtered_img]
    label = ['Motion_Blurred_Image', 'Motion_Blurring + Gaussian_Noise', 'Wiener_Filter_applied']

    for i in range(len(display)):
        cv2.imwrite(f"results/{label[i]}.png", display[i])

