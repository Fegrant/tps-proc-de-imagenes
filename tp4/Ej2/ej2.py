from PIL import Image, ImageFilter, ImageOps
import cv2
import numpy as np
import matplotlib.pyplot as plt
image = Image.open("original_image.jpg").convert("L")

# Aplica el filtro EDGE_ENHANCE para resaltar los bordes
i_edge_enhace= image.filter(ImageFilter.EDGE_ENHANCE)

i_edge_enhace_more = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

i_edge_enhace.save("image_filter_enhace.jpg")

i_edge_enhace_more.save("image_filter_enhace_more.jpg")

invert = ImageOps.invert(i_edge_enhace_more)

invert.save("enhace_more_invert.png")

original_image = image.convert('L')
b = np.array(original_image)
# Create an unsharp mask kernel, high pass
h = np.array([[0, -1, 0],
             [-1, 5, -1],
              [0, -1, 0]])

# Apply the filter to the image
i_high_pass = cv2.filter2D(b, -1, h)

cv2.imwrite("high_pass.jpg", i_high_pass)