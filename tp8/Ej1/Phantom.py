import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')


class Phantom:
    def __init__(self, intensidad=0.6, inclinacion=180, semi_eje_x=0.3, semi_eje_y=0.4, centro_x=0.2, centro_y=1.0,
                 size=256):
        self.centro_y = centro_y
        self.centro_x = centro_x
        self.semi_eje_y = semi_eje_y
        self.semi_eje_x = semi_eje_x
        self.intensidad = intensidad
        self.inclinacion = inclinacion
        self.size = size
        self.phantom = np.zeros((size, size))

    def create_ellipse_phantom(self):
        # Calcular los parámetros de la elipse
        a = self.semi_eje_x * self.size / 2
        b = self.semi_eje_y * self.size / 2
        theta = np.radians(self.inclinacion)
        cx = (self.centro_x + 1) * self.size / 2
        cy = (self.centro_y + 1) * self.size / 2

        # Generar puntos en la elipse
        y, x = np.ogrid[0:self.size, 0:self.size]
        x_rot = (x - cx) * np.cos(theta) - (y - cy) * np.sin(theta)
        y_rot = (x - cx) * np.sin(theta) + (y - cy) * np.cos(theta)

        # Aplicar condición a cada punto individual
        mask = (x_rot / a) ** 2 + (y_rot / b) ** 2 <= 1

        # Agregar la intensidad solo a la región de la elipse
        self.phantom[mask] += self.intensidad

    def add_ellipse_phantom(self, intensidad=0.6, inclinacion=180, semi_eje_x=0.3, semi_eje_y=0.4, centro_x=0.2,
                            centro_y=1.0):
        # Calcular los parámetros de la elipse
        a = semi_eje_x * self.size / 2
        b = semi_eje_y * self.size / 2
        theta = np.radians(inclinacion)
        cx = (centro_x + 1) * self.size / 2
        cy = (centro_y + 1) * self.size / 2

        # Generar puntos en la elipse
        y, x = np.ogrid[0:self.size, 0:self.size]
        x_rot = (x - cx) * np.cos(theta) - (y - cy) * np.sin(theta)
        y_rot = (x - cx) * np.sin(theta) + (y - cy) * np.cos(theta)

        # Aplicar condición a cada punto individual
        mask = (x_rot / a) ** 2 + (y_rot / b) ** 2 <= 1

        # Agregar la intensidad solo a la región de la elipse
        self.phantom[mask] += intensidad
