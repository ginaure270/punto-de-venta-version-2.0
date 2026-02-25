import tkinter as tk
from PIL import Image, ImageTk
import os

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except Exception:
    ctk = None
    CTK_AVAILABLE = False


def make_ctk_button(parent, text="", command=None, width=240, height=60, image_path=None, font=("sans", 20, "bold"), corner_radius=40, primary_color=None, text_color=None, hover_color=None, **opts):
    """Return a CTkButton if available, else a normal tk.Button. Keeps image reference on widget.
    `font` is a tuple like (name, size[, style])."""
    if CTK_AVAILABLE:
        try:
            # prepare CTk-specific options (avoid passing unknown kwargs)
            ctk_opts = dict(opts)
            if primary_color:
                ctk_opts.setdefault('fg_color', primary_color)
            if text_color:
                ctk_opts.setdefault('text_color', text_color)
            if hover_color:
                ctk_opts.setdefault('hover_color', hover_color)

            if image_path and os.path.exists(image_path):
                img = Image.open(image_path).resize((40, 40))
                photo = ImageTk.PhotoImage(img)
                btn = ctk.CTkButton(parent, text=text, command=command, width=width, height=height, image=photo, font=font, corner_radius=corner_radius, **ctk_opts)
                btn._photo = photo
                _wrap_place_ignore_size(btn)
                return btn

            btn = ctk.CTkButton(parent, text=text, command=command, width=width, height=height, font=font, corner_radius=corner_radius, **ctk_opts)
            _wrap_place_ignore_size(btn)
            return btn
        except Exception:
            btn = ctk.CTkButton(parent, text=text, command=command, width=width, height=height, font=font, corner_radius=corner_radius)
            _wrap_place_ignore_size(btn)
            return btn

    # fallback
    # Fallback to native tk.Button. Map colors if provided.
    tk_opts = dict(opts)
    if primary_color:
        tk_opts.setdefault('bg', primary_color)
    if text_color:
        tk_opts.setdefault('fg', text_color)
    if hover_color:
        tk_opts.setdefault('activebackground', hover_color)

    if image_path and os.path.exists(image_path):
        try:
            img = Image.open(image_path).resize((40, 40))
            photo = ImageTk.PhotoImage(img)
            btn = tk.Button(parent, text=text, command=command, image=photo, compound="left", font=font, **tk_opts)
            btn._photo = photo
            return btn
        except Exception:
            pass
    return tk.Button(parent, text=text, command=command, font=font, **tk_opts)


def _wrap_place_ignore_size(widget):
    """Wrap the widget.place method to ignore width/height kwargs (needed for CTkWidget compatibility).
    This makes calling widget.place(x=..., y=..., width=..., height=...) safe even if the
    underlying widget disallows width/height in place()."""
    try:
        orig_place = widget.place
        def place_override(*args, **kwargs):
            kwargs = {k: v for k, v in kwargs.items() if k not in ("width", "height")}
            return orig_place(*args, **kwargs)
        widget.place = place_override
    except Exception:
        pass


if __name__ == '__main__':
    root = tk.Tk()
    b = make_ctk_button(root, text='Comprar', image_path='imagenes/ventas.png', command=lambda: print('ok'))
    b.pack(padx=16, pady=16)
    root.mainloop()
