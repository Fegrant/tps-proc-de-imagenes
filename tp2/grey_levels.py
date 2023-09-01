from PIL import Image

# Cargar la imagen en escala de grises
image = Image.open('imagen.png').convert('L')

# Definir el número deseado de niveles de grises (128 en este caso)
num_levels = 128

# Cuantización de niveles de grises
quantized_image = image.quantize(colors=num_levels)

# Mostrar la imagen cuantizada
quantized_image.show()