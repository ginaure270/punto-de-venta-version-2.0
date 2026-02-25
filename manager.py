from tkinter import Tk, Frame, messagebox
from container import  Container

class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Caja Registradora")
        self.resizable(True, True)
        self.configure(bg="#28404D")
        self.geometry("1920x1000+0+0")

        # Confirmación antes de cerrar la aplicación principal
        try:
            self.protocol("WM_DELETE_WINDOW", self.on_close)
        except Exception:
            pass

        self.container = Frame(self, bg="#2D353A")
        self.container.pack(fill="both", expand=True)

        self.frames = {
            Container: None 
        }

        self.load_frames()

        self.show_frame(Container)

    def load_frames(self):
        for FrameClass in self.frames.keys():
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

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

def main():
    app = Manager()
    app.mainloop()


if __name__ == "__main__":
    main()
