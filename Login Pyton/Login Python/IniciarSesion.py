import tkinter as tk
from tkinter import messagebox
import mysql.connector
from Registro import RegisterWindow
from Home import HomeWindow  # Asegúrate de importar la clase HomeWindow desde el archivo home.py

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Inicio de sesión")

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

        # Crear widgets
        self.label_usuario = tk.Label(self, text="Número de empleado:", font=("Arial", 14))
        
        self.entry_idemployee = tk.Entry(self, width=40, font=("Arial", 12))
        
        self.button_registrar = tk.Button(self, text="Registrar", command=self.abrir_ventana_registro, width=15, font=("Arial", 12))
        self.button_ingresar = tk.Button(self, text="Ingresar", command=self.validar_login, width=15, font=("Arial", 12))

        # Ubicar widgets en la ventana
        self.label_usuario.pack(pady=5)
        self.entry_idemployee.pack(pady=5)
   
        self.button_registrar.pack(pady=5)
        self.button_ingresar.pack(pady=5)

        # Crear widgets para el margen inferior
        margin_bottom = tk.Frame(self, height=margin_height)
        margin_bottom.pack(fill=tk.BOTH, expand=True)

        self.geometry(f"{window_width}x{window_height}+{screen_width//2 - window_width//2}+{margin_height}")

    def validar_login(self):
        employee_id = self.entry_idemployee.get()
        

        try:
            # Conectar a la base de datos
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="agencia_pia"
            )

            # Crear un cursor para ejecutar consultas SQL
            cursor = conexion.cursor()

            # Ejecutar consulta para buscar el usuario en la base de datos
            consulta = "SELECT * FROM empleados WHERE EmpleadoID = %s "
            cursor.execute(consulta, (employee_id,))
            resultado = cursor.fetchall()

            if resultado:  # Si se encontró el usuario y la contraseña coinciden
                messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso")
                self.destroy()  # Cerrar la ventana de inicio de sesión
                # Abrir la ventana HomeWindow
                home_window = HomeWindow()
                home_window.mainloop()
            else:
                messagebox.showerror("Error", "Usuario incorrecto")

        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error en la base de datos: {error}")

        finally:
            # Cerrar la conexión a la base de datos
            if 'conexion' in locals():
                conexion.close() 

    def abrir_ventana_registro(self):
        # Ocultar la ventana de inicio de sesión
        self.withdraw()
        # Crear y mostrar la ventana de registro
        register_window = RegisterWindow(self)
        register_window.protocol("WM_DELETE_WINDOW", self.mostrar_ventana_principal)  # Mostrar ventana de inicio de sesión al cerrar la ventana de registro
        register_window.mainloop()

    def mostrar_ventana_principal(self):
        self.deiconify()
