import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib

matplotlib.use('TkAgg')

# Initial variable values
intensidad = 0.6
inclinacion = 180  # degrees
semi_eje_x = 0.3
semi_eje_y = 0.4
centro_x = 0.2
centro_y = 0.5

# Initialize a list to store the artists
phantoms = []

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
    y, x = np.ogrid[-a:size - a, -b:size - b]
    mask = (x * np.cos(theta) + y * np.sin(theta)) ** 2 / a ** 2 + (
            y * np.cos(theta) - x * np.sin(theta)) ** 2 / b ** 2 <= 1

    # Agregar la intensidad a la región de la elipse
    phantom[mask] += intensidad

    return phantom


def update_plot():
    global phantoms  # Use the global imshow object

    # Get the updated variable values
    intensidad = float(intensidad_var.get())
    inclinacion = float(inclinacion_var.get())
    semi_eje_x = float(semi_eje_x_var.get())
    semi_eje_y = float(semi_eje_y_var.get())
    centro_x = float(centro_x_var.get())
    centro_y = float(centro_y_var.get())

    # Create the ellipse phantom using the provided function
    phantom = create_ellipse_phantom(intensidad, inclinacion, semi_eje_x, semi_eje_y, centro_x, centro_y)

    if not phantoms:
        phantoms.append(phantom)
        plt.imshow(phantom, cmap='Blues')
        plt.colorbar()
    else:
        phantoms.append(phantom)
        for p in phantoms:
            plt.imshow(p, cmap='Blues')

    plt.title('Phantom de Elipse')
    canvas.draw()


# Create the main application window
root = tk.Tk()
root.title("Ellipse Phantom Modifier")

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()
ax.set_title("Ellipse Phantom")

# Embed Matplotlib figure in Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create labels and entry widgets for variable modification
variables_frame = ttk.LabelFrame(root, text="Modify Variables")
variables_frame.pack(padx=10, pady=10, side=tk.BOTTOM)

# Intensidad
ttk.Label(variables_frame, text="Intensidad:").grid(row=0, column=0)
intensidad_var = tk.StringVar(value=intensidad)
ttk.Entry(variables_frame, textvariable=intensidad_var).grid(row=0, column=1)

# Inclinacion
ttk.Label(variables_frame, text="Inclinacion:").grid(row=1, column=0)
inclinacion_var = tk.StringVar(value=inclinacion)
ttk.Entry(variables_frame, textvariable=inclinacion_var).grid(row=1, column=1)

# Semi Eje X
ttk.Label(variables_frame, text="Semi Eje X:").grid(row=2, column=0)
semi_eje_x_var = tk.StringVar(value=semi_eje_x)
ttk.Entry(variables_frame, textvariable=semi_eje_x_var).grid(row=2, column=1)

# Semi Eje Y
ttk.Label(variables_frame, text="Semi Eje Y:").grid(row=3, column=0)
semi_eje_y_var = tk.StringVar(value=semi_eje_y)
ttk.Entry(variables_frame, textvariable=semi_eje_y_var).grid(row=3, column=1)

# Centro X
ttk.Label(variables_frame, text="Centro X:").grid(row=4, column=0)
centro_x_var = tk.StringVar(value=centro_x)
ttk.Entry(variables_frame, textvariable=centro_x_var).grid(row=4, column=1)

# Centro Y
ttk.Label(variables_frame, text="Centro Y:").grid(row=5, column=0)
centro_y_var = tk.StringVar(value=centro_y)
ttk.Entry(variables_frame, textvariable=centro_y_var).grid(row=5, column=1)
# Button to update the plot
update_button = ttk.Button(variables_frame, text="Update Plot", command=update_plot)
update_button.grid(row=6, column=0, columnspan=2)

# Start the Tkinter event loop
root.mainloop()
