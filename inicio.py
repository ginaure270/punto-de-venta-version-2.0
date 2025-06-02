import globales
import tkinter as tk
from tkinter import messagebox
from manager import Manager

USUARIOS = {
    "admin": "FREEFIRE",
    "user": "Skibidy"
}

class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inicio de sesión")
        self.geometry("350x200")
        self.resizable(False, False)
        self.configure(bg="#C6D9E3")
        self.widgets()

    def widgets(self):
        tk.Label(self, text="Usuario:", bg="#C6D9E3", font=("Arial", 12)).place(x=40, y=40)
        tk.Label(self, text="Contraseña:", bg="#C6D9E3", font=("Arial", 12)).place(x=40, y=80)

        self.usuario = tk.Entry(self, width=20)
        self.usuario.place(x=150, y=40)
        self.contrasena = tk.Entry(self, width=20, show="*")
        self.contrasena.place(x=150, y=80)

        btn = tk.Button(self, text="Iniciar sesión", command=self.verificar)
        btn.place(x=120, y=130, width=120, height=30)

    def verificar(self):
        user = self.usuario.get()
        pwd = self.contrasena.get()
        if user in USUARIOS and USUARIOS[user] == pwd:
            if user == "admin":
                globales.admin = True
                messagebox.showinfo("Bienvenido", "Has iniciado sesión como administrador")
            else:
                globales.admin = False
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.destroy()
            app = Manager()
            app.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

if __name__ == "__main__":
    login = Login()
    login.mainloop()