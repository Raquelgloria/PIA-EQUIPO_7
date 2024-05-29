import tkinter as tk

class HomeWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Home Screen")

        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Configurar tamaño de la ventana
        window_width = min(900, screen_width)  # Máximo ancho de 900
        window_height = min(1100, screen_height)  # Máximo alto de 1100

        # Calcular dimensiones del margen
        margin_height = (screen_height - window_height) // 2

        # Crear widgets para el margen superior
        margin_top = tk.Frame(self, height=margin_height)
        margin_top.pack(fill=tk.BOTH, expand=True)

        # Crear label para el texto centrado
        label_home = tk.Label(self, text="Home Screen", font=("Arial", 24))
        label_home.pack()

        # Crear widgets para el margen inferior
        margin_bottom = tk.Frame(self, height=margin_height)
        margin_bottom.pack(fill=tk.BOTH, expand=True)

        # Configurar propiedades de la ventana
        self.resizable(True, True)  # Permitir redimensionar la ventana tanto horizontal como verticalmente
        # self.attributes("-fullscreen", True)  # Hacer que la ventana esté siempre maximizada
        self.geometry(f"{window_width}x{window_height}+{screen_width//2 - window_width//2}+{margin_height}")

if __name__ == "__main__":
    home_window = HomeWindow()
    home_window.mainloop()
