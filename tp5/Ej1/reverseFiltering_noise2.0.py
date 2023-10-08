import numpy as np
import cv2
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

cv2.imwrite("results/Dimage.jpg", g)

# 1. creating a new h and altering to contain zero and near-zero values
Hz = np.array(H, copy=True)
Hz[np.abs(H) < 0.4] = 0.0001
Hz[np.abs(H) < 0.2] = 0.0

# 2. adding noise to the image
g_noise = (g.astype(np.int32) + np.random.randint(5, size=f.shape)).astype(np.uint8)
Gn = fftn(g_noise)  # taking it FFT

# Inverse Transform
gn = ifftn(Gn).real

cv2.imwrite("results/DNoiseImg.jpg", gn)

# compute FFTs
Gn = fftn(gn)

# choose a value to fill the near-zero values with some constant value
Hz[np.abs(Hz) <= 0.0002] = 0.0002

# inverse filtering
Fn_hat = np.divide(Gn, Hz)

# inverse FFT
fn_hat = ifftn(Fn_hat).real

cv2.imwrite("results/UltimateRestore.jpg", fn_hat)
