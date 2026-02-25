import customtkinter as ctk

app = ctk.CTk()
app.geometry("300x150")

label = ctk.CTkLabel(app, text="¡Hola desde CustomTkinter!", corner_radius=10, fg_color="lightblue")
label.pack(padx=20, pady=20)

app.mainloop()