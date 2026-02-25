import tkinter as tk
from tkinter import messagebox, filedialog
import conexion as con
import shutil
import os
from PIL import Image, ImageTk

class AnadirProducto(tk.Toplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.title("Añadir Producto")
        self.geometry("400x350")
        self.callback = callback
        self.imagen_path = None
        # Mantener la ventana encima de las demás
        self.transient(master)           # hace que dependa de la ventana principal
        self.attributes('-topmost', True)
        self.lift()
        self.focus_force()

        tk.Label(self, text="Nombre:").pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        tk.Label(self, text="ID (opcional):").pack()
        self.entry_ide = tk.Entry(self)
        self.entry_ide.pack()

        tk.Label(self, text="Precio:").pack()
        self.entry_precio = tk.Entry(self)
        self.entry_precio.pack()

        tk.Label(self, text="Cantidad:").pack()
        self.entry_cantidad = tk.Entry(self)
        self.entry_cantidad.pack()

        import tkinter.font as tkfont


        tk.Button(self, text="Añadir Producto", command=self.anadir_producto).pack(pady=10)


        tk.Button(self, text="Cancelar", command=self.destroy).pack()
        tk.Button(self, text="Seleccionar Imagen", command=self.seleccionar_imagen).pack(pady=10)
        
        # Imagen por defecto
        self.logo_image = Image.open("imagenes_productos/null.webp")
        self.logo_image = self.logo_image.resize((100, 100))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
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

    def anadir_producto(self):
        nombre = self.entry_nombre.get()
        precio = self.entry_precio.get()
        cantidad = self.entry_cantidad.get()
        ide = self.entry_ide.get().strip()
        if not ide:
            messagebox.showwarning("ID requerido", "Debe ingresar un ID para el producto.")
            return
        # comprobar duplicados
        try:
            existentes = con.buscar_producto(ide)
            # buscar_producto busca por nombre; validar existencia exacta por ide
            conn = __import__('sqlite3').connect(con.DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM inventario WHERE ide = ?", (ide,))
            if cur.fetchone():
                messagebox.showerror("Error", f"Ya existe un producto con el ID '{ide}'. Elija otro ID.")
                conn.close()
                return
            conn.close()
        except Exception:
            pass

        if nombre and precio and cantidad:
            try:
                id_producto = con.anadir_producto(nombre, int(cantidad), float(precio), ide=ide)
                if self.imagen_path:
                    carpeta_destino = os.path.join(os.getcwd(), "imagenes_productos")
                    if not os.path.exists(carpeta_destino):
                        os.makedirs(carpeta_destino)
                    destino = os.path.join(carpeta_destino, f"{id_producto}.jpg")
                    shutil.copy2(self.imagen_path, destino)
                messagebox.showinfo("Éxito", "Producto añadido correctamente")
                self.callback()
                self.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")

    # dejar comportamiento de cierre por defecto (self.destroy)


