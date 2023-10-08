import numpy as np
import cv2
from scipy.fftpack import fftn, ifftn, fftshift


def gaussian_filter(k=5, sigma=1.0):
    arx = np.arange((-k // 2) + 1.0, (k // 2) + 1.0)
    x, y = np.meshgrid(arx, arx)
    filt = np.exp(-(1 / 2) * (np.square(x) + np.square(y)) / np.square(sigma))
    return filt / np.sum(filt)


f = cv2.imread("../image_sources/img.png", cv2.IMREAD_GRAYSCALE)

h = gaussian_filter(k=7, sigma=2.5)

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

# # 2. adding noise to the image
# g_noise = (g.astype(np.int32) + np.random.randint(5, size=f.shape)).astype(np.uint8)
# Gn = fftn(g_noise)  # taking it FFT

# Generate Gaussian noise with the same dimensions as the image
noise = np.random.normal(0, 0.5, g.shape).astype(np.uint8)
# Add the noise to the image
g_noise = cv2.add(g, noise, dtype=cv2.CV_8U)
Gn = fftn(g_noise)  # taking it FFT



# Inverse Transform
# - we have to perform FFT shift before reconstructing the image in the space domain for the image that was convolved
gn = ifftn(Gn).real

cv2.imwrite("results/degraded_image2.jpg", g)
cv2.imwrite("results/degraded_image_noisy.jpg", gn)


# compute FFTs
Gn = fftn(gn)

# inverse filtering with noisy image
Fn_hat = np.divide(Gn, H)
fn_hat = fftshift(ifftn(Fn_hat).real)

cv2.imwrite("results/restoredNoisyImage3.jpg", fn_hat)


