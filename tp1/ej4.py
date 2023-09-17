import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Crear una figura y un eje
fig, ax = plt.subplots()

color_1 = 97 / 255
color_2 = 187 / 255
color_variable = 110 / 255

square1_outside = (color_1, color_1, color_1)
square2_outside = (color_2, color_2, color_2)
square_fixed_inside = (0.5, 0.5, 0.5)
square_variable_inside = (color_variable, color_variable, color_variable)

# Crear un cuadrado personalizado como un objeto Patch
square_1 = patches.Rectangle((0.2, 0.2), 0.8, 0.8, facecolor=square1_outside)
square_1_inside = patches.Rectangle((0.4, 0.4), 0.4, 0.4, facecolor=square_variable_inside)

# Crear un cuadrado personalizado como un objeto Patch
square_2 = patches.Rectangle((1.2, 0.2), 0.8, 0.8, facecolor=square2_outside)
square_2_inside = patches.Rectangle((1.4, 0.4), 0.4, 0.4, facecolor=square_fixed_inside)

# Agregar el cuadrado al eje
ax.add_patch(square_1)
ax.add_patch(square_1_inside)
ax.add_patch(square_2)
ax.add_patch(square_2_inside)

# Mostrar el gráfico
plt.axis('equal')
plt.show()