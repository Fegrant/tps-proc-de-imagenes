import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib
from Phantom import Phantom

matplotlib.use('TkAgg')

# Initial variable values
intensidad = 0.6
inclinacion = 180  # degrees
semi_eje_x = 0.3
semi_eje_y = 0.4
centro_x = 0.2
centro_y = 0.5

phantom = None

# Initial variable values for the second panel
desde = 0
paso = 1
hasta = 360
angulo = 0

phantom2 = None


def update_plot():
    global phantom  # Use the global imshow object

    # Get the updated variable values
    intensidad = float(intensidad_var.get())
    inclinacion = float(inclinacion_var.get())
    semi_eje_x = float(semi_eje_x_var.get())
    semi_eje_y = float(semi_eje_y_var.get())
    centro_x = float(centro_x_var.get())
    centro_y = float(centro_y_var.get())

    if phantom is None:
        phantom = Phantom(intensidad, inclinacion, semi_eje_x, semi_eje_y, centro_x, centro_y)
        phantom.create_ellipse_phantom()
        ax1.imshow(phantom.phantom, cmap='Reds')
        ax1.colorbar = plt.colorbar(ax1.imshow(phantom.phantom, cmap='Reds'))
    else:
        phantom.add_ellipse_phantom(intensidad, inclinacion, semi_eje_x, semi_eje_y, centro_x, centro_y)
        ax1.imshow(phantom.phantom, cmap='Reds')

    plt.title('Phantom de Elipse')
    canvas1.draw()


def update_plot2():
    global phantom2

    desde = float(desde_var.get())
    paso = float(paso_var.get())
    hasta = float(hasta_var.get())
    angulo = float(angulo_var.get())

    # Your calculation logic for the second plot goes here
    # Example: Create a phantom based on the provided variables
    if phantom2 is None:
        phantom2 = Phantom()  # Replace this with your logic
        ax2.imshow(phantom2.phantom, cmap='Reds')
        ax2.set_title('Phantom for Second Plot')
        ax2.colorbar = plt.colorbar(ax2.imshow(phantom2.phantom, cmap='Reds'))
    else:
        # Update the phantom based on the modified variables
        # Replace this with your logic
        phantom2.update_phantom(desde, paso, hasta, angulo)
        ax2.imshow(phantom2.phantom, cmap='Reds')

    canvas2.draw()


# Create the main application window
root = tk.Tk()
root.title("Ellipse Phantom Modifier")

# First Panel
fig1, ax1 = plt.subplots()
ax1.set_title("Ellipse Phantom")
canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

variables_frame1 = ttk.LabelFrame(root, text="Modify Variables (Panel 1)")
variables_frame1.pack(padx=10, pady=10, side=tk.LEFT)

# Intensidad
ttk.Label(variables_frame1, text="Intensidad:").grid(row=0, column=0)
intensidad_var = tk.StringVar(value=intensidad)
ttk.Entry(variables_frame1, textvariable=intensidad_var).grid(row=0, column=1)

# Inclinacion
ttk.Label(variables_frame1, text="Inclinacion:").grid(row=1, column=0)
inclinacion_var = tk.StringVar(value=inclinacion)
ttk.Entry(variables_frame1, textvariable=inclinacion_var).grid(row=1, column=1)

# Semi Eje X
ttk.Label(variables_frame1, text="Semi Eje X:").grid(row=2, column=0)
semi_eje_x_var = tk.StringVar(value=semi_eje_x)
ttk.Entry(variables_frame1, textvariable=semi_eje_x_var).grid(row=2, column=1)

# Semi Eje Y
ttk.Label(variables_frame1, text="Semi Eje Y:").grid(row=3, column=0)
semi_eje_y_var = tk.StringVar(value=semi_eje_y)
ttk.Entry(variables_frame1, textvariable=semi_eje_y_var).grid(row=3, column=1)

# Centro X
ttk.Label(variables_frame1, text="Centro X:").grid(row=4, column=0)
centro_x_var = tk.StringVar(value=centro_x)
ttk.Entry(variables_frame1, textvariable=centro_x_var).grid(row=4, column=1)

# Centro Y
ttk.Label(variables_frame1, text="Centro Y:").grid(row=5, column=0)
centro_y_var = tk.StringVar(value=centro_y)
ttk.Entry(variables_frame1, textvariable=centro_y_var).grid(row=5, column=1)
# Button to update the plot
update_button = ttk.Button(variables_frame1, text="Update Plot", command=update_plot)
update_button.grid(row=6, column=0, columnspan=2)

# Second Panel
fig2, ax2 = plt.subplots()
ax2.set_title("Second Plot")
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

variables_frame2 = ttk.LabelFrame(root, text="Modify Variables (Panel 2)")
variables_frame2.pack(padx=10, pady=10, side=tk.RIGHT)

# Variables for the second panel
ttk.Label(variables_frame2, text="Desde:").grid(row=0, column=0)
desde_var = tk.StringVar(value=desde)
ttk.Entry(variables_frame2, textvariable=desde_var).grid(row=0, column=1)

ttk.Label(variables_frame2, text="Paso:").grid(row=1, column=0)
paso_var = tk.StringVar(value=paso)
ttk.Entry(variables_frame2, textvariable=paso_var).grid(row=1, column=1)

ttk.Label(variables_frame2, text="Hasta:").grid(row=2, column=0)
hasta_var = tk.StringVar(value=hasta)
ttk.Entry(variables_frame2, textvariable=hasta_var).grid(row=2, column=1)

ttk.Label(variables_frame2, text="Angulo:").grid(row=3, column=0)
angulo_var = tk.StringVar(value=angulo)
ttk.Entry(variables_frame2, textvariable=angulo_var).grid(row=3, column=1)

calculate_button = ttk.Button(variables_frame2, text="Calculate", command=update_plot2)
calculate_button.grid(row=6, column=0, columnspan=2)

# Start the Tkinter event loop
root.mainloop()
