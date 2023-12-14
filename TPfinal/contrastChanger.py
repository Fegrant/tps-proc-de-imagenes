from PIL import Image, ImageEnhance

# Open the image
image = Image.open('results/homomorphicImageLn.jpg')

# Create an ImageEnhance object and adjust the contrast
# (factor > 1 increases contrast, factor < 1 decreases contrast)
factor = 2  # You can adjust this value
enhancer = ImageEnhance.Contrast(image)
adjusted_image = enhancer.enhance(factor)

# Save the adjusted image
adjusted_image.save(f'results/contrast{factor}.jpg')
