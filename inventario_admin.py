import tkinter as tk
from tkinter import ttk, messagebox
import conexion as con
from anadir import AnadirProducto
from PIL import Image, ImageTk
from ctk_button import make_ctk_button
import os

class Inventario_Admin(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Scale window size dynamically based on screen resolution
        scale_x = self.master.winfo_screenwidth() / 1920
        scale_y = self.master.winfo_screenheight() / 1080
        font_scale = min(scale_x, scale_y)

        self.master.title("Inventario Admin")
        self.master.geometry(f"{int(1920 * scale_x)}x{int(1080 * scale_y)}")
        self.master.configure(bg="#061B27")

        # Mantener la ventana por encima de las demás
        try:
            self.master.wm_attributes("-topmost", True)
            self.master.lift()
        except Exception:
            pass

        frame = tk.Frame(self.master, bg="#1F2D2E", highlightbackground="#252829", highlightthickness=2)
        frame.place(x=0 * scale_x, y=0 * scale_y, width=350 * scale_x, height=1080 * scale_y)

        try:
            self.master.state('zoomed')  # Windows
        except Exception:
            try:
                self.master.attributes('-zoomed', True)  # X11
            except Exception:
                self.master.update_idletasks()
                w = self.master.winfo_screenwidth()
                h = self.master.winfo_screenheight()
                self.master.geometry(f"{w}x{h}+0+0")

        titulo = tk.Label(self, text="Inventario", bg="#7D868B", font=("Arial", int(18 * font_scale), "bold"))
        titulo.place(x=900 * scale_x, y=30 * scale_y)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", int(12 * font_scale)))
        style.configure("Treeview.Heading", font=("Arial", int(14 * font_scale), "bold"))

        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.place(x=450 * scale_x, y=100 * scale_y, width=1000 * scale_x, height=600 * scale_y)
        self.tree.bind("<<TreeviewSelect>>", self.mostrar_imagen_producto)

        self.logo_image = Image.open("imagenes_productos/null.webp")
        self.logo_image = self.logo_image.resize((int(300 * scale_x), int(300 * scale_y)))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.imagen_label = tk.Label(self, image=self.logo_image, bg="#7D868B")
        self.imagen_label.place(x=1500 * scale_x, y=100 * scale_y, width=300 * scale_x, height=300 * scale_y)

        self.nombre = tk.Label(self, text="No image", bg="lightblue", font=("Arial", int(14 * font_scale), "bold"))
        self.nombre.place(x=1500 * scale_x, y=420 * scale_y, width=300 * scale_x)
        self.nombre.config(anchor="center", justify="center")

        self.textbox1label = tk.Label(self, text="Buscar Producto:", bg="#7D868B", font=("Arial", int(14 * font_scale), "bold"))
        self.textbox1label.place(x=870 * scale_x, y=720 * scale_y, width=200 * scale_x, height=30 * scale_y)
        self.textbox1label.config(anchor="center", justify="center")

        self.textbox1 = tk.Entry(self, width=80, font=("Arial", int(14 * font_scale), "bold"))
        self.textbox1.place(x=820 * scale_x, y=760 * scale_y, width=300 * scale_x, height=34 * scale_y)
        self.textbox1.config(justify="center")
        self.textbox1.bind("<KeyRelease>", self.buscar)

        btnañadir = make_ctk_button(frame, text="Añadir", command=self.abrir_ventana_anadir, width=int(240 * scale_x), height=int(70 * scale_y))
        btnañadir.place(x=50 * scale_x, y=730 * scale_y, width=240 * scale_x, height=60 * scale_y)

        btn_modificar = make_ctk_button(frame, text="Modificar", command=self.abrir_ventana_modificar, width=int(240 * scale_x), height=int(70 * scale_y))
        btn_modificar.place(x=50 * scale_x, y=330 * scale_y, width=240 * scale_x, height=60 * scale_y)

        btn_borrar = make_ctk_button(frame, text="Borrar", command=self.borrar_producto, width=int(240 * scale_x), height=int(70 * scale_y))
        btn_borrar.place(x=50 * scale_x, y=530 * scale_y, width=240 * scale_x, height=60 * scale_y)

        self.mostrar_todos()

    def buscar(self, event=None):
        nombre = self.textbox1.get()
        resultados = con.buscar_producto(nombre)
        self.tree.delete(*self.tree.get_children())
        for fila in resultados:
            self.tree.insert("", tk.END, values=fila)

    def mostrar_todos(self):
        base = con.buscar_producto("")
        self.tree.delete(*self.tree.get_children())
        for fila in base:
            self.tree.insert("", tk.END, values=fila)

    def borrar_producto(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            item = self.tree.item(seleccionado)
            id_producto = item['values'][0]
            con.borrar_producto(id_producto)
            self.mostrar_todos()
        else:
            messagebox.showwarning("Selecciona", "Selecciona un producto para borrar.")

    def abrir_ventana_anadir(self):
        ventana = AnadirProducto(self.master, self.mostrar_todos)

    def abrir_ventana_modificar(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            item = self.tree.item(seleccionado)
            id_producto = item['values'][0]
            nombre = item['values'][1]
            cantidad = item['values'][2]
            precio = item['values'][3]
            from modificar import ModificarProducto
            ventana = ModificarProducto(self.master, id_producto, nombre, precio, cantidad, self.mostrar_todos)
        else:
            messagebox.showwarning("Selecciona", "Selecciona un producto para modificar.")

    def mostrar_imagen_producto(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            id_producto = item['values'][0]
            ruta_imagen = f"imagenes_productos/{id_producto}.jpg"
            if os.path.exists(ruta_imagen):
                imagen = Image.open(ruta_imagen)
            else:
                imagen = Image.open("imagenes_productos/null.webp")
            imagen = imagen.resize((300, 300))
            self.imagen_tk = ImageTk.PhotoImage(imagen)
            self.imagen_label.config(image=self.imagen_tk)
            self.imagen_label.image = self.imagen_tk  

        self.mostrar_nombre_producto(event)

    def mostrar_nombre_producto(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            nombre_producto = item['values'][1]
            self.nombre.config(text=nombre_producto)
        else:
            self.nombre.config(text="No image")







