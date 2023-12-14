from PIL import Image, ImageEnhance

# Open the image
image = Image.open('results/contrast1.5.jpg')

# Create an ImageEnhance object and adjust the brightness (factor > 1 increases brightness, factor < 1 decreases
# brightness)
factor = 1.25 # You can adjust this value
enhancer = ImageEnhance.Brightness(image)
adjusted_image = enhancer.enhance(factor)

# Save the adjusted image
adjusted_image.save(f'results/bright{factor}.jpg')
