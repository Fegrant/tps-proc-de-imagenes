from PIL import Image


def delete_alternate_column(image_path):
    image = Image.open(image_path)

    width, height = image.size
    new_width = width // 2
    new_height = height // 2

    result_image = Image.new(image.mode, (new_width, new_height))
    result_image_pixels = []

    for y in range(0, height, 2):  # Borrar filas pares
        for x in range(0, width, 2):  # Borrar columnas pares
            pixel = image.getpixel((x, y))
            result_image_pixels.append(pixel)

    result_image.putdata(result_image_pixels)
    return result_image, new_width


input_image_path = "image_sources/Fig0219(rose1024).jpg"
# input_image_path = "Rose64.jpg"

new_image, updated_width = delete_alternate_column(input_image_path)

output_image_path = f"results/Rose{updated_width}.jpg"

print(output_image_path)
new_image.save(output_image_path)
