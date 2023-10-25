import cv2
import numpy as np
import os

results_dir = 'results/'

if not os.path.exists(results_dir):
    os.makedirs(results_dir)

def apply_opening(image_path, kernel_size):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    kernel = np.zeros((2*kernel_size+1, 2*kernel_size+1), dtype=np.uint8)
    cv2.circle(kernel, (kernel_size, kernel_size), kernel_size, 1, -1)

    # Aplico erosión seguida de dilatación
    opened_image = cv2.erode(image, kernel, iterations=1)
    opened_image = cv2.dilate(opened_image, kernel, iterations=1)

    cv2.imwrite(results_dir + 'original.jpg', image)
    cv2.imwrite(results_dir + 'opened_' + str(kernel_size) + '.jpg', opened_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_path = '../image_sources/image_3.jpg'
kernel_size = int(input("Ingresa el radio del elemento estructural: "))

apply_opening(image_path, kernel_size)
