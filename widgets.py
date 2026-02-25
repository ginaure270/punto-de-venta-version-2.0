import tkinter as tk


class RoundedButton(tk.Canvas):
    def __init__(self, master, text='', width=200, height=48, radius=14,
                 bg="#ffffff", fg="#333333", font=("Segoe UI", 11, "bold"),
                 command=None, hover_bg=None, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, bg=master['bg'], **kwargs)
        self.width = width
        self.height = height
        self.radius = radius
        self.bg = bg
        self.fg = fg
        self.font = font
        self.command = command
        self.hover_bg = hover_bg or self._shade_color(bg, -12)
        self.pressed = False
        self._draw(bg)
        self.create_text(self.width//2, self.height//2, text=text, fill=self.fg, font=self.font, tags=("txt",))
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _draw(self, color):
        self.delete("bg")
        x1, y1, x2, y2 = 0, 0, self.width, self.height
        r = self.radius
        self.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, style='pieslice', fill=color, outline=color, tags=("bg",))
        self.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, style='pieslice', fill=color, outline=color, tags=("bg",))
        self.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style='pieslice', fill=color, outline=color, tags=("bg",))
        self.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style='pieslice', fill=color, outline=color, tags=("bg",))
        self.create_rectangle(x1+r, y1, x2-r, y2, fill=color, outline=color, tags=("bg",))
        self.create_rectangle(x1, y1+r, x2, y2-r, fill=color, outline=color, tags=("bg",))

    def _on_press(self, event=None):
        self.pressed = True
        self._draw(self._shade_color(self.bg, -18))

    def _on_release(self, event=None):
        if self.pressed and self.command:
            try:
                self.command()
            except Exception:
                pass
        self.pressed = False
        self._draw(self.bg)

    def _on_enter(self, event=None):
        if not self.pressed:
            self._draw(self.hover_bg)

    def _on_leave(self, event=None):
        if not self.pressed:
            self._draw(self.bg)

    @staticmethod
    def _shade_color(hex_color, percent):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        def clamp(v):
            return max(0, min(255, v))
        r = clamp(int(r + (percent/100.0)*255))
        g = clamp(int(g + (percent/100.0)*255))
        b = clamp(int(b + (percent/100.0)*255))
        return f"#{r:02x}{g:02x}{b:02x}"


def make_button(parent, text=None, image=None, command=None, width=None, height=None, **kwargs):
    """Factory: si hay imagen o se especifica que se necesita un tk.Button, devuelve tk.Button.
    En caso contrario devuelve un `RoundedButton` que soporta place/pack/grid.
    """
    if image is not None or kwargs.pop('force_tk', False):
        btn = tk.Button(parent, text=text, image=image, command=command, **kwargs)
        return btn
    width = width or 200
    height = height or 48
    rb = RoundedButton(parent, text=text or '', width=width, height=height, command=command, **kwargs)
    return rb
