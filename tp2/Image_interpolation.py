from PIL import Image

# Abrir la imagen original
image1 = Image.open("results/Rose512.jpg")
image2 = Image.open("results/Rose256.jpg")
image3 = Image.open("results/Rose128.jpg")
image4 = Image.open("results/Rose64.jpg")
image5 = Image.open("results/Rose32.jpg")

images = [image1, image2, image3, image4, image5]

# Definir las nuevas dimensiones deseadas para la imagen interpolada
new_width = 1024
new_height = 1024

# Realizar la interpolación para cambiar el tamaño de la imagen
for index, image in enumerate(images):
    interpolated_image = image.resize((new_width, new_height), Image.NEAREST)
    # Guardar la imagen interpolada
    interpolated_image.save(f"results/interpolated_image{index+1}.jpg")
