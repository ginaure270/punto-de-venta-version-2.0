from container import  Container
from tkinter import Tk, Frame, Entry, Button, messagebox
from index import index
from manager import Manager

admin_user = False

class Inicio_Sesion(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Inicio De Sesion")
        self.resizable(False, False)
        self.configure(bg="#395C63")
        self.geometry("300x200+120+20")

        self.container = Frame(self, bg="#C6D9E3")
        self.container.pack(fill="both", expand=True)
        
        self.Usuario = Entry(self, bg="#C6D9E3")
        self.Usuario.place(x=50, y=50, width=200, height=30)
        self.Usuario.insert(0, "Usuario")
        
        self.Contraseña = Entry(self, show="*", bg="#C6D9E3")
        self.Contraseña.place(x=50, y=100, width=200, height=30)
        self.Contraseña.insert(0, "Contraseña")
        
        self.Iniciar_sesion = Button(self, text="Iniciar Sesion", command=self.iniciar_sesion, bg="#C6D9E3")
        self.Iniciar_sesion.place(x=50, y=150, width=200, height=30)

    def iniciar_sesion(self):
        usuario = self.Usuario.get()
        contraseña = self.Contraseña.get()
        global admin_user
        if usuario == "ADMIN" and contraseña == "FREEFIRE":
            admin_user = True
            index.mainloop()
        elif usuario == "USER" and contraseña == "12345":
            admin_user = False
            index.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


