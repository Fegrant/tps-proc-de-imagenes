import numpy as np
import matplotlib.pyplot as plt

from skimage.transform import iradon, warp
from ej1 import create_ellipse_phantom


def pad_image(image):
    diagonal = np.sqrt(2) * max(image.shape)
    pad = [int(np.ceil(diagonal - s)) for s in image.shape]
    new_center = [(s + p) // 2 for s, p in zip(image.shape, pad)]
    old_center = [s // 2 for s in image.shape]
    pad_before = [nc - oc for oc, nc in zip(old_center, new_center)]
    pad_width = [(pb, p - pb) for pb, p in zip(pad_before, pad)]
    return np.pad(image, pad_width, mode='constant', constant_values=0)

def radon(image, theta):
    # image: la imagen de entrada (phantom)
    # theta: ángulos de proyección en grados

    image = np.float64(image)

    padded_image = pad_image(image)
    center = padded_image.shape[0] // 2
    radon_image = np.zeros((padded_image.shape[0], len(theta)), dtype=image.dtype)

    for i, angle in enumerate(np.deg2rad(theta)):
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        R = np.array(
            [
                [cos_a, sin_a, -center * (cos_a + sin_a - 1)],
                [-sin_a, cos_a, -center * (cos_a - sin_a - 1)],
                [0, 0, 1],
            ]
        )
        rotated = warp(padded_image, R, clip=False)
        radon_image[:, i] = rotated.sum(0)
    return radon_image


# Creación del phantom
intensidad = 0.6
inclinacion = 180  # grados
semi_eje_x = 0.3
semi_eje_y = 0.4
centro_x = 0.2
centro_y = 0.5

phantom = create_ellipse_phantom(intensidad, inclinacion, semi_eje_x, semi_eje_y, centro_x, centro_y)

start_angle = 0
end_angle = 180
angle_step = 1

radon_transform = radon(phantom, np.arange(start_angle, end_angle, angle_step))

plt.imshow(radon_transform, cmap='gray')
plt.title('Transformada de Radon')
plt.show()

# Transformada inversa
filter_type = 'ramp'
interpolation = 'linear'

inverse_radon_transform = iradon(radon_transform, theta=np.arange(start_angle, end_angle, angle_step), circle=False, filter_name=filter_type, interpolation=interpolation)

plt.imshow(inverse_radon_transform, cmap='gray')
plt.title('Transformada inversa de Radon')
plt.show()


def inverse_random_transform_filters(radon_transform, start_angle, end_angle, angle_step):

    filter_types = ['ramp', 'shepp-logan', 'cosine']
    interpolation = 'linear'  # Método de interpolación (puedes cambiarlo según tus necesidades)

    # Crear subplots para mostrar imágenes reconstruidas con diferentes filtros
    plt.figure(figsize=(15, 5))

    for i, filter_type in enumerate(filter_types, 1):
        # Aplicar la transformada inversa de Radon con el filtro actual
        inverse_radon_transform = iradon(radon_transform, theta=np.arange(start_angle, end_angle, angle_step),
                                        filter_name=filter_type, interpolation=interpolation)

        # Mostrar la imagen reconstruida en un subplot
        plt.subplot(1, len(filter_types), i)
        plt.imshow(inverse_radon_transform, cmap='gray')
        plt.title(f'Transformada inversa de Radon\nFiltro: {filter_type}')

    plt.tight_layout()
    plt.show()