# Import required libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Etapa 1
im = cv2.imread('imagenes/Girl_and_rose.jpg')
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
fig, axs = plt.subplots(2, 3)
axs[0, 0].imshow(im)
axs[0, 0].set_title('1. Imagen RGB original')

# Etapa 2
gris = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
axs[0, 1].imshow(gris, cmap='gray')
axs[0, 1].set_title('2. Transformación a escala de grises')

# Etapa 3
imR = im[:,:,0].astype(float)
imG = im[:,:,1].astype(float)
imB = im[:,:,2].astype(float)
axs[0, 2].imshow(imR, cmap='gray')
axs[0, 2].set_title('3. Visualización de Banda ROJA original')

# Etapa 4
imR2 = imR - imG - imB
masc = (imR2 > 20)
imR2 = imR2 * masc
imR2 = cv2.medianBlur(imR2.astype(np.uint8), 3)
axs[1, 0].imshow(imR2, cmap='gray')
axs[1, 0].set_title('4. Filtro de mediana sobre banda ROJA')

# Etapa 5
imR2 = imR2 / 255.0
imR3 = cv2.pow(imR2, 1.8)
axs[1, 1].imshow(imR3, cmap='gray')
axs[1, 1].set_title('5. Corrección GAMMA factor 1.8')
print('En la imagen 5 haga click en el centro de la rosa...')
(x, y) = plt.ginput(1)[0]
y = round(y)
x = round(x)

# Etapa 6
T = 28
masc = np.zeros_like(imR3)
masc[y-T:y+T, x-T:x+T] = 1
imR4 = (imR3 > 0.01) * masc
axs[1, 2].imshow(imR4, cmap='gray')
axs[1, 2].set_title('6. Binarización "mascara" rosa')

# Imagen final
masc2 = 1 - imR4
imR = gris / 255.0
imG = (gris * masc2) / 255.0
imB = (gris * masc2) / 255.0
imFinal = cv2.merge([imR, imG, imB])

plt.figure()
plt.imshow(imFinal)
plt.title('Efecto publicitario buscado...')
plt.show()
