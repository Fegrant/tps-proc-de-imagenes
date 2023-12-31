import numpy as np
import cv2
from scipy.signal import convolve2d
from scipy.fft import fft2, ifft2, fftshift, ifftshift
import matplotlib.pyplot as plt
import imageio
from scipy.fftpack import fftn, ifftn, fftshift


def gaussian_filter(k=5, sigma=1.0):
    arx = np.arange((-k // 2) + 1.0, (k // 2) + 1.0)
    x, y = np.meshgrid(arx, arx)
    filt = np.exp(-(1 / 2) * (np.square(x) + np.square(y)) / np.square(sigma))
    return filt / np.sum(filt)


f = cv2.imread("../image_sources/img.png", cv2.IMREAD_GRAYSCALE)

h = gaussian_filter(k=9, sigma=1.5)

# computing the number of padding on one side
a = int(f.shape[0] // 2 - h.shape[0] // 2)
h_pad = np.pad(h, (a, a - 1), 'constant', constant_values=(0))

# computing the Fourier transforms
F = fftn(f)
H = fftn(h_pad)

# convolution
G = np.multiply(F, H)

# Inverse Transform
# - we have to perform FFT shift before reconstructing the image in the space domain
g = fftshift(ifftn(G).real)

cv2.imwrite("results/degraded_image.jpg", g)

# reverse filter  F_hat = G/H
F_hat = np.divide(G, H)

f_hat = ifftn(F_hat).real

cv2.imwrite("results/restoredImage.jpg", f_hat)
