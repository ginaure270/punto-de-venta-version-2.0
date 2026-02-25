import tkinter as tk
from tkinter import messagebox, filedialog
import conexion as con
import shutil
import os
from PIL import Image, ImageTk
from ctk_button import make_ctk_button

class ModificarProducto(tk.Toplevel):
    def __init__(self, master, id_producto, nombre, precio, cantidad, callback):
        super().__init__(master)
        self.title("Modificar Producto")
        self.geometry("500x1000")
        self.id_producto = id_producto
        self.callback = callback
        self.imagen_path = None
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.lift()
        self.attributes("-topmost", True)




        tk.Label(self, text="Nombre:").pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()
        self.entry_nombre.insert(0, nombre)

        tk.Label(self, text="ID:").pack()
        self.entry_ide = tk.Entry(self)
        # intentar obtener ide actual desde la base (id_producto puede ser ide o rowid)
        try:
            conn = __import__('sqlite3').connect(con.DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT ide FROM inventario WHERE ide = ? OR rowid = ? LIMIT 1", (id_producto, id_producto))
            r = cur.fetchone()
            if r and r[0]:
                self.entry_ide.insert(0, r[0])
            conn.close()
        except Exception:
            pass
        self.entry_ide.pack()

        tk.Label(self, text="Precio:").pack()
        self.entry_precio = tk.Entry(self)
        self.entry_precio.pack()
        self.entry_precio.insert(0, precio)

        tk.Label(self, text="Cantidad:").pack()
        self.entry_cantidad = tk.Entry(self)
        self.entry_cantidad.pack()
        self.entry_cantidad.insert(0, cantidad)

        make_ctk_button(self, text="Guardar cambios", command=self.modificar_producto).pack(pady=10)
        make_ctk_button(self, text="Cancelar", command=self._on_close).pack()
        make_ctk_button(self, text="Seleccionar Imagen", command=self.seleccionar_imagen).pack(pady=10)

        # Imagen por defecto
        ruta_imagen = f"imagenes_productos/{id_producto}.jpg"
        if os.path.exists(ruta_imagen):
            imagen = Image.open(ruta_imagen)
        else:
            imagen = Image.open("imagenes_productos/null.webp")
        imagen = imagen.resize((100, 100))
        self.logo_image = ImageTk.PhotoImage(imagen)
        self.imagen_label = tk.Label(self, image=self.logo_image, bg="#C6D9E3")
        self.imagen_label.pack(pady=5)
        self.imagen_tk = self.logo_image  # Para evitar que el recolector de basura elimine la imagen

    def seleccionar_imagen(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos JPG", "*.jpg"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.imagen_path = archivo
            imagen = Image.open(archivo)
            imagen = imagen.resize((100, 100))
            self.imagen_tk = ImageTk.PhotoImage(imagen)
            self.imagen_label.config(image=self.imagen_tk)
        else:
            self.imagen_path = None
            self.imagen_label.config(image=self.logo_image)

    def modificar_producto(self):
        nombre = self.entry_nombre.get()
        precio = self.entry_precio.get()
        cantidad = self.entry_cantidad.get()
        ide = self.entry_ide.get().strip() or None
        if nombre and precio and cantidad:
            try:
                con.modificar_producto(self.id_producto, nombre, int(cantidad), float(precio), ide=ide)
                if self.imagen_path:
                    carpeta_destino = os.path.join(os.getcwd(), "imagenes_productos")
                    if not os.path.exists(carpeta_destino):
                        os.makedirs(carpeta_destino)
                    destino = os.path.join(carpeta_destino, f"{self.id_producto}.jpg")
                    shutil.copy2(self.imagen_path, destino)
                messagebox.showinfo("Éxito", "Producto modificado correctamente")
                self.callback()
                self.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")

    def _on_close(self):
        try:
            self.destroy()
        except Exception:
            pass