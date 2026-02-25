import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from anadir import AnadirProducto
import conexion as con
from PIL import Image, ImageTk
import os
import customtkinter as ctk
from ctk_button import make_ctk_button
from conexion import inicializar_base_datos
inicializar_base_datos()
ctk.set_appearance_mode("Dark")
class Inventario(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Inventario")

        # Scale window size dynamically based on screen resolution
        scale_x = self.master.winfo_screenwidth() / 1920
        scale_y = self.master.winfo_screenheight() / 1080
        font_scale = min(scale_x, scale_y)

        window_width = int(1050 * scale_x)
        window_height = int(500 * scale_y)
        self.master.geometry(f"{window_width}x{window_height}")

        self.master.configure(bg="#DBDADA")

        # Maximizar la ventana
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

        frame1 = tk.Frame(self, bg="#FFFFFF", highlightbackground="gray", highlightthickness=1)
        frame1.place(x=0 * scale_x, y=0 * scale_y, width=1920 * scale_x, height=100 * scale_y)

        titulo = tk.Label(self, text="INVENTARIO", bg="#acccdf", font=("sans", int(30 * font_scale), "bold"), anchor="center")
        titulo.place(x=5 * scale_x, y=0 * scale_y, width=1910 * scale_x, height=90 * scale_y)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", int(12 * font_scale)))
        style.configure("Treeview.Heading", font=("Arial", int(14 * font_scale), "bold"))

        self.tree = ttk.Treeview(self.master, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings", height=20)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.place(x=200 * scale_x, y=120 * scale_y, width=1250 * scale_x, height=700 * scale_y)

        numeroproducto = ctk.CTkLabel(self.master, text="Número de producto:", corner_radius=10, bg_color="#C5C4C4", fg_color="#252829", font=("Arial", int(14 * font_scale), "bold"), width=int(160 * scale_x), height=int(40 * scale_y))
        numeroproducto.place(x=1610 * scale_x, y=530 * scale_y)

        self.entry_num_producto = tk.Entry(self.master, width=20, font=("Arial", int(14 * font_scale)))
        self.entry_num_producto.place(x=1610 * scale_x, y=580 * scale_y, width=170 * scale_x, height=30 * scale_y)

        btn_cerrar = make_ctk_button(self, text="Reabastecer", command=self.sumar_cantidad_seleccionada, width=int(200 * scale_x), height=int(50 * scale_y))
        btn_cerrar.place(x=1595 * scale_x, y=620 * scale_y, width=200 * scale_x, height=50 * scale_y)

        btnañadir = make_ctk_button(self, text="Añadir", command=self.abrir_ventana_anadir, width=int(200 * scale_x), height=int(50 * scale_y))
        btnañadir.place(x=1595 * scale_x, y=700 * scale_y, width=200 * scale_x, height=50 * scale_y)

        btn_modificar = make_ctk_button(self, text="Modificar", command=self.abrir_ventana_modificar, width=int(200 * scale_x), height=int(50 * scale_y))
        btn_modificar.place(x=1595 * scale_x, y=780 * scale_y, width=200 * scale_x, height=50 * scale_y)

        barrabusqueda = ctk.CTkLabel(self.master, text="Buscar (ID o Nombre):", corner_radius=10, bg_color="#C5C4C4", fg_color="#252829", font=("Arial", int(14 * font_scale), "bold"), width=int(180 * scale_x), height=int(40 * scale_y))
        barrabusqueda.place(x=710 * scale_x, y=850 * scale_y)

        self.search_under_tree = tk.Entry(self.master, font=("Arial", int(14 * font_scale)))
        self.search_under_tree.place(x=650 * scale_x, y=900 * scale_y, width=300 * scale_x, height=30 * scale_y)

        framemarco = tk.Frame(self.master, bg="#252829", highlightbackground="white", highlightthickness=4)
        framemarco.place(x=1530 * scale_x, y=120 * scale_y, width=310 * scale_x, height=310 * scale_y)

        self.logo_image = Image.open("imagenes_productos/null.webp")
        self.logo_image = self.logo_image.resize((int(300 * scale_x), int(300 * scale_y)))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.imagen_label = tk.Label(self.master, image=self.logo_image, bg="#C6D9E3")
        self.imagen_label.place(x=1535 * scale_x, y=125 * scale_y, width=300 * scale_x, height=300 * scale_y)

        self.nombre = tk.Label(self.master, text="_________", bg="#C2C0C0", font=("Arial", int(14 * font_scale), "bold"))
        self.nombre.place(x=1535 * scale_x, y=450 * scale_y, width=300 * scale_x)
        self.nombre.config(anchor="center", justify="center")

        self.tree.bind("<<TreeviewSelect>>", self.mostrar_imagen_producto)
        self.search_under_tree.bind("<KeyRelease>", self.buscar)
        self.mostrar_todos()


    def buscar_id_nombre(self, _event=None):
        term = self.search_under_tree.get()
        resultados = con.buscar_por_id_o_nombre(term)
        self.tree.delete(*self.tree.get_children())
        for fila in resultados:
            self.tree.insert("", tk.END, values=fila)



    def abrir_ventana_anadir(self):
        ventana = AnadirProducto(self.master, self.mostrar_todos)


    def abrir_ventana_modificar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un producto en la tabla para modificar.")
            return
        item = self.tree.item(seleccion[0])
        try:
            orig_id = str(item['values'][0])
            orig_nombre = str(item['values'][1])
            orig_stock = item['values'][2]
            orig_precio = item['values'][3]
        except Exception:
            messagebox.showerror("Error", "Producto seleccionado inválido.")
            return

        self.mod_win = tk.Toplevel(self.master)
        self.mod_win.title("Modificar producto")
        self.mod_win.geometry("600x420")
        try:
            self.mod_win.transient(self.master)
            self.mod_win.focus_force()
            self.mod_win.attributes('-topmost', True)
        except Exception:
            pass

        tk.Label(self.mod_win, text="ID:").place(x=10, y=10)
        self.mod_id_entry = tk.Entry(self.mod_win, width=30)
        self.mod_id_entry.place(x=120, y=10)
        self.mod_id_entry.insert(0, orig_id)

        tk.Label(self.mod_win, text="Nombre:").place(x=10, y=50)
        self.mod_nombre_entry = tk.Entry(self.mod_win, width=30)
        self.mod_nombre_entry.place(x=120, y=50)
        self.mod_nombre_entry.insert(0, orig_nombre)

        tk.Label(self.mod_win, text="Precio:").place(x=10, y=90)
        self.mod_precio_entry = tk.Entry(self.mod_win, width=20)
        self.mod_precio_entry.place(x=120, y=90)
        self.mod_precio_entry.insert(0, str(orig_precio))

        tk.Label(self.mod_win, text=f"Stock actual: {orig_stock}").place(x=10, y=130)

        # Imagen preview
        self._mod_img_path = None
        imagen_path = f"imagenes_productos/{orig_id}.jpg"
        if not os.path.exists(imagen_path):
            imagen_path = "imagenes_productos/null.webp"
        img = Image.open(imagen_path).resize((200, 200))
        self._mod_imgtk = ImageTk.PhotoImage(img)
        self.mod_img_label = tk.Label(self.mod_win, image=self._mod_imgtk, bg="#C6D9E3")
        self.mod_img_label.place(x=350, y=10, width=200, height=200)

        def seleccionar_imagen():
            ruta = filedialog.askopenfilename(title="Seleccione imagen", filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.webp")])
            if not ruta:
                return
            try:
                imgp = Image.open(ruta).resize((200, 200))
                self._mod_imgtk = ImageTk.PhotoImage(imgp)
                self.mod_img_label.config(image=self._mod_imgtk)
                self.mod_img_label.image = self._mod_imgtk
                self._mod_img_path = ruta
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

        btn_sel_img = tk.Button(self.mod_win, text="Seleccionar imagen", command=seleccionar_imagen)
        btn_sel_img.place(x=360, y=240)

        def guardar_cambios():
            new_id = self.mod_id_entry.get().strip()
            new_nombre = self.mod_nombre_entry.get().strip()
            new_precio_text = self.mod_precio_entry.get().strip()

            if not new_id or not new_nombre:
                messagebox.showerror("Error", "ID y Nombre no pueden estar vacíos.")
                return
            try:
                new_precio = float(new_precio_text)
            except Exception:
                messagebox.showerror("Error", "Precio inválido.")
                return

            # intentar conservar stock original
            try:
                stock_val = int(orig_stock)
            except Exception:
                try:
                    stock_val = int(float(orig_stock))
                except Exception:
                    stock_val = 0

            try:
                con.modificar_producto(new_id, new_nombre, stock_val, new_precio)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el producto en BD: {e}")
                return

            # manejar imagenes: si seleccionó nueva imagen, guardarla como new_id.jpg
            try:
                dest_folder = "imagenes_productos"
                os.makedirs(dest_folder, exist_ok=True)
                dest_path = os.path.join(dest_folder, f"{new_id}.jpg")
                if self._mod_img_path:
                    img_to_save = Image.open(self._mod_img_path)
                    img_to_save.save(dest_path)
                else:
                    old_img = os.path.join(dest_folder, f"{orig_id}.jpg")
                    if orig_id != new_id and os.path.exists(old_img):
                        try:
                            os.replace(old_img, dest_path)
                        except Exception:
                            img_tmp = Image.open(old_img)
                            img_tmp.save(dest_path)
                            try:
                                os.remove(old_img)
                            except Exception:
                                pass
            except Exception as e:
                messagebox.showwarning("Aviso", f"Producto actualizado pero no se pudo actualizar la imagen: {e}")

            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
            self.mostrar_todos()
            self.mod_win.destroy()

        btn_guardar = tk.Button(self.mod_win, text="Guardar cambios", command=guardar_cambios)
        btn_guardar.place(x=120, y=180)

        btn_cancel = tk.Button(self.mod_win, text="Cancelar", command=self.mod_win.destroy)
        btn_cancel.place(x=220, y=180)




    def sumar_por_entry(self, event=None):
        # handler para bind Enter
        self.sumar_cantidad_seleccionada()

    def sumar_cantidad_seleccionada(self):
        # Obtener selección del treeview
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un producto en la tabla antes de sumar.")
            return
        item = self.tree.item(seleccion[0])
        try:
            id_prod = item['values'][0]
            nombre = item['values'][1]
            stock_actual = item['values'][2]
            precio = item['values'][3]
        except Exception:
            messagebox.showerror("Error", "Producto seleccionado inválido.")
            return

        cantidad_text = self.entry_num_producto.get()
        try:
            cantidad = int(cantidad_text)
        except Exception:
            messagebox.showerror("Error", "Ingrese un número entero válido en 'Número de producto'.")
            return
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad a sumar debe ser mayor que 0.")
            return

        try:
            nuevo_stock = int(stock_actual) + cantidad
        except Exception:
            try:
                nuevo_stock = int(float(stock_actual)) + cantidad
            except Exception:
                messagebox.showerror("Error", "Stock actual inválido en la base de datos.")
                return

        try:
            con.modificar_producto(id_prod, nombre, nuevo_stock, precio)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")
            return

        messagebox.showinfo("Éxito", f"Se sumaron {cantidad} unidades a '{nombre}'. Nuevo stock: {nuevo_stock}")
        # refrescar interfaz
        self.mostrar_todos()
        # limpiar entry
        self.entry_num_producto.delete(0, tk.END)

    def mostrar_todos(self):
        base = con.buscar_producto("")
        self.tree.delete(*self.tree.get_children())
        for fila in base:
            self.tree.insert("", tk.END, values=fila)

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


    def abrir_suma_window(self):
        self.suma_win = tk.Toplevel(self.master)
        self.suma_win.title("Sumar existencias")
        self.suma_win.geometry("700x400")
        try:
            self.suma_win.transient(self.master)
            self.suma_win.focus_force()
            self.suma_win.attributes('-topmost', True)
        except Exception:
            pass

        tk.Label(self.suma_win, text="Buscar producto:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.suma_buscar = tk.Entry(self.suma_win, width=40)
        self.suma_buscar.grid(row=1, column=0, padx=6)
        self.suma_buscar.bind("<KeyRelease>", self._suma_actualizar_sugerencias)

        # Listbox con sugerencias
        self.suma_sugerencias = tk.Listbox(self.suma_win, height=8, width=60)
        self.suma_sugerencias.grid(row=2, column=0, padx=6, pady=6)
        self.suma_sugerencias.bind("<<ListboxSelect>>", self._suma_seleccionar_producto)

        # Entrada para cantidad a sumar
        tk.Label(self.suma_win, text="Cantidad a sumar:").grid(row=3, column=0, sticky="w", padx=6, pady=(10,0))
        self.suma_cantidad = tk.Entry(self.suma_win, width=20)
        self.suma_cantidad.grid(row=4, column=0, padx=6, sticky="w")

        # Botón para confirmar suma
        self.suma_confirmar = tk.Button(self.suma_win, text="Agregar", command=self._suma_confirmar)
        self.suma_confirmar.grid(row=5, column=0, padx=6, pady=10, sticky="w")

        # Area para imagen y datos del producto seleccionado
        self.suma_imagen_label = tk.Label(self.suma_win, bg="#C6D9E3")
        self.suma_imagen_label.grid(row=0, column=1, rowspan=6, padx=10, pady=10)

        self.suma_sel_info = tk.Label(self.suma_win, text="Producto: Ninguno")
        self.suma_sel_info.grid(row=6, column=0, columnspan=2, sticky="w", padx=6)

        # Datos internos
        self._suma_producto = None  # (id, nombre, stock, precio)

        # Poblar inicialmente con todos los productos
        self._suma_actualizar_sugerencias()
        # No protocol override: dejar comportamiento por defecto

    def _suma_actualizar_sugerencias(self, _event=None):
        texto = self.suma_buscar.get() if hasattr(self, 'suma_buscar') else ""
        resultados = con.buscar_producto(texto)
        self.suma_sugerencias.delete(0, tk.END)
        for fila in resultados:
            # mostrar id - nombre - stock
            self.suma_sugerencias.insert(tk.END, f"{fila[0]} - {fila[1]} - stock:{fila[2]}")

    def _suma_seleccionar_producto(self, event=None):
        sel = self.suma_sugerencias.curselection()
        if not sel:
            return
        texto = self.suma_sugerencias.get(sel[0])
        # formato: id - nombre - stock:NN
        try:
            id_str = texto.split(" - ")[0]
            id_prod = id_str.strip()
        except Exception:
            return
        # obtener datos completos
        resultados = con.buscar_producto(id_prod)
        if not resultados:
            # intentar buscar por nombre
            resultados = con.buscar_producto(texto)
        if resultados:
            fila = resultados[0]
            self._suma_producto = fila
            nombre = fila[1]
            stock = fila[2]
            precio = fila[3]
            self.suma_sel_info.config(text=f"Producto: {nombre} | Stock actual: {stock} | Precio: {precio}")
            # cargar imagen
            ruta_imagen = f"imagenes_productos/{fila[0]}.jpg"
            if os.path.exists(ruta_imagen):
                img = Image.open(ruta_imagen)
            else:
                img = Image.open("imagenes_productos/null.webp")
            img = img.resize((200, 200))
            self._suma_imgtk = ImageTk.PhotoImage(img)
            self.suma_imagen_label.config(image=self._suma_imgtk)
            self.suma_imagen_label.image = self._suma_imgtk

    def _suma_confirmar(self):
        if not self._suma_producto:
            messagebox.showerror("Error", "No hay producto seleccionado.")
            return
        cantidad_text = self.suma_cantidad.get()
        try:
            cantidad_sumar = int(cantidad_text)
        except Exception:
            messagebox.showerror("Error", "Ingrese un número entero válido para la cantidad.")
            return
        if cantidad_sumar <= 0:
            messagebox.showerror("Error", "La cantidad a sumar debe ser mayor que 0.")
            return
        id_prod, nombre, stock_actual, precio = self._suma_producto
        try:
            nuevo_stock = int(stock_actual) + cantidad_sumar
        except Exception:
            try:
                nuevo_stock = int(float(stock_actual)) + cantidad_sumar
            except Exception:
                messagebox.showerror("Error", "Stock actual inválido en la base de datos.")
                return
        # llamar a modificar_producto para actualizar stock
        try:
            con.modificar_producto(id_prod, nombre, nuevo_stock, precio)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")
            return
        messagebox.showinfo("Éxito", f"Se sumaron {cantidad_sumar} unidades a '{nombre}'. Nuevo stock: {nuevo_stock}")
        # refrescar vista principal
        self.mostrar_todos()
        # actualizar sugerencias y limpiar cantidad
        self._suma_actualizar_sugerencias()
        self.suma_cantidad.delete(0, tk.END)

    def mostrar_nombre_producto(self, _event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            nombre_producto = item['values'][1]
            self.nombre.config(text=nombre_producto)
        else:
            self.nombre.config(text="No image")

    def buscar(self, event=None):
        nombre = self.search_under_tree.get() if hasattr(self, 'search_under_tree') else ""
        resultados = con.buscar_producto(nombre)
        self.tree.delete(*self.tree.get_children())
        for fila in resultados:
            self.tree.insert("", tk.END, values=fila)

    def borrar_producto(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            item = self.tree.item(seleccionado[0])
            id_producto = item['values'][0]
            con.borrar_producto(id_producto)
            self.mostrar_todos()
        else:
            messagebox.showwarning("Selecciona", "Selecciona un producto para borrar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Inventario(master=root)
    app.mainloop()