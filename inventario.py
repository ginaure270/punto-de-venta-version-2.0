#contribution by SJLS27
import tkinter as tk
from tkinter import ttk
import conexion as con


class Inventario(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Inventario")
        self.master.configure(bg="lightblue")
        self.master.geometry("800x500")

        self.titulo = tk.Label(self.master, text="Inventario", bg="lightblue", font=("Arial", 16, "bold"))
        self.titulo.grid(row=1, column=2)

        self.tree = ttk.Treeview(self.master, columns=("ID", "Nombre", "Precio", "Cantidad"), show="headings", height=20)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.grid(row=2, column=2)

        self.textbox1 = tk.Entry(self.master, width=20)
        self.textbox1.grid(row=3, column=2)
        self.textbox1.bind("<KeyRelease>", self.buscar)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = Inventario(master=root)
    app.mainloop()
