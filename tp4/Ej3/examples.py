import cv2
import matplotlib.pyplot as plt
import os

def show_all_bitplanes(image_url, exercise):
    fig, ax = plt.subplots(2, 4, figsize=(25, 10))
    imagen = cv2.imread(image_url, cv2.IMREAD_GRAYSCALE)

    # Seteo el numero de bits de la imagen, y aplico una máscara para quedarme con el bit i-ésimo
    num_bits = 8
    bit_planes = [((imagen >> i) & 1) * 255 for i in range(num_bits)]

    for i, bit_plane in enumerate(bit_planes):
        plt.subplot(2, 4, i + 1)
        plt.imshow(bit_plane, cmap='gray')
        plt.title(f'Bit Plane {i}')

    plt.savefig(f'results/bit_planes_{exercise}.png')


if not os.path.exists('results'):
    os.makedirs('results')

imagen_3a = '../image_sources/8 bit fractal.png'
imagen_3b = '../image_sources/onedollar.jpg'
show_all_bitplanes(imagen_3a, '3a')
show_all_bitplanes(imagen_3b, '3b')