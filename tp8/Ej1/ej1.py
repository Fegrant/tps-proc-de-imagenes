import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')


def create_ellipse_phantom(intensidad, inclinacion, semi_eje_x, semi_eje_y, centro_x, centro_y, size=256):
    # Crear una imagen en blanco
    phantom = np.zeros((size, size))

    # Calcular los parámetros de la elipse
    a = semi_eje_x * size / 2
    b = semi_eje_y * size / 2
    theta = np.radians(inclinacion)
    cx = (centro_x + 1) * size / 2
    cy = (centro_y + 1) * size / 2

    # Generar puntos en la elipse
    y, x = np.ogrid[0:size, 0:size]
    x_rot = (x - cx) * np.cos(theta) - (y - cy) * np.sin(theta)
    y_rot = (x - cx) * np.sin(theta) + (y - cy) * np.cos(theta)

    # Aplicar condición a cada punto individual
    mask = (x_rot / a) ** 2 + (y_rot / b) ** 2 <= 1

    # Agregar la intensidad solo a la región de la elipse
    phantom[mask] += intensidad

    return phantom


# Ejemplo de uso
intensidad = 0.6
inclinacion = 180  # grados
semi_eje_x = 0.3
semi_eje_y = 0.4
centro_x = 0.2
centro_y = 1

phantom = create_ellipse_phantom(intensidad, inclinacion, semi_eje_x, semi_eje_y, centro_x, centro_y)

# Mostrar el phantom
plt.imshow(phantom, cmap='Blues')
plt.colorbar()
plt.title('Phantom de Elipse')
plt.show()