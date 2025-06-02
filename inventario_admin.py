import tkinter as tk
from tkinter import ttk, messagebox
import conexion as con


class Inventario_Admin(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#061B27")
        self.pack(fill="both", expand=True)

        def buscar(event=None):
            nombre = self.textbox1.get()
            resultados = con.buscar_producto(nombre)
            self.tree.delete(*self.tree.get_children())
            for fila in resultados:
                self.tree.insert("", tk.END, values=fila)

        def mostrar_todos():
            base = con.buscar_producto("")
            self.tree.delete(*self.tree.get_children())
            for fila in base:
                self.tree.insert("", tk.END, values=fila)



                    #AGARRAME LA PORONGA
                     #AGARRAME LA PORONGA
                      #AGARRAME LA PORONGA
                       #AGARRAME LA PORONGA
                        #AGARRAME LA PORONGA
                         #AGARRAME LA PORONGA
                          #AGARRAME LA PORONGA
                           #AGARRAME LA PORONGA
                            #AGARRAME LA PORONGA
                             #AGARRAME LA PORONGA
                              #AGARRAME LA PORONGA
                               #AGARRAME LA PORONGA
                                #AGARRAME LA PORONGA
                                 #AGARRAME LA PORONGA
                                  #AGARRAME LA PORONGA
                                   #AGARRAME LA PORONGA
                                    #AGARRAME LA PORONGA
                                     #AGARRAME LA PORONGA
                                      #AGARRAME LA PORONGA
                                       #AGARRAME LA PORONGA
                                        #AGARRAME LA PORONGA
                                         #AGARRAME LA PORONGA
                                          #AGARRAME LA PORONGA
                                           #AGARRAME LA PORONGA
                                            #AGARRAME LA PORONGA
                                             #AGARRAME LA PORONGA
                                              #AGARRAME LA PORONGA
                                               #AGARRAME LA PORONGA
                                                #AGARRAME LA PORONGA
                                                 #AGARRAME LA PORONGA
                                                  #AGARRAME LA PORONGA 
                                                   #AGARRAME LA PORONGA
                                                    #AGARRAME LA PORONGA
                                                    #AGARRAME LA PORONGA
                                                     #AGARRAME LA PORONGA
                                                      #AGARRAME LA PORONGA
                                                       #AGARRAME LA PORONGA
                                                        #AGARRAME LA PORONGA
                                                         #AGARRAME LA PORONGA
                                                          #AGARRAME LA PORONGA
                                                           #AGARRAME LA PORONGA
                                                            #AGARRAME LA PORONGA
                                                             #AGARRAME LA PORONGA
                                                              #AGARRAME LA PORONGA #AGARRAME LA PORONGA
                                                               #AGARRAME LA PORONGA


        def anadir_producto():
            nombre = self.entry_nombre.get()
            precio = self.entry_precio.get()
            cantidad = self.entry_cantidad.get()
            if nombre and precio and cantidad:
                try:
                    con.anadir_producto(nombre, int(cantidad), float(precio))
                    mostrar_todos()
                    self.entry_nombre.delete(0, tk.END)
                    self.entry_precio.delete(0, tk.END)
                    self.entry_cantidad.delete(0, tk.END)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Campos vacíos", "Completa todos los campos.")

        def borrar_producto():
            seleccionado = self.tree.selection()
            if seleccionado:
                item = self.tree.item(seleccionado)
                id_producto = item['values'][0]
                con.borrar_producto(id_producto)
                mostrar_todos()
            else:
                messagebox.showwarning("Selecciona", "Selecciona un producto para borrar.")

        def modificar_producto():
            seleccionado = self.tree.selection()
            if seleccionado:
                item = self.tree.item(seleccionado)
                id_producto = item['values'][0]
                nombre = self.entry_nombre.get()
                precio = self.entry_precio.get()
                cantidad = self.entry_cantidad.get()
                if nombre and precio and cantidad:
                    con.modificar_producto(id_producto, nombre, int(cantidad), float(precio))
                    mostrar_todos()
                else:
                    messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            else:
                messagebox.showwarning("Selecciona", "Selecciona un producto para modificar.")

        def cargar_producto(event):
            seleccionado = self.tree.selection()
            if seleccionado:
                item = self.tree.item(seleccionado)
                self.entry_nombre.delete(0, tk.END)
                self.entry_precio.delete(0, tk.END)
                self.entry_cantidad.delete(0, tk.END)
                self.entry_nombre.insert(0, item['values'][1])   # Nombre
                self.entry_precio.insert(0, item['values'][2])   # Precio
                self.entry_cantidad.insert(0, item['values'][3]) # Cantidad

        # Título
        titulo = tk.Label(self, text="Inventario", bg="lightblue", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=1, columnspan=3)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("ID","Nombre", "Precio", "Cantidad"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.grid(row=1, column=1, columnspan=3, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", cargar_producto)

        # Entry para buscar
        tk.Label(self, text="Buscar:", bg="#99BCCE").grid(row=2, column=1, sticky="e")
        self.textbox1 = tk.Entry(self, width=20)
        self.textbox1.grid(row=2, column=2, sticky="w")
        self.textbox1.bind("<KeyRelease>", buscar)

        # Entradas para add y mod
        tk.Label(self, text="Nombre:", bg="#99BCCE").grid(row=3, column=1, sticky="e")
        self.entry_nombre = tk.Entry(self, width=20)
        self.entry_nombre.grid(row=3, column=2, sticky="w")

        tk.Label(self, text="Precio:", bg="#99BCCE").grid(row=4, column=1, sticky="e")
        self.entry_precio = tk.Entry(self, width=20)
        self.entry_precio.grid(row=4, column=2, sticky="w")

        tk.Label(self, text="Cantidad:", bg="#99BCCE").grid(row=5, column=1, sticky="e")
        self.entry_cantidad = tk.Entry(self, width=20)
        self.entry_cantidad.grid(row=5, column=2, sticky="w")

        # Botones
        btn_anadir = tk.Button(self, text="Añadir", command=anadir_producto)
        btn_anadir.grid(row=6, column=1, pady=10)

        btn_modificar = tk.Button(self, text="Modificar", command=modificar_producto)
        btn_modificar.grid(row=6, column=2, pady=10)

        btn_borrar = tk.Button(self, text="Borrar", command=borrar_producto)
        btn_borrar.grid(row=6, column=3, pady=10)

        mostrar_todos()