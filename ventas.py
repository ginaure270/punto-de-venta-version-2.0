import sqlite3
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import conexion as con
from generar_recibo_cierre import generate_and_save_receipt
from mover_cierre import migrar_ventas_a_cierre
import os
from anadir import AnadirProducto
from PIL import Image, ImageTk  
import os  
from tkinter import LabelFrame
from datetime import datetime
from globales import usd_rate
from ctk_button import make_ctk_button
from PIL import Image, ImageTk
from globales import usd_rate, last_update



class Ventas(tk.Frame):
    db_name = "database_ventas.db"

    def __init__(self, parent):
        super().__init__(parent)

        # Calculate scaling factors based on screen resolution
        self.scale_x = self.winfo_screenwidth() / 1920
        self.scale_y = self.winfo_screenheight() / 1080

        # No forzar 'topmost' aquí para permitir que los pop-ups se muestren encima
        self.numero_factura_actual = self.obtener_numero_factura_actual()
        # Mapa para guardar los valores originales (en USD) por item id del Treeview
        self.original_values = {}
        self.widgets()

        parent.state("zoomed")

        self.etiqueta_hora = tk.Label(self, font=("Arial", int(16 * self.scale_y)), fg="white", bg="#556C79")
        self.etiqueta_hora.place(x=int(1700 * self.scale_x), y=int(10 * self.scale_y), width=int(200 * self.scale_x), height=int(40 * self.scale_y))

        def actualizar_hora():
            fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.etiqueta_hora.config(text=fecha_hora)
            self.after(1000, actualizar_hora)

        actualizar_hora()

    def widgets(self):
        frame1 = tk.Frame(self, bg="#FFFFFF", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=int(1920 * self.scale_x), height=int(100 * self.scale_y))

        titulo = tk.Label(self, text="VENTAS", bg="#acccdf", font=("sans", int(30 * self.scale_y), "bold"), anchor="center")
        titulo.pack()
        titulo.place(x=int(5 * self.scale_x), y=0, width=int(1910 * self.scale_x), height=int(90 * self.scale_y))

        frame2 = tk.Frame(self, bg="#C0C0C0", highlightbackground="gray", highlightthickness=4)
        frame2.place(x=int(350 * self.scale_x), y=int(100 * self.scale_y), width=int(1700 * self.scale_x), height=int(920 * self.scale_y))

        lblframe5 = LabelFrame(self, text="Opciones", bg="#689CB8", font=("sans", int(15 * self.scale_y), "bold"), labelanchor='n')
        lblframe5.place(x=0, y=int(350 * self.scale_y), width=int(350 * self.scale_x), height=int(660 * self.scale_y))

        lblframe = LabelFrame(frame2, text=" Informacion de la venta", bg="#9AB8C9", font=("sans", int(15 * self.scale_y), "bold"), highlightbackground="gray", highlightthickness=5)
        lblframe.place(x=int(50 * self.scale_x), y=int(20 * self.scale_y), width=int(1000 * self.scale_x), height=int(100 * self.scale_y))

        label_nombre = ctk.CTkLabel(lblframe, text="Productos:", corner_radius=10, fg_color="#FF9133", bg_color="#9AB8C9", text_color="white", font=("sans", int(14 * self.scale_y), "bold"))
        label_nombre.pack(padx=5, pady=5)
        label_nombre.place(x=int(10 * self.scale_x), y=int(15 * self.scale_y))

        # Campo de búsqueda: Entry con lista de sugerencias
        self.entry_nombre = ttk.Entry(lblframe, font=("sans", int(12 * self.scale_y), "bold"))
        self.entry_nombre.place(x=int(110 * self.scale_x), y=int(15 * self.scale_y), width=int(160 * self.scale_x), height=int(30 * self.scale_y))

        # Listbox de sugerencias (inicialmente oculto)
        self.suggestion_box = tk.Listbox(lblframe, font=("sans", int(10 * self.scale_y)), height=5, bg="white", fg="black")
        self.suggestion_box.place_forget()

        # Bind para buscar mientras se escribe y para selección
        self.entry_nombre.bind('<KeyRelease>', self._on_nombre_key)

        # Al pulsar Enter en la barra de búsqueda, añadir automáticamente cantidad=1
        self.entry_nombre.bind('<Return>', self._on_nombre_enter)
        self.suggestion_box.bind('<<ListboxSelect>>', self._on_suggestion_select)

        self.cargar_productos()

        label_valor = ctk.CTkLabel(lblframe, text="Precio:", corner_radius=10, fg_color="#FF9133", bg_color="#9AB8C9", text_color="white", font=("sans", int(14 * self.scale_y), "bold"))
        label_valor.pack(padx=5, pady=5)
        label_valor.place(x=int(280 * self.scale_x), y=int(15 * self.scale_y))

        self.entry_valor = ttk.Entry(lblframe, font=("sans", int(12 * self.scale_y), "bold"), state="readonly")
        self.entry_valor.place(x=int(350 * self.scale_x), y=int(15 * self.scale_y), width=int(180 * self.scale_x), height=int(30 * self.scale_y))

        label_cantidad = ctk.CTkLabel(lblframe, text="Cantidad:", corner_radius=10, fg_color="#FF9133", bg_color="#9AB8C9", text_color="white", font=("sans", int(14 * self.scale_y), "bold"))
        label_cantidad.pack(padx=5, pady=5)
        label_cantidad.place(x=int(540 * self.scale_x), y=int(15 * self.scale_y))

        self.entry_cantidad = ttk.Entry(lblframe, font=("sans", int(12 * self.scale_y), "bold"))
        self.entry_cantidad.place(x=int(630 * self.scale_x), y=int(15 * self.scale_y), width=int(100 * self.scale_x), height=int(30 * self.scale_y))

        treFrame = tk.Frame(frame2, bg="#3C5A44", highlightbackground="gray", highlightthickness=1)
        treFrame.place(x=int(50 * self.scale_x), y=int(150 * self.scale_y), width=int(1000 * self.scale_x), height=int(500 * self.scale_y))

        scrol_y = ttk.Scrollbar(treFrame, orient="vertical")
        scrol_y.pack(side="right", fill="y")

        scrol_x = ttk.Scrollbar(treFrame, orient="horizontal")
        scrol_x.pack(side="bottom", fill="x")

        # Estilo personalizado para aumentar la fuente del Treeview
        style = ttk.Style()
        try:
            style.configure("Ventas.Treeview", font=("Sans", int(12 * self.scale_y)))
            style.configure("Ventas.Treeview.Heading", font=("Sans", int(13 * self.scale_y), "bold"))
            tree_style = "Ventas.Treeview"
        except Exception:
            tree_style = None

        self.tree = ttk.Treeview(treFrame, columns=("Producto", "Precio", "Cantidad", "Subtotal"), show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, style=tree_style)
        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)

        self.tree.heading("#1", text="Producto")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Subtotal")

        self.tree.column("Producto", anchor="center")
        self.tree.column("Precio", anchor="center")
        self.tree.column("Cantidad", anchor="center")
        self.tree.column("Subtotal", anchor="center")

        self.tree.pack(expand=True, fill="both")

        lblframe1 = LabelFrame(lblframe5, bg="#689CB8", font="sans 12 bold")
        lblframe1.place(x=0, y=int(120 * self.scale_y), width=int(1060 * self.scale_x), height=int(600 * self.scale_y))

        logoframe = tk.Frame(self, bg="#acccdf")
        logoframe.pack()
        logoframe.place(x=0, y=0, width=int(350 * self.scale_x), height=int(350 * self.scale_y))

        # Scale images proportionally using the smaller axis scale to preserve aspect ratio
        _img_scale = min(self.scale_x, self.scale_y)

        # Logo image (scaled)
        try:
            logo_w = max(1, int(300 * _img_scale))
            logo_h = max(1, int(300 * _img_scale))
            self.logo_image = Image.open("imagenes/logotipo.png")
            self.logo_image = self.logo_image.resize((logo_w, logo_h))
            self.logo_image = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self, image=self.logo_image, bg="#acccdf")
            self.logo_label.place(x=int(25 * self.scale_x), y=int(30 * self.scale_y))
        except Exception:
            pass

        # Approved/check image (small icon, scaled)
        try:
            aprobado_w = max(1, int(25 * _img_scale))
            aprobado_h = max(1, int(25 * _img_scale))
            self.aprobado = Image.open("imagenes/aprobado.png")
            self.aprobado = self.aprobado.resize((aprobado_w, aprobado_h))
            self.aprobado = ImageTk.PhotoImage(self.aprobado)
            self.aprobado_label = tk.Label(self, image=self.aprobado, bg="#C0C0C0")
            self.aprobado_label.place(x=int(450 * self.scale_x), y=int(900 * self.scale_y))
        except Exception:
            pass

        label_update = tk.Label(frame2, text=f"Última actualización: {last_update}", bg="#C0C0C0", fg="white", font=("sans", int(12 * self.scale_y), "bold"))
        label_update.place(x=int(125 * self.scale_x), y=int(800 * self.scale_y))

        label_usd = ctk.CTkLabel(frame2, text=f"Tasa de cambio USD: {usd_rate} Bs.S.", corner_radius=10, fg_color="#FFFFFF",bg_color="#C0C0C0", text_color="#143866", width=int(350 * self.scale_x), height=int(50 * self.scale_y), font=("Arial", int(20 * self.scale_y), "bold"))
        label_usd.pack(padx=20, pady=20)
        label_usd.place(x=int(100 * self.scale_x), y=int(700 * self.scale_y))

        boton_pagar = make_ctk_button(lblframe5, text="Confirmar Pago", command=self.pagar_y_facturar, width=int(270 * self.scale_x), height=int(70 * self.scale_y), primary_color="#1CC96D", text_color="white", font=("sans", int(22 * self.scale_y), "bold"))
        boton_pagar.pack(padx=4, pady=4)
        boton_pagar.place(x=int(35 * self.scale_x), y=int(20 * self.scale_y))

        boton_limpiar = make_ctk_button(lblframe1, text="Limpiar Lista", command=self.limpiar_treeview, width=int(270 * self.scale_x), height=int(70 * self.scale_y), primary_color="#ED4040", text_color="white", font=("sans", int(22 * self.scale_y), "bold"))
        boton_limpiar.pack(padx=4, pady=4)
        boton_limpiar.place(x=int(35 * self.scale_x), y=int(30 * self.scale_y))

        boton_agregar = make_ctk_button(lblframe, text="Agg Articulo", command=self.registrar, width=int(100 * self.scale_x), height=int(40 * self.scale_y), primary_color="#1CC96D", text_color="white", font=("sans", int(22 * self.scale_y), "bold"))
        boton_agregar.pack(padx=4, pady=4)
        boton_agregar.place(x=int(760 * self.scale_x), y=int(5 * self.scale_y))

        boton_ver_facturas = make_ctk_button(lblframe1, text="Ver Facturas", command=self.abrir_ventana_factura, width=int(270 * self.scale_x), height=int(70 * self.scale_y), primary_color="#FF9133", text_color="white", font=("sans", int(22 * self.scale_y), "bold"))
        boton_ver_facturas.pack(padx=4, pady=4)
        boton_ver_facturas.place(x=int(35 * self.scale_x), y=int(130 * self.scale_y))

        boton_generar_recibo = make_ctk_button(lblframe1, text="Generar Recibo", command=self.solicitar_contrasena_recibo, width=int(270 * self.scale_x), height=int(70 * self.scale_y), primary_color="#FF9133", text_color="white", font=("sans", int(22 * self.scale_y), "bold"))
        boton_generar_recibo.pack(padx=4, pady=4)
        boton_generar_recibo.place(x=int(35 * self.scale_x), y=int(330 * self.scale_y))

        boton_migrar_cierre = make_ctk_button(lblframe1, text="Mover a Cierre", command=self.solicitar_contrasena_migracion, width=int(270 * self.scale_x), height=int(70 * self.scale_y), primary_color="#FF9133", text_color="white", font=("sans", int(22 * self.scale_y), "bold"))
        boton_migrar_cierre.pack(padx=4, pady=4)
        boton_migrar_cierre.place(x=int(35 * self.scale_x), y=int(230 * self.scale_y))

        self.label_suma_total = tk.Label(frame2, text="Total:\n Bs0.00", bg="#C0C0C0", font="sans 25 bold")
        self.label_suma_total.place(x=int(1200 * self.scale_x), y=int(50 * self.scale_y))

        # Poner el foco en la barra de búsqueda al mostrar la ventana
        try:
            self.after(100, lambda: self.entry_nombre.focus_set())
        except Exception:
            try:
                self.entry_nombre.focus_set()
            except Exception:
                pass

    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT ide, nombre FROM inventario")
            productos = c.fetchall()
            # cache de productos (opcional) y comprobación (tupla de (ide, nombre))
            self.productos_cache = [(r[0], r[1]) for r in productos]
            if not productos:
                print("No se encontraron productos en la base de datos.")
            conn.close()
        except sqlite3.Error as e:
            print(f"Error al cargar productos desde la base de datos:", e)

    def actualizar_precio(self, event):
        nombre_producto = self.entry_nombre.get().strip()
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            # buscar por ide o por nombre
            c.execute("SELECT precio FROM inventario WHERE ide = ? OR nombre = ? LIMIT 1", (nombre_producto, nombre_producto))
            precio = c.fetchone()
            if (precio):
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, precio[0])
                self.entry_valor.config(state="readonly")
            else:
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, "Precio no disponible")
                self.entry_valor.config(state="readonly")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el precio del producto: {e}")
        finally:
            conn.close()

    def _on_nombre_key(self, event):
        """Buscar productos que contengan el texto y mostrar sugerencias en la listbox."""
        text = self.entry_nombre.get()
        if not text:
            try:
                self.suggestion_box.place_forget()
            except Exception:
                pass
            return
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT ide, nombre FROM inventario WHERE ide LIKE ? OR nombre LIKE ? LIMIT 8", ('%'+text+'%', '%'+text+'%'))
            rows = c.fetchall()
            conn.close()

            self.suggestion_box.delete(0, tk.END)
            # mantener lista de valores reales (ide) para cada entrada
            self.suggestion_values = []
            for r in rows:
                ide = r[0] if r[0] is not None else ''
                nombre = r[1] if len(r) > 1 and r[1] is not None else ''
                display = f"{ide} - {nombre}" if ide else nombre
                self.suggestion_box.insert(tk.END, display)
                self.suggestion_values.append(ide)

            if rows:
                # colocar la lista justo debajo del entry
                self.suggestion_box.place(x=int(100 * self.scale_x), y=int(50 * self.scale_y), width=int(180 * self.scale_x), height=min(100, 20*len(rows)))
            else:
                self.suggestion_box.place_forget()
        except Exception:
            try:
                self.suggestion_box.place_forget()
            except Exception:
                pass

    def _on_suggestion_select(self, event):
        sel = self.suggestion_box.curselection()
        if not sel:
            return
        idx = sel[0]
        # obtener ide real si está disponible
        ide = None
        try:
            ide = self.suggestion_values[idx]
        except Exception:
            ide = None
        value = self.suggestion_box.get(idx)
        # si hay ide, ponerlo en el entry para búsquedas por ide; si no, poner el texto completo
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, ide if ide else value)
        try:
            self.suggestion_box.place_forget()
        except Exception:
            pass
        # actualizar precio para el producto seleccionado
        self.actualizar_precio(None)
        # actualizar precio para el producto seleccionado
        self.actualizar_precio(None)

    def _on_nombre_enter(self, event):
        """Al pulsar Enter en la barra de búsqueda: selecciona el producto mostrado y lo agrega con cantidad 1."""
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            return 'break'
        # ocultar sugerencias si están visibles
        try:
            self.suggestion_box.place_forget()
        except Exception:
            pass

        # Actualizar precio (rellena entry_valor)
        try:
            self.actualizar_precio(None)
        except Exception:
            pass

        # Poner cantidad 1 y registrar el item
        try:
            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, '1')
        except Exception:
            pass

        # Reutilizar la lógica de registrar() (hará la verificación de stock)
        try:
            self.registrar()
        except Exception as e:
            # registrar ya muestra mensajes de error; en caso de excepción, mostrarla
            messagebox.showerror('Error', f'No se pudo agregar el producto: {e}')
        return 'break'

    def actualizar_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])
            total += subtotal
        self.label_suma_total.config(text=f"Total:\n Bs {total:.2f}")
        
    def registrar(self):
        producto = self.entry_nombre.get()
        precio = self.entry_valor.get()
        cantidad = self.entry_cantidad.get()

        if producto and precio and cantidad:
            try:
                cantidad = int(cantidad)
                if not self.verificar_stock(producto, cantidad):
                    messagebox.showerror("Error", "No hay suficiente stock para este producto.")
                    return
                precio = float(precio)
                subtotal = cantidad * precio

                # Mostrar los valores multiplicados por usd_rate en la vista
                precio_mostrado = precio * usd_rate
                subtotal_mostrado = subtotal * usd_rate

                # Resolver nombre real si el usuario ingresó un ide
                nombre_mostrar = producto
                try:
                    conn = sqlite3.connect(self.db_name)
                    c = conn.cursor()
                    c.execute("SELECT nombre FROM inventario WHERE ide = ? OR nombre = ? LIMIT 1", (producto, producto))
                    row = c.fetchone()
                    conn.close()
                    if row and row[0]:
                        nombre_mostrar = row[0]
                except Exception:
                    # en caso de error, usar el valor tal cual
                    nombre_mostrar = producto

                item_id = self.tree.insert("", "end", values=(nombre_mostrar, f"{precio_mostrado:.2f}", cantidad, f"{subtotal_mostrado:.2f}"))
                # Guardar los valores originales (en USD) para usarlos al guardar en la BD
                self.original_values[item_id] = (precio, subtotal)
                try:
                    self.entry_nombre.delete(0, tk.END)
                except Exception:
                    pass
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.config(state="readonly")
                self.entry_cantidad.delete(0, tk.END)

                self.actualizar_total()
                # Notificar al contenedor principal para actualizar total del día inmediatamente
                try:
                    container = self.master.master
                    if hasattr(container, 'update_total_dia'):
                        container.update_total_dia()
                except Exception:
                    pass
            except ValueError:
                messagebox.showerror("Error", "Cantidad o Precio no validos.")
        else:
            messagebox.showerror("Error", "Debe completar todos los campos.")

    def verificar_stock(self, nombre_producto, cantidad):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()                                    #problema con esta variable
            # buscar stock por ide o por nombre
            c.execute("SELECT stock FROM inventario WHERE ide = ? OR nombre = ?", (nombre_producto, nombre_producto))
            stock = c.fetchone()
            if stock and stock[0] >= cantidad:
                return True
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al verificar el stock: {e}")
            return False
        finally:
            conn.close()

    def obtener_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])
            total += subtotal
        return total
        


    def pagar_y_facturar(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            # Empezar transacción explícita
            for child in self.tree.get_children():
                item = self.tree.item(child, "values")
                nombre_producto = item[0]
                cantidad_vendida = int(item[2]) if item[2] else 0

                # Verificar stock antes de insertar
                if not self.verificar_stock(nombre_producto, cantidad_vendida):
                    conn.rollback()
                    messagebox.showerror("Error", f"No hay suficiente stock para {nombre_producto}.")
                    return

                # Recuperar los valores originales en USD si están disponibles, si no reconvertir usando usd_rate
                if child in self.original_values:
                    precio_usd, subtotal_usd = self.original_values[child]
                else:
                    try:
                        precio_usd = float(item[1]) / usd_rate if usd_rate else float(item[1])
                        subtotal_usd = float(item[3]) / usd_rate if usd_rate else float(item[3])
                    except Exception:
                        precio_usd = float(item[1]) if item[1] else 0.0
                        subtotal_usd = float(item[3]) if item[3] else 0.0

                # resolver nombre real si el usuario buscó por ide
                try:
                    c.execute("SELECT nombre FROM inventario WHERE ide = ? OR nombre = ? LIMIT 1", (nombre_producto, nombre_producto))
                    nombre_real_row = c.fetchone()
                    nombre_real = nombre_real_row[0] if nombre_real_row and nombre_real_row[0] else nombre_producto
                except Exception:
                    nombre_real = nombre_producto

                c.execute(
                    "INSERT INTO ventas (factura, nombre_articulo, valor_articulo, cantidad, subtotal, fecha) VALUES (?, ?, ?, ?, ?, ?)",
                    (self.numero_factura_actual, nombre_real, float(precio_usd), cantidad_vendida, float(subtotal_usd), datetime.now().strftime('%Y-%m-%d'))
                )

                # Restar stock en inventario (por ide o por nombre)
                c.execute("UPDATE inventario SET stock = stock - ? WHERE ide = ? OR nombre = ?", (cantidad_vendida, nombre_producto, nombre_producto))

            conn.commit()

            # Actualizar número de factura, limpiar vista y valores originales
            self.numero_factura_actual += 1
            for child in self.tree.get_children():
                self.tree.delete(child)
            self.label_suma_total.config(text="Total: Bs 0.00")
            self.original_values.clear()

            # Actualizar total del día en contenedor (los items de la venta fueron removidos)
            try:
                container = self.master.master
                if hasattr(container, 'update_total_dia'):
                    container.update_total_dia()
            except Exception:
                pass

            messagebox.showinfo("Éxito", "Compra agregada a las facturas.")
            try:
                # Traer la ventana principal al frente y darle foco
                self.master.lift()
                self.master.focus_force()
            except Exception:
                try:
                    self.focus_force()
                except Exception:
                    pass
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar la venta: {e}")
        finally:
            try:
                conn.close()
            except Exception:
                pass
















    def pagar(self, ventana_pago, entry_cantidad_pagada, label_cambio):
        try:
            cantidad_pagada = float(entry_cantidad_pagada.get())
            total = self.obtener_total()
            cambio = cantidad_pagada - total
            if cambio < 0:
                messagebox.showerror("Error", "La cantidad pagada es insuficiente.")
                return
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            try:
                for child in self.tree.get_children():
                    item = self.tree.item(child, "values")
                    nombre_producto = item[0]
                    cantidad_vendida = int(item[2])
                    if not self.verificar_stock(nombre_producto, cantidad_vendida):
                        messagebox.showerror("Error", f"No hay suficiente stock para {nombre_producto}.")
                        return
                    # Recuperar los valores originales en USD si están disponibles
                    if child in self.original_values:
                        precio_usd, subtotal_usd = self.original_values[child]
                    else:
                        # Si no están disponibles, intentar reconvertir dividiendo por usd_rate
                        try:
                            precio_usd = float(item[1]) / usd_rate if usd_rate != 0 else float(item[1])
                            subtotal_usd = float(item[3]) / usd_rate if usd_rate != 0 else float(item[3])
                        except Exception:
                            precio_usd = float(item[1])
                            subtotal_usd = float(item[3])

                    # obtener nombre real si el usuario buscó por ide
                    try:
                        c.execute("SELECT nombre FROM inventario WHERE ide = ? OR nombre = ? LIMIT 1", (nombre_producto, nombre_producto))
                        nombre_real = c.fetchone()
                        if nombre_real:
                            nombre_real = nombre_real[0]
                        else:
                            nombre_real = nombre_producto
                    except Exception:
                        nombre_real = nombre_producto

                    c.execute("INSERT INTO ventas (factura, nombre_articulo, valor_articulo, cantidad, subtotal, fecha) VALUES (?, ?, ?, ?, ?, ?)",
                                  (self.numero_factura_actual, nombre_real, float(precio_usd), cantidad_vendida, float(subtotal_usd), datetime.now().strftime('%Y-%m-%d')))

                    c.execute("UPDATE inventario SET stock = stock - ? WHERE ide = ? OR nombre = ?", (cantidad_vendida, nombre_producto, nombre_producto))

                conn.commit()
                messagebox.showinfo("Éxito", f"Pago realizado con éxito.")

                self.numero_factura_actual +=1
                self.mostrar_numero_factura()


                for child in self.tree.get_children():
                    self.tree.delete(child)
                self.label_suma_total.config(text="Total: $0.00")

                ventana_pago.destroy()

                # Notificar al contenedor para actualizar total del día
                try:
                    container = self.master.master
                    if hasattr(container, 'update_total_dia'):
                        container.update_total_dia()
                except Exception:
                    pass

            except sqlite3.Error as e:
                conn.rollback()
                messagebox.showerror("Error", f"Error al registrar la venta: {e}")
            finally:
                conn.close()
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida para el pago.")

    def obtener_numero_factura_actual(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT MAX(factura) FROM ventas")
            max_factura = c.fetchone()[0]
            if max_factura:
                return max_factura + 1
            else:
                return 1
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el número de factura: {e}")
            return 1
        finally:
            conn.close()

    def mostrar_numero_factura(self):
        self.numero_factura_actual.set(self.numero_factura_actual())

    def abrir_ventana_factura(self):
        ventana_factura = tk.Toplevel(self)
        ventana_factura.title("Facturas")
        ventana_factura.geometry("800x600")
        ventana_factura.configure(bg="#C6D9E3")
        ventana_factura.resizable(False, False)
        try:
            ventana_factura.transient(self.master)
            ventana_factura.focus_force()
            ventana_factura.attributes('-topmost', True)
        except Exception:
            pass

        facturas = tk.Label(ventana_factura, text="Lista de Facturas", bg="#C6D9E3", font="sans 20 bold")
        facturas.place(x=300, y=15)

        tree_frame = tk.Frame(ventana_factura, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        tree_frame.place(x=10, y=100, width=780, height=380)

        scrol_y = ttk.Scrollbar(tree_frame, orient="vertical")
        scrol_y.pack(side="right", fill="y")

        scrol_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        scrol_x.pack(side="bottom", fill="x")

        tree_facturas = ttk.Treeview(tree_frame, columns=("ID", "Factura", "Producto", "Precio", "Cantidad", "Subtotal"), show="headings", height=15, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=tree_facturas.yview)
        scrol_x.config(command=tree_facturas.xview)

        tree_facturas.heading("#1", text="ID")
        tree_facturas.heading("#2", text="Factura")
        tree_facturas.heading("#3", text="Producto")
        tree_facturas.heading("#4", text="Precio")
        tree_facturas.heading("#5", text="Cantidad")
        tree_facturas.heading("#6", text="Subtotal")

        tree_facturas.column("ID", width=70, anchor="center")
        tree_facturas.column("Factura", width=100, anchor="center")
        tree_facturas.column("Producto", width=200, anchor="center")
        tree_facturas.column("Precio", width=130, anchor="center")
        tree_facturas.column("Cantidad", width=130, anchor="center")
        tree_facturas.column("Subtotal", width=130, anchor="center")

        tree_facturas.pack(expand=True, fill="both")

        self.cargar_facturas(tree_facturas)

    def cargar_facturas(self, tree):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            facturas = c.fetchall()
            for factura in facturas:
                # Asumimos que la tupla es: (id, factura, nombre_articulo, valor_articulo, cantidad, subtotal)
                try:
                    precio_db = float(factura[3])
                    subtotal_db = float(factura[5])
                    # Mostrar multiplicado por usd_rate
                    precio_mostrado = precio_db * usd_rate
                    subtotal_mostrado = subtotal_db * usd_rate
                    tree.insert("", "end", values=(factura[0], factura[1], factura[2], f"{precio_mostrado:.2f}", factura[4], f"{subtotal_mostrado:.2f}"))
                except Exception:
                    # En caso de datos inesperados, insertar la fila cruda
                    tree.insert("", "end", values=factura)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar las facturas: {e}")
        
    def limpiar_treeview(self):
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.label_suma_total.config(text="Total: bs 0.00")

    def solicitar_contrasena_recibo(self):
        """Muestra una ventana emergente pidiendo la contraseña antes de generar el recibo."""
        ventana = tk.Toplevel(self)
        ventana.title('Autorización: Generar Recibo')
        ventana.geometry('360x140')
        ventana.resizable(False, False)
        try:
            ventana.transient(self.master)
            ventana.focus_force()
            ventana.attributes('-topmost', True)
        except Exception:
            pass

        lbl = tk.Label(ventana, text='Introduzca la contraseña para generar el recibo:', wraplength=340)
        lbl.pack(pady=(10, 5))

        pwd_var = tk.StringVar()
        entry_pwd = tk.Entry(ventana, textvariable=pwd_var, show='*', width=30)
        entry_pwd.pack(pady=(0, 10))

        def on_cancel():
            ventana.destroy()

        def on_ok():
            pwd = pwd_var.get()
            if self._validar_contrasena(pwd):
                try:
                    path = generate_and_save_receipt()
                    messagebox.showinfo('Éxito', f'Recibo generado y guardado en:\n{path}')
                    ventana.destroy()
                except Exception as e:
                    messagebox.showerror('Error', f'Error al generar el recibo: {e}')
            else:
                messagebox.showerror('Error', 'Contraseña incorrecta.')

        btn_frame = tk.Frame(ventana)
        btn_frame.pack(pady=(5, 10))
        tk.Button(btn_frame, text='Cancelar', command=on_cancel, width=12).pack(side='left', padx=8)
        tk.Button(btn_frame, text='Generar', command=on_ok, width=12).pack(side='left', padx=8)

    def _validar_contrasena(self, pwd):
        """Valida la contraseña contra el archivo `recibo/password` si existe, o contra 'recibo' por defecto."""
        try:
            base = os.path.join(os.path.dirname(__file__), 'recibo')
            pw_file = os.path.join(base, 'password')
            if os.path.exists(pw_file):
                with open(pw_file, 'r', encoding='utf-8') as f:
                    expected = f.read().strip()
            else:
                expected = 'recibo'
            return pwd == expected
        except Exception:
            return False

    def solicitar_contrasena_migracion(self):
        """Pide contraseña y, si es correcta, ejecuta la migración ventas -> cierre."""
        ventana = tk.Toplevel(self)
        ventana.title('Autorización: Migrar Ventas a Cierre')
        ventana.geometry('360x140')
        ventana.resizable(False, False)
        try:
            ventana.transient(self.master)
            ventana.focus_force()
            ventana.attributes('-topmost', True)
        except Exception:
            pass

        lbl = tk.Label(ventana, text='Introduzca la contraseña para migrar ventas a cierre:', wraplength=340)
        lbl.pack(pady=(10, 5))

        pwd_var = tk.StringVar()
        entry_pwd = tk.Entry(ventana, textvariable=pwd_var, show='*', width=30)
        entry_pwd.pack(pady=(0, 10))

        def on_cancel():
            ventana.destroy()

        def on_ok():
            pwd = pwd_var.get()
            if self._validar_contrasena(pwd):
                try:
                    resultado = migrar_ventas_a_cierre()
                    migrated = resultado.get('migrated') if isinstance(resultado, dict) else None
                    message = f'Migración completada. Registros insertados: {migrated}' if migrated is not None else 'Migración completada.'
                    messagebox.showinfo('Éxito', message)
                    ventana.destroy()
                    
                    # Al completar migración (cierre), resetear total del día mostrado
                    try:
                        container = self.master.master
                        if hasattr(container, 'reset_total_dia'):
                            container.reset_total_dia()
                        elif hasattr(container, 'update_total_dia'):
                            container.update_total_dia()
                    except Exception:
                        pass
                except Exception as e:
                    messagebox.showerror('Error', f'Error durante la migración: {e}')
            else:
                messagebox.showerror('Error', 'Contraseña incorrecta.')

        btn_frame = tk.Frame(ventana)
        btn_frame.pack(pady=(5, 10))
        tk.Button(btn_frame, text='Cancelar', command=on_cancel, width=12).pack(side='left', padx=8)
        tk.Button(btn_frame, text='Migrar', command=on_ok, width=12).pack(side='left', padx=8)
