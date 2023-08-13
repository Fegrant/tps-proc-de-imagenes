from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math

import math
import sys
import time

# Función para realizar la decimación tomando un pixel específico del bloque
def decimate_image(image_array, pixel_position, block_size):
    decimated_pixels = []
    for y in range(0, image_array.shape[0], block_size):
        for x in range(0, image_array.shape[1], block_size):
            block = image_array[y:y+block_size, x:x+block_size]
            decimated_pixels.append(block[pixel_position]) # quiero del bloque el pixel position (0,0) o (1,1)
    decimated_image = np.array(decimated_pixels).reshape(image_array.shape[0] // block_size, image_array.shape[1] // block_size)
    return decimated_image

# Función para realizar la decimación tomando un pixel específico del bloque
def decimate_image_avg(image_array, block_size):
    decimated_pixels = []
    for y in range(0, image_array.shape[0], block_size):
        for x in range(0, image_array.shape[1], block_size):
            block = image_array[y:y+block_size, x:x+block_size]
            numpy_block = np.array(block)
            decimated_pixels.append(np.mean(numpy_block))
    decimated_image = np.array(decimated_pixels).reshape(image_array.shape[0] // block_size, image_array.shape[1] // block_size)
    return decimated_image


# Interpolation kernel
def u(s, a):
    if abs(s) >= 0 and abs(s) <= 1:
        return (a + 2) * (abs(s) ** 3) - (a + 3) * (abs(s) ** 2) + 1
    elif abs(s) > 1 and abs(s) <= 2:
        return a * (abs(s) ** 3) - 5 * a * (abs(s) ** 2) + 8 * a * abs(s) - 4 * a
    return 0

def padding(img, H, W):
    zimg = np.zeros((H + 4, W + 4))
    zimg[2:H + 2, 2:W + 2] = img

    zimg[2:H + 2, 0:2] = img[:, 0:1]
    zimg[H + 2:H + 4, 2:W + 2] = img[H - 1:H, :]
    zimg[2:H + 2, W + 2:W + 4] = img[:, W - 1:W]
    zimg[0:2, 2:W + 2] = img[0:1, :]

    zimg[0:2, 0:2] = img[0, 0]
    zimg[H + 2:H + 4, 0:2] = img[H - 1, 0]
    zimg[H + 2:H + 4, W + 2:W + 4] = img[H - 1, W - 1]
    zimg[0:2, W + 2:W + 4] = img[0, W - 1]
    return zimg

def bicubic(img, ratio, a):
    H, W = img.shape
    img = padding(img, H, W)

    dH = math.floor(H * ratio)
    dW = math.floor(W * ratio)

    dst = np.zeros((dH, dW))
    h = 1 / ratio


    for j in range(dH):
        for i in range(dW):
            x, y = i * h + 2, j * h + 2

        
           
            x1 = max(min(1 + x - math.floor(x), W - 1), 0)
            x2 = max(min(x - math.floor(x), W - 1), 0)
            x3 = max(min(math.floor(x) + 1 - x, W - 1), 0)
            x4 = max(min(math.floor(x) + 2 - x, W - 1), 0)

            y1 = max(min(1 + y - math.floor(y), H - 1), 0)
            y2 = max(min(y - math.floor(y), H - 1), 0)
            y3 = max(min(math.floor(y) + 1 - y, H - 1), 0)
            y4 = max(min(math.floor(y) + 2 - y, H - 1), 0)
            x, y = i * h + 2, j * h + 2

            mat_l = np.array([[u(x1, a), u(x2, a), u(x3, a), u(x4, a)]])
            mat_m = np.array([[img[int(y - y1), int(x - x1)],
                               img[int(y - y2), int(x - x1)],
                               img[int(y + y3), int(x - x1)],
                               img[int(y + y4), int(x - x1)]],
                              [img[int(y - y1), int(x - x2)],
                               img[int(y - y2), int(x - x2)],
                               img[int(y + y3), int(x - x2)],
                               img[int(y + y4), int(x - x2)]],
                              [img[int(y - y1), int(x + x3)],
                               img[int(y - y2), int(x + x3)],
                               img[int(y + y3), int(x + x3)],
                               img[int(y + y4), int(x + x3)]],
                              [img[int(y - y1), int(x + x4)],
                               img[int(y - y2), int(x + x4)],
                               img[int(y + y3), int(x + x4)],
                               img[int(y + y4), int(x + x4)]]])
            mat_r = np.array(
                [[u(y1, a)], [u(y2, a)], [u(y3, a)], [u(y4, a)]])

            dst[j, i] = np.dot(np.dot(mat_l, mat_m), mat_r)

    return dst
  
  


def bilinear_interpolation(image, y, x):
    height = image.shape[0]
    width = image.shape[1]

    x1 = max(min(math.floor(x), width - 1), 0)
    y1 = max(min(math.floor(y), height - 1), 0)
    x2 = max(min(math.ceil(x), width - 1), 0)
    y2 = max(min(math.ceil(y), height - 1), 0)

    a = float(image[y1, x1])
    b = float(image[y2, x1])
    c = float(image[y1, x2])
    d = float(image[y2, x2])

    dx = x - x1
    dy = y - y1

    new_pixel = a * (1 - dx) * (1 - dy)
    new_pixel += b * dy * (1 - dx)
    new_pixel += c * dx * (1 - dy)
    new_pixel += d * dx * dy
    return round(new_pixel)

interpolation_functions = {
    "bilinear": bilinear_interpolation,
}


def resize(image, new_height, new_width, interpolation_type="bilinear"):
    new_image = np.zeros((new_height, new_width), image.dtype)  # new_image = [[0 for _ in range(new_width)] for _ in range(new_height)]

    orig_height = image.shape[0]
    orig_width = image.shape[1]

    # Compute center column and center row
    x_orig_center = (orig_width-1) / 2
    y_orig_center = (orig_height-1) / 2

    # Compute center of resized image
    x_scaled_center = (new_width-1) / 2
    y_scaled_center = (new_height-1) / 2

    # Compute the scale in both axes
    scale_x = orig_width / new_width
    scale_y = orig_height / new_height

    for y in range(new_height):
        for x in range(new_width):
            x_ = (x - x_scaled_center) * scale_x + x_orig_center
            y_ = (y - y_scaled_center) * scale_y + y_orig_center

            new_image[y, x] = interpolation_functions[interpolation_type](image, y_, x_)

    return new_image



def main():
    
    # Tamaño del bloque
    block_size = 4
    ratio = 4
    a = -1/4

    # Cargar la imagen
    image_path = "mono.bmp"
    original_image = Image.open(image_path).convert('L')
    # Convertir la imagen a un array numpy
    image_array = np.array(original_image)

    # Graficar el espectro de la imagen original
    original_spectrum = np.fft.fftshift(np.fft.fft2(image_array))
    plt.imshow(np.log(np.abs(original_spectrum) + 1), cmap='pink')
    plt.title("Espectro de la imagen original")
    plt.show()


    #decimated 2_2
    decimated_pixel_22 = decimate_image(image_array,(1, 1),block_size)
    image  = Image.fromarray(decimated_pixel_22.astype('uint8'))
    image.save("decimated_pixel_22.bmp")  

    #bilinear interpolation 2_2
    new_height, new_width = image_array.shape[0], image_array.shape[1]
    interpolated_image = resize(decimated_pixel_22, new_height, new_width)
    interpolated_pil_image  = Image.fromarray(interpolated_image.astype('uint8'))
    interpolated_pil_image.save("interpolated_image_22.bmp")

    #bicubic interpolation 2_2
    interpolated_image = bicubic(decimated_pixel_22, ratio, a)
    bicubic_img = Image.fromarray(interpolated_image.astype('uint8'))
    bicubic_img.save('bicubic_image_22.bmp')

    #decimated 1_1
    decimated_pixel_11 = decimate_image(image_array,(0, 0),block_size)
    image  = Image.fromarray(decimated_pixel_11.astype('uint8'))
    image.save("decimated_pixel_11.bmp") 

    #bilinear interpolation 1_1
    interpolated_image = resize(decimated_pixel_11, new_height, new_width)
    interpolated_pil_image  = Image.fromarray(interpolated_image.astype('uint8'))
    interpolated_pil_image.save("interpolated_image_11.bmp")

    #bicubic interpolation 1_1
    interpolated_image = bicubic(decimated_pixel_11, ratio, a)
    bicubic_img = Image.fromarray(interpolated_image.astype('uint8'))
    bicubic_img.save('bicubic_image_11.bmp')

    #decimated avg
    decimated_pixel_avg_ = decimate_image_avg(image_array,block_size)
    image = Image.fromarray(decimated_pixel_avg_.astype('uint8'))
    image.save("decimated_pixel_avg.bmp")  # Save the image to a file

    #bilinear interpolation avg
    interpolated_image = resize(decimated_pixel_avg_, new_height, new_width)
    interpolated_pil_image = Image.fromarray(interpolated_image.astype('uint8'))
    interpolated_pil_image.save("interpolated_image_avg.bmp")

    #bicubic interpolation
    interpolated_image = bicubic(decimated_pixel_avg_, ratio, a)
    bicubic_img = Image.fromarray(interpolated_image.astype('uint8'))
    bicubic_img.save('bicubic_image_avg.bmp')



if __name__ == "__main__":
    main()