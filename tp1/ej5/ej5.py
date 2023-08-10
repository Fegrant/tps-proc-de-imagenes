from PIL import Image
import numpy as np



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



def main():
    # Cargar la imagen
    image_path = "mono.bmp"
    original_image = Image.open(image_path)

    # Convertir la imagen a un array numpy
    image_array = np.array(original_image)

    # Tamaño del bloque
    block_size = 4
    # Decimación usando diferentes puntos
    decimated_pixel_22 = decimate_image(image_array,(1, 1),block_size)
    # Convertir el numpy array a una imagen PIL
    image = Image.fromarray(decimated_pixel_22)
    image.save("decimated_pixel_22.bmp")  # Save the image to a file


    decimated_pixel_11 = decimate_image(image_array,(0, 0),block_size)
    # Convertir el numpy array a una imagen PIL
    image = Image.fromarray(decimated_pixel_11)
    image.save("decimated_pixel_11.bmp")  # Save the image to a file

    decimated_pixel_avg_ = decimate_image_avg(image_array,block_size)
    # Convertir el numpy array a una imagen PIL
    image = Image.fromarray(decimated_pixel_avg_, mode="L")
    image.save("decimated_pixel_avg.bmp")  # Save the image to a file


if __name__ == "__main__":
    main()