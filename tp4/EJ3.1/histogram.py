import cv2
import numpy as np
import matplotlib.pyplot as plt

base_path = "../image_sources/eyebw.jpg"

imagen = cv2.imread(base_path, cv2.IMREAD_GRAYSCALE)  

histograma = cv2.calcHist([imagen], [0], None, [256], [0, 256])

escalas_de_grises = list(range(256))

plt.figure()
plt.title("Histograma del ojo")
plt.xlabel("Valor de intensidad (Escala de Grises)")
plt.ylabel("Número de Píxeles")
plt.plot(escalas_de_grises, histograma)
plt.xlim([0, 255])
plt.show()