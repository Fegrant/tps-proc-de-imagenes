import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib
from Phantom import Phantom
from Radon import radon, inverse_random_transform_filters

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

radon_fig = None

# Initial variable values for the third panel
desde_3 = 0
paso_3 = 1
hasta_3 = 360
interpolacion_options = ['nearest', 'linear', 'cubic']
filtro_options = ['ramp', 'shepp-logan', 'cosine']

iradon_fig = None


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
    global radon_fig
    global phantom

    desde = float(desde_var.get())
    paso = float(paso_var.get())
    hasta = float(hasta_var.get())
    angulo = float(angulo_var.get())

    if radon_fig is None:
        radon_fig = radon(phantom.phantom, np.arange(desde, hasta, paso))
        ax2.imshow(radon_fig, cmap='Reds')
        ax2.set_title('Radon')
        ax2.colorbar = plt.colorbar(ax2.imshow(radon_fig, cmap='Reds'))
    else:
        radon_fig = radon(phantom.phantom, np.arange(desde, hasta, paso))
        ax2.imshow(radon_fig, cmap='Reds')
        ax2.set_title('Radon')

    canvas2.draw()


def update_plot3():
    global iradon_fig
    global radon_fig

    desde_3 = float(desde_var_3.get())
    paso_3 = float(paso_var_3.get())
    hasta_3 = float(hasta_var_3.get())
    interpolacion_3_value = interpolacion_3.get()
    filtro_3_value = filtro_3.get()


    if iradon_fig is None:
        iradon_fig = inverse_random_transform_filters(radon_fig, desde_3, hasta_3, paso_3, filtro_3_value,
                                             interpolacion_3_value)
        ax3.imshow(iradon_fig, cmap='Reds')
        ax3.set_title('Phantom for Third Plot')
        ax3.colorbar = plt.colorbar(ax3.imshow(iradon_fig, cmap='Reds'))
    else:
        iradon_fig = inverse_random_transform_filters(radon_fig, desde_3, hasta_3, paso_3, filtro_3_value,
                                                      interpolacion_3_value)
        ax3.imshow(iradon_fig, cmap='Reds')
        ax3.set_title(f'Interpolación: {interpolacion_3_value} - Filtro: {filtro_3_value}')

    canvas3.draw()


# Create the main application window
root = tk.Tk()
root.title("Ellipse Phantom Modifier")

# First Panel
fig1, ax1 = plt.subplots()
ax1.set_title("Ellipse Phantom")
canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.grid(row=0, column=1, sticky="nsew")

variables_frame1 = ttk.LabelFrame(root, text="Modify Variables (Panel 1)")
variables_frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

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
canvas_widget2.grid(row=1, column=1, sticky="nsew")

variables_frame2 = ttk.LabelFrame(root, text="Modify Variables (Panel 2)")
variables_frame2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

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
calculate_button.grid(row=4, column=0, columnspan=2)

# Third Panel

interpolacion_3 = tk.StringVar(value=interpolacion_options[0])
filtro_3 = tk.StringVar(value=filtro_options[0])

fig3, ax3 = plt.subplots()
ax3.set_title("Third Plot")
canvas3 = FigureCanvasTkAgg(fig3, master=root)
canvas_widget3 = canvas3.get_tk_widget()
canvas_widget3.grid(row=2, column=1, sticky="nsew")

variables_frame3 = ttk.LabelFrame(root, text="Modify Variables (Panel 3)")
variables_frame3.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

# Variables for the third panel
ttk.Label(variables_frame3, text="Desde:").grid(row=0, column=0)
desde_var_3 = tk.StringVar(value=desde_3)
ttk.Entry(variables_frame3, textvariable=desde_var_3).grid(row=0, column=1)

ttk.Label(variables_frame3, text="Paso:").grid(row=1, column=0)
paso_var_3 = tk.StringVar(value=paso_3)
ttk.Entry(variables_frame3, textvariable=paso_var_3).grid(row=1, column=1)

ttk.Label(variables_frame3, text="Hasta:").grid(row=2, column=0)
hasta_var_3 = tk.StringVar(value=hasta_3)
ttk.Entry(variables_frame3, textvariable=hasta_var_3).grid(row=2, column=1)

ttk.Label(variables_frame3, text="Interpolacion:").grid(row=3, column=0)
interpolacion_dropdown = ttk.Combobox(variables_frame3, textvariable=interpolacion_3, values=interpolacion_options)
interpolacion_dropdown.grid(row=3, column=1)

ttk.Label(variables_frame3, text="Filtro:").grid(row=4, column=0)
filtro_dropdown = ttk.Combobox(variables_frame3, textvariable=filtro_3, values=filtro_options)
filtro_dropdown.grid(row=4, column=1)

# Button to update the plot for the third panel
calculate_button_3 = ttk.Button(variables_frame3, text="Calculate", command=update_plot3)
calculate_button_3.grid(row=5, column=0, columnspan=2)

# Configure row and column weights
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the Tkinter event loop
root.mainloop()
