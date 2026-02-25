import tkinter as tk
from datetime import datetime

def actualizar_hora():
    """Actualiza la etiqueta con la fecha y hora actual cada segundo."""
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    etiqueta.config(text=fecha_hora)
    ventana.after(1000, actualizar_hora)  # Llama a la función cada 1000ms (1 segundo)

# Crear ventana
ventana = tk.Tk()
ventana.title("Fecha y Hora")
ventana.geometry("300x100")

# Crear etiqueta para mostrar la fecha y hora
etiqueta = tk.Label(ventana, font=("Arial", 16), fg="white", bg="black")


# Iniciar actualización automática
actualizar_hora()

# Ejecutar la ventana
ventana.mainloop()













