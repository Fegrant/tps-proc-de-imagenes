from PIL import Image
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

#matrix escala blancos
def wbscalematrix(m, n, wb_scales, align):
    # Makes a white-balance scaling matrix for an image of size m-by-n
    # from the individual RGB white balance scalar multipliers [wb_scales] = [R_scale G_scale B_scale].
    #
    # [align] is string indicating the 2x2 Bayer arrangement: 
    # 'rggb':  
    #    R G 
    #    G B 
    # 'gbrg':
    #    G B
    #    R G
    # 'grbg','bggr' follow as before.
    #
    # 
    scalematrix = wb_scales[1] * np.ones((m, n))#initialize to all green values
    print(scalematrix)
    if (align == 'rggb'):
        scalematrix[0::2, 0::2] = wb_scales[0]  # R
        scalematrix[1::2, 1::2] = wb_scales[2]  # B
    elif (align == 'bggr'):
        scalematrix[1::2, 1::2] = wb_scales[0]  # R
        scalematrix[0::2, 0::2] = wb_scales[2]  # B
    elif (align == 'grbg'):
        scalematrix[0::2, 1::2] = wb_scales[0]  # R
        scalematrix[1::2, 0::2] = wb_scales[2]  # B
    elif (align == 'gbrg'):
        scalematrix[1::2, 0::2] = wb_scales[0]  # R
        scalematrix[0::2, 1::2] = wb_scales[2]  # B
    print(scalematrix)
    return scalematrix

def apply_cmatrix(img, cmatrix):
    # Applies color transformation CMATRIX to RGB input IM. 
    # Finds the appropriate weighting of the old color planes to form the new color planes, 
    # equivalent to but much more efficient than applying a matrix transformation to each pixel.
    if (img.shape[2] != 3):
        raise ValueError('Apply cmatrix to RGB image only.')

    r = cmatrix[0,0] * img[:,:,0] + cmatrix[0,1] * img[:,:,1] + cmatrix[0,2] * img[:,:,2]
    g = cmatrix[1,0] * img[:,:,0] + cmatrix[1,1] * img[:,:,1] + cmatrix[1,2] * img[:,:,2]
    b = cmatrix[2,0] * img[:,:,0] + cmatrix[2,1] * img[:,:,1] + cmatrix[2,2] * img[:,:,2]
    corrected = np.stack((r,g,b), axis=2)
    return corrected
# Función para realizar la debayerización (bilinear interpolation)

def debayering(input):
    # Bilinear Interpolation of the missing pixels
    #
    # Assumes a Bayer CFA in the 'rggb' layout
    #   R G R G
    #   G B G B
    #   R G R G
    #   G B G B
    #
    img = input.astype(np.double)

    m = img.shape[0]
    n = img.shape[1]

    # First, we're going to create indicator masks that tell us
    # where each of the color pixels are in the bayered input image
    # 1 indicates presence of that color, 0 otherwise
    red_mask = np.tile([[1, 0], [0, 0]], (int(m/2), int(n/2)))
    green_mask = np.tile([[0, 1], [1, 0]], (int(m/2), int(n/2)))
    blue_mask = np.tile([[0, 0], [0, 1]], (int(m/2), int(n/2)))

    r = np.multiply(img, red_mask)
    g = np.multiply(img, green_mask)
    b = np.multiply(img, blue_mask)

    # To conceptualize how this works, let's continue to draw it out on paper.
    # - Sketch the first 5 rows and columns of the g image
    # - Sketch the 3x3 filter and add the numeric weights (they sum to 1)
    # - Sketch the output image

    # Move the filter through the valid region of the image.
    # - What is the output at pixel 1,1 ?  [0-index, remember]
    # - What is the output at pixel 2,1 ?
    # - What is the output at pixel 3,1 ?
    # - What is the output at pixel 1,2 ?
    # - What is the output at pixel 2,2 ?
    # - What is the output at pixel 3,2 ?

    # See how it works? 
    # The filter only produces output if the surrounding pixels match its pattern.
    # When they do, it produces their mean value.

    # Note that we're going to have some incorrect values at the image boundaries, 
    # but let's ignore that for this exercise.

    # Now, let's try it for blue. This one is a two-step process.
    # - Step 1: We fill in the 'central' blue pixel in the location of the red pixel
    # - Step 2: We fill in the blue pixels at the locations of the green pixels, 
    #           similar to how the green interpolation worked, but offset by a row/column
    #
    # Sketch out the matrices to help you follow.
    # Remember, we'll still have some incorrect value at the image boundaries.
    # Interpolating green:
    filter_g = 0.25 * np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    missing_g = convolve2d(g, filter_g, 'same')
    g = g + missing_g

    # Interpolating red and blue:
    filter1 = 0.25 * np.array([[1,0,1],[0,0,0],[1,0,1]])
    missing_b1 = convolve2d(b, filter1, 'same')

    filter2 = 0.25 * np.array([[0,1,0],[1,0,1],[0,1,0]])
    missing_b2 = convolve2d(b + missing_b1, filter2, 'same')
    b = b + missing_b1 + missing_b2

    missing_r1 = convolve2d(r, filter1, 'same')
    missing_r2 = convolve2d(r + missing_r1, filter2, 'same')
    r = r + missing_r1 + missing_r2

    output = np.stack((r, g, b), axis=2)
    return output

wb_multipliers = [2.217041, 1.000000, 1.192484]
black = 0
saturation = 16383
raw_data = Image.open("imagenes/sample.tiff")
#raw_data.show()
raw = np.array(raw_data).astype(np.double)
## Normalizar la imagen
linear_bayer = (raw - black) / (saturation - black)
plt.imshow(linear_bayer, cmap='gray')
plt.show()
# Balance de blancos
mask = wbscalematrix(linear_bayer.shape[0], linear_bayer.shape[1], wb_multipliers, 'rggb')
balanced_bayer = np.multiply(linear_bayer, mask)
#balanced_bayer = linear_bayer
plt.imshow(balanced_bayer, cmap='gray')
plt.show()
lin_rgb = debayering(balanced_bayer)
plt.imshow(lin_rgb)
plt.show()
# Conversión del espacio 
rgb2xyz = np.array([[0.4124564, 0.3575761, 0.1804375],
           [0.2126729, 0.7151522, 0.0721750],
           [0.0193339, 0.1191920, 0.9503041]])
xyz2cam = np.array([[0.6653, -0.1486, -0.0611],
           [-0.4221, 1.3303, 0.0929],
           [-0.0881, 0.2416, 0.7226]])
rgb2cam = xyz2cam * rgb2xyz
denom = np.tile(np.reshape(np.sum(rgb2cam, axis=1), (3, -1)), (1, 3))
rgb2cam = np.divide(rgb2cam, denom)
cam2rgb = np.linalg.inv(rgb2cam)
lin_srgb = apply_cmatrix(lin_rgb, cam2rgb)
lin_srgb[lin_srgb > 1.0] = 1.0
plt.imshow(lin_srgb)
plt.show()
# Ajuste de brillo 
brightness_factor = 0.25
bright_srgb = lin_srgb * brightness_factor
bright_srgb[bright_srgb > 1.0] = 1.0
plt.imshow(bright_srgb)
plt.show()
# Corrección gamma 
gamma = 2.2
nl_srgb = np.power(np.maximum(bright_srgb, 0), 1.0 / gamma)
nl_srgb[nl_srgb > 1.0] = 1.0
plt.imshow(nl_srgb)
plt.show()