from PIL import Image


def delete_alternate_column(image_path):
    image = Image.open(image_path)

    width, height = image.size
    new_width = width // 2
    new_height = height // 2

    result_image = Image.new("RGB", (new_width, new_height))

    for y in range(0, height, 2):  # Borrar filas pares
        new_row = []
        for x in range(0, width, 2):  # Borrar columnas pares
            pixel = image.getpixel((x, y))
            new_row.append(pixel)
        result_image.putdata(new_row)

    return image, new_width


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_image_path = "rose1024.jpg"

    new_image, updated_width = delete_alternate_column(input_image_path)

    output_image_path = f"Rose{updated_width}.jpg"

    print(output_image_path)
    new_image.save(output_image_path)
