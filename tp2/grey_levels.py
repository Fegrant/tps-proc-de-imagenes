from PIL import Image


def remove_bit_from_pixels(image_path, mask):
    image = Image.open(image_path)

    width, height = image.size

    result_image = Image.new(image.mode, (width, height))
    result_image_pixels = []

    pixeles = list(image.getdata())

    # Itera sobre cada píxel

    for pixel in pixeles:
        modified_pixel = pixel & mask
        result_image_pixels.append(modified_pixel)

    result_image.putdata(result_image_pixels)
    return result_image


input_image_path = "image_sources/Fig0221(a)(ctskull-256).tif"

masks = [0b10000000,
         0b1100000,
         0b1110000,
         0b11110000,
         0b11111000,
         0b11111100,
         0b11111110,
         0b11111111]

for maski in masks:
    new_image = remove_bit_from_pixels(input_image_path, maski)

    output_image_path = f"results/skull{bin(maski)}.jpg"
    print(output_image_path)
    new_image.save(output_image_path)
