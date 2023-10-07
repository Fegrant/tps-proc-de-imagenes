import numpy as np
import cv2
from scipy.signal import convolve2d
from scipy.fft import fft2, ifft2, fftshift, ifftshift
import matplotlib.pyplot as plt


def create_gaussian_psf(size, sigma):
    print("psf")
    x = np.linspace(-size // 2, size // 2, size)
    y = np.linspace(-size // 2, size // 2, size)
    xv, yv = np.meshgrid(x, y)
    psf = np.exp(-(xv**2 + yv**2) / (2 * sigma**2))
    psf /= np.sum(psf)  # Normalize the PSF
    return psf


original_image = cv2.imread("../image_sources/img.png", cv2.IMREAD_GRAYSCALE)

psf_size = 15
psf_sigma = 2.0
psf = create_gaussian_psf(psf_size, psf_sigma)


degraded_image = convolve2d(original_image, psf, 'same', 'symm')

# noise_stddev = 10
# degraded_image += np.random.normal(0, noise_stddev, degraded_image.shape).astype(np.uint8)

cv2.imwrite("results/degraded_image.jpg", degraded_image)

# Ensure PSF and blurred image have the same dimensions
psf = np.pad(psf, [(0, degraded_image.shape[0] - psf.shape[0]), (0, degraded_image.shape[1] - psf.shape[1])], mode='constant')

# Perform Fourier Transform on the image and the PSF
image_fft = fft2(degraded_image)
psf_fft = fft2(psf)

# Avoid division by zero, add a small constant to the PSF FFT
psf_fft += 1e-5

# Inverse filtering
restored_image_fft = image_fft / psf_fft

# Inverse Fourier Transform
restored_image = np.abs(ifft2(restored_image_fft))
cv2.imwrite("results/restoredImage.jpg", restored_image)
print("restored")
