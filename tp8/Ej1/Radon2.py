import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import iradon, radon
from skimage.data import shepp_logan_phantom

phantom = shepp_logan_phantom()

# Mostrar la imagen original (phantom)
plt.imshow(phantom, cmap='gray')
plt.title('Phantom Shepp-Logan')
plt.show()

start_angle = 0
end_angle = 180
angle_step = 1

# Transformada de Radon
radon_transform = radon(phantom, np.arange(start_angle, end_angle, angle_step))

# Mostrar la Transformada de Radon
plt.imshow(radon_transform, cmap='gray')
plt.title('Transformada de Radon')
plt.show()

# Seleccionar parámetros para la transformada inversa de Radon
filter_types = ['ramp', 'shepp-logan', 'cosine']
interpolation_methods = ['nearest', 'linear', 'cubic']

# Calcular la cantidad de subplots necesarios
num_subplots = len(filter_types) * len(interpolation_methods)

for i, filter_type in enumerate(filter_types, 1):    
    for j, interp_method in enumerate(interpolation_methods, 1):
        # Aplicar la transformada inversa de Radon con el filtro actual
        inverse_radon_transform = iradon(radon_transform, theta=np.arange(start_angle, end_angle, angle_step),
                                         filter_name=filter_type, interpolation=interp_method)

        # Mostrar cada imagen por separado
        plt.imshow(inverse_radon_transform, cmap='gray', vmin=phantom.min(), vmax=phantom.max())  # Escala consistente
        plt.title(f'Interpolación: {interp_method} - Filtro: {filter_type}')
        plt.show()
