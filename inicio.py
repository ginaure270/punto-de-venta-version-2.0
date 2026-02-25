import globales
import tkinter as tk
from tkinter import messagebox
from manager import Manager
from PIL import Image, ImageTk
from ctk_button import make_ctk_button
import customtkinter as ctk
ctk.set_appearance_mode("Dark")

      
USUARIOS = {
    "admin": "papo",
    "Alejandro": "cafe123",
    "Danito": "Danito"     
}

class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Punto de Venta 1.7")

        # Scale window size dynamically based on screen resolution
        scale_x = self.winfo_screenwidth() / 1920
        scale_y = self.winfo_screenheight() / 1080
        window_width = int(1000 * scale_x)
        window_height = int(600 * scale_y)
        self.geometry(f"{window_width}x{window_height}+{int(500 * scale_x)}+{int(200 * scale_y)}")

        self.resizable(False, False)
        self.configure(bg="#DBDADA")
        # Confirmación al intentar cerrar la aplicación
        try:
            self.protocol("WM_DELETE_WINDOW", self.on_close)
        except Exception:
            pass
        self.widgets()


        






    def widgets(self):
        # Adjust layout using relative placement based on 1920x1080 resolution
        scale_x = self.winfo_screenwidth() / 1920
        scale_y = self.winfo_screenheight() / 1080
        font_scale = min(scale_x, scale_y)

        nombre_usuario = tk.Label(self, text="Nombre de usuario:", fg="#252829", bg="#DBDADA", font=("sans", int(16 * font_scale), "bold"))
        nombre_usuario.place(x=650 * scale_x, y=200 * scale_y)

        contraseñausuario = tk.Label(self, text="Contraseña:", fg="#252829", bg="#DBDADA", font=("sans", int(16 * font_scale), "bold"))
        contraseñausuario.place(x=650 * scale_x, y=270 * scale_y)

        inicio_sesion = tk.Label(self, text="Inicio de sesión", fg="#252829", bg="#DBDADA", font=("sans", int(25 * font_scale), "bold"))
        inicio_sesion.place(x=620 * scale_x, y=50 * scale_y)

        version = tk.Label(self, text="Versión 1.7", bg="#DBDADA", font=("sans", int(10 * font_scale)))
        version.place(x=900 * scale_x, y=570 * scale_y)

        self.usuario = tk.Entry(self, width=20, font=("sans", int(12 * font_scale)))
        self.usuario.place(x=660 * scale_x, y=240 * scale_y)

        self.contrasena = tk.Entry(self, width=20, font=("sans", int(12 * font_scale)), show="*")
        self.contrasena.place(x=660 * scale_x, y=310 * scale_y)

        btn_verificar = make_ctk_button(self, text="Iniciar sesión", command=self.verificar, width=int(200 * scale_x), height=int(50 * scale_y))
        btn_verificar.place(x=655 * scale_x, y=380 * scale_y, width=200 * scale_x, height=50 * scale_y)

        btn_cerrar = make_ctk_button(self, text="Cerrar", command=self.on_close, width=int(200 * scale_x), height=int(50 * scale_y))
        btn_cerrar.place(x=655 * scale_x, y=450 * scale_y, width=200 * scale_x, height=50 * scale_y)

        framemitad = tk.Frame(self, bg="#1F2D2E", highlightbackground="white", highlightthickness=4)
        framemitad.place(x=0 * scale_x, y=0 * scale_y, width=500 * scale_x, height=600 * scale_y)

        derechosreservados = tk.Label(self, text="© 2025 Todos los derechos reservados", fg="#252829", bg="#E9E7E7", font=("sans", int(15 * font_scale), "bold"))
        derechosreservados.place(x=65 * scale_x, y=570 * scale_y)

        self.logo_image = Image.open("imagenes/codewave.png")
        self.logo_image = self.logo_image.resize((int(300 * scale_x), int(300 * scale_y)))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self, image=self.logo_image, bg="#1F2D2E")
        self.logo_label.place(x=100 * scale_x, y=20 * scale_y)

        sistema = tk.Label(self, text="Sistema de punto de venta", fg="#FFFFFF", bg="#1F2D2E", font=("sans", int(20 * font_scale), "bold"))
        sistema.place(x=65 * scale_x, y=300 * scale_y)

        bolivar = tk.Label(self, text="Bolívar. . Venezuela", fg="#FFFFFF", bg="#1F2D2E", font=("sans", int(10 * font_scale), "bold"))
        bolivar.place(x=180 * scale_x, y=340 * scale_y)

        copyright = tk.Label(self, text="© 2025 CodeWave 2025", fg="#FFFFFF", bg="#1F2D2E", font=("sans", int(12 * font_scale), "bold"))
        copyright.place(x=150 * scale_x, y=500 * scale_y)

        self.logo_image1 = Image.open("imagenes/usuario.png")
        self.logo_image1 = self.logo_image1.resize((int(90 * scale_x), int(90 * scale_y)))
        self.logo_image1 = ImageTk.PhotoImage(self.logo_image1)
        self.logo_label1 = tk.Label(self, image=self.logo_image1, bg="#DBDADA")
        self.logo_label1.place(x=700 * scale_x, y=90 * scale_y)










    def verificar(self):
        user = self.usuario.get()
        pwd = self.contrasena.get()
        if user in USUARIOS and USUARIOS[user] == pwd:
            if user == "admin" or user == "Danito":
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

    def on_close(self):
        try:
            respuesta = messagebox.askyesno("Salir", "¿Estás seguro de que quieres cerrar el programa?")
        except Exception:
            respuesta = False
        if respuesta:
            try:
                self.destroy()
            except Exception:
                pass

if __name__ == "__main__":
    login = Login()
    login.mainloop()