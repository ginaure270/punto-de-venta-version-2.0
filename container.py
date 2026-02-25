from logging import root
import tkinter as tk
import customtkinter as ctk
from ventas import Ventas
from inventario import Inventario
from inventario_admin import Inventario_Admin
import globales as g
from PIL import Image, ImageTk
import webbrowser
import os
from globales import usd_rate, last_update
from ctk_button import make_ctk_button
import sqlite3 as sql
import conexion as con
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from datetime import date, datetime, timedelta


def _ensure_ventas_has_fecha(db_path=None):
    """Asegura que la tabla `ventas` tenga la columna `fecha`. Si no existe,
    la añade y asigna la fecha de hoy a filas existentes."""
    if db_path is None:
        try:
            db_path = con.DB_PATH
        except Exception:
            db_path = 'database_ventas.db'
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cols = [r[1] for r in cur.execute("PRAGMA table_info(ventas)").fetchall()]
        if 'fecha' not in cols:
            try:
                cur.execute("ALTER TABLE ventas ADD COLUMN fecha TEXT")
            except Exception:
                pass
            today = datetime.now().strftime('%Y-%m-%d')
            try:
                cur.execute("UPDATE ventas SET fecha = ? WHERE fecha IS NULL OR fecha = ''", (today,))
            except Exception:
                pass
            conn.commit()
    except Exception:
        pass
    finally:
        try:
            conn.close()
        except Exception:
            pass

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        # lista de frames abiertos (Toplevel -> frame), usada para leer Treeviews activos
        self.open_frames = []
        self.pack()
        self.place(x=0, y=0, width=1990, height=1100)
        self.config(bg="#1F2D2E")
        self.widgets()
        controlador.state("zoomed")


    def show_frame(self, container):
        # Crear el Toplevel con el controlador (ventana raíz) como parent
        # así el stacking se maneja correctamente y `container` no queda encima.
        top_level = tk.Toplevel(self.controlador)
        frame = container(top_level)
        frame.config(bg="#C0C0C0")
        frame.pack(fill="both", expand=True)
        top_level.geometry("1920x1200+1+1")
        top_level.resizable(True , True)
        try:
            try:
                top_level.focus_force()
                top_level.lift()
            except Exception:
                pass
        except Exception:
            pass
        # Guardar referencia para poder sumar subtotales desde los Treeview abiertos
        try:
            self.open_frames.append(frame)
        except Exception:
            pass
        # Asegurar limpieza cuando se cierre el Toplevel
        try:
            def _on_close():
                try:
                    if frame in self.open_frames:
                        self.open_frames.remove(frame)
                except Exception:
                    pass
                try:
                    top_level.destroy()
                except Exception:
                    pass
            top_level.protocol("WM_DELETE_WINDOW", _on_close)
        except Exception:
            pass
    

    def ventas(self):
        self.show_frame(Ventas)

    def inventario(self):
        self.show_frame(Inventario)

    def abrir_pagina(self):
        webbrowser.open("https://github.com/SJLS27")
        webbrowser.open("https://github.com/ginaure270")


    def inventario_admin(self):
        if g.admin == False:
            tk.messagebox.showerror("Error", "No tienes permisos para acceder a esta sección.")
            return
        else:
            self.show_frame(Inventario_Admin)

    def user_button_action(self):
        # Acción simple al pulsar el botón de usuario
        try:
            tk.messagebox.showinfo("Usuario", "Abrir perfil de usuario")
        except Exception:
            print("Usuario pressed")

    def logout_action(self):
        # Confirmar cierre de sesión y volver a la pantalla de login
        try:
            respuesta = tk.messagebox.askyesno("Cerrar sesión", "¿Estás seguro de cerrar sesión?")
        except Exception:
            respuesta = False
        if not respuesta:
            return
        try:
            self.controlador.destroy()
        except Exception:
            pass
        try:
            from inicio import Login
            login = Login()
            login.mainloop()
        except Exception as e:
            print("No se pudo abrir Login:", e)

    def widgets(self):
        # Adjust layout using relative placement based on 1920x1080 resolution
        scale_x = self.winfo_screenwidth() / 1920
        scale_y = self.winfo_screenheight() / 1080
        font_scale = min(scale_x, scale_y)

        frame1 = tk.Frame(self, bg="#DBDADA")
        frame1.place(x=350 * scale_x, y=0, width=2000 * scale_x, height=1990 * scale_y)

        btn_ventas = make_ctk_button(self, text="Ir a ventas", command=self.ventas, image_path="imagenes/ventas.png", width=int(240 * scale_x), height=int(60 * scale_y), primary_color="#606663", text_color="white")
        btn_ventas.place(x=50 * scale_x, y=350 * scale_y, width=260 * scale_x, height=60 * scale_y)

        btninventario = make_ctk_button(self, text="Ir a inventario", command=self.inventario, width=int(240 * scale_x), height=int(60 * scale_y), primary_color="#606663", text_color="white")
        btninventario.place(x=50 * scale_x, y=450 * scale_y, width=260 * scale_x, height=60 * scale_y)

        btninventarioadmin = make_ctk_button(self, text="Admin", command=self.inventario_admin, width=int(240 * scale_x), height=int(60 * scale_y), primary_color="#1CC96D", text_color="white")
        btninventarioadmin.place(x=50 * scale_x, y=550 * scale_y, width=260 * scale_x, height=60 * scale_y)

        btn_cerrarsesion = make_ctk_button(self, text="Cerrar sesion", command=self.logout_action, width=int(240 * scale_x), height=int(60 * scale_y), primary_color="#606663", text_color="white")
        btn_cerrarsesion.place(x=50 * scale_x, y=650 * scale_y, width=260 * scale_x, height=60 * scale_y)

        self.logo_image = Image.open("imagenes/codewave.png")
        self.logo_image = self.logo_image.resize((int(300 * scale_x), int(300 * scale_y)))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self, image=self.logo_image, bg="#1F2D2E")
        self.logo_label.place(x=30 * scale_x, y=30 * scale_y)

        label_hola = tk.Label(self, text=f"¡Hola, Bienvenido!", bg="#E2E6E9", fg="#252829", font=("arial", int(18 * font_scale), "bold"))
        label_hola.place(x=430 * scale_x, y=70 * scale_y)

        label_usd = ctk.CTkLabel(self, text=f"Tasa de cambio USD:\n .", corner_radius=13, fg_color="#FFFFFF", bg_color="#DBDADA", text_color="#656C6C", width=int(300 * scale_x), height=int(120 * scale_y), font=("Arial", int(20 * font_scale), "bold"))
        label_usd.place(x=430 * scale_x, y=150 * scale_y)

        label_usdprecio = tk.Label(self, text=f"  {usd_rate} Bs.S", bg="#FFFFFF", fg="#000000", font=("sans", int(22 * font_scale), "bold"))
        label_usdprecio.place(x=440 * scale_x, y=220 * scale_y, width=270 * scale_x, height=30 * scale_y)

        self.logo_image2 = Image.open("imagenes/moneda2.png")
        self.logo_image2 = self.logo_image2.resize((int(35 * scale_x), int(35 * scale_y)))
        self.logo_image2 = ImageTk.PhotoImage(self.logo_image2)
        self.logo_label2 = tk.Label(self, image=self.logo_image2, bg="#FFFFFF")
        self.logo_label2.place(x=450 * scale_x, y=215 * scale_y)

        label_update = tk.Label(self, text=f"Última actualización: {last_update}", bg="#DBDADA", fg="#252829", font=("sans", int(12 * font_scale), "bold"))
        label_update.place(x=470 * scale_x, y=450 * scale_y)

        self.aprobado = Image.open("imagenes/aprobado.png")
        self.aprobado = self.aprobado.resize((int(20 * scale_x), int(20 * scale_y)))
        self.aprobado = ImageTk.PhotoImage(self.aprobado)
        self.labelaprobado = tk.Label(self, image=self.aprobado, bg="#DBDADA")
        self.labelaprobado.place(x=450 * scale_x, y=450 * scale_y)

        chart_frame = tk.Frame(self, bg="#FFFFFF", highlightbackground="gray", highlightthickness=4)
        chart_frame.place(x=550 * scale_x, y=500 * scale_y, width=1100 * scale_x, height=400 * scale_y)

        self.fig = Figure(figsize=(8, 3.5), dpi=100, facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#FFFFFF")
        self.ax.tick_params(colors="black", which="both")
        self.ax.title.set_color("black")
        self.ax.yaxis.label.set_color("black")
        self.ax.xaxis.label.set_color("black")

        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.canvas.get_tk_widget().configure(bg="#FFFFFF")

        def update_weekly_chart():
            today = date.today()
            days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
            esp = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
            labels = []
            for i in range(6, -1, -1):
                d = (today - timedelta(days=i)).strftime('%Y-%m-%d')
                try:
                    wd = datetime.strptime(d, '%Y-%m-%d').weekday()
                    labels.append(esp[wd])
                except Exception:
                    labels.append(d)
            counts = []
            db_path = None
            try:
                db_path = con.DB_PATH
            except Exception:
                db_path = 'database_ventas.db'
            try:
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                for d in days:
                    try:
                        cur.execute("SELECT SUM(cantidad) FROM ventas WHERE fecha = ?", (d,))
                        r = cur.fetchone()
                        counts.append(r[0] if r and r[0] is not None else 0)
                    except Exception:
                        counts.append(0)
                conn.close()
            except Exception:
                counts = [0]*7

            self.ax.clear()
            self.ax.bar(labels, counts, color="#1CC96D")
            self.ax.set_title('Producción últimos 7 días')
            self.ax.set_ylabel('Cantidad')
            self.ax.set_ylim(0, max(max(counts) * 1.2, 1))
            for i, v in enumerate(counts):
                self.ax.text(i, v + (max(max(counts) * 0.02, 0.1)), str(v), ha='center')
            self.canvas.draw()

        update_weekly_chart()
        try:
            self.after(60000, update_weekly_chart)
        except Exception:
            pass



