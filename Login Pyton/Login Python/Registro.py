import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector


class RegisterWindow(tk.Tk):
    def __init__(self, login_window):
        super().__init__()

        self.title("Registro")

        self.state("zoomed") 
        

        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular dimensiones del margen
        margin_height = (screen_height - 400) // 2

        # Crear widgets para el margen superior
        margin_top = tk.Frame(self, height=margin_height)
        margin_top.pack(fill=tk.BOTH, expand=True)

        # Crear los widgets
        self.label_nombre = tk.Label(self, text="Nombre:", font=("Arial", 14))
        self.label_correo = tk.Label(self, text="Número de empleado:", font=("Arial", 14))
        
        self.entry_nombre = tk.Entry(self, font=("Arial", 12))
        self.entry_idemployee = tk.Entry(self, font=("Arial", 12))
        
        self.button_registrar = tk.Button(self, text="Registrar", command=self.registrar_usuario, font=("Arial", 12))
        self.button_cancelar = tk.Button(self, text="Cancelar", command=self.cancelar_registro, font=("Arial", 12))

        # Colocar los widgets en la ventana
        self.label_nombre.pack(pady=5)
        self.entry_nombre.pack(pady=5)
        self.label_correo.pack(pady=5)
        self.entry_idemployee.pack(pady=5)
 
        self.button_registrar.pack(pady=5)
        self.button_cancelar.pack(pady=5)

        # Crear widgets para el margen inferior
        margin_bottom = tk.Frame(self, height=margin_height)
        margin_bottom.pack(fill=tk.BOTH, expand=True)

        # Centrar la ventana
        self.geometry(f"500x400+{screen_width // 2 - 250}+{margin_height}")

        self.login_window = login_window

    def registrar_usuario(self):
        username = self.entry_nombre.get().strip()
        employeeID = self.entry_idemployee.get().strip()
        

        try:
            # Conectarse a la base de datos
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="agencia_pia"
            )

            # Crear un cursor para ejecutar consultas SQL
            cursor = conexion.cursor()

            

            print(username, employeeID)

            # Ejecutar una consulta SQL para insertar un nuevo usuario
            if all(data is not None and data != '' for data in [username, employeeID]):
                consulta = "INSERT INTO empleados (Nombre, EmpleadoID) VALUES (%s, %s)"
                valores = (username, employeeID)
                cursor.execute(consulta, valores)

                conexion.commit()
                messagebox.showinfo("Registro", "Usuario registrado exitosamente")
                self.destroy()
                self.login_window.deiconify()
            else:
                messagebox.showerror("Error", f"No se ha podido registrar al usuario: {error}")


        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se ha podido registrar al usuario: {error}")

        except Exception as error:
            messagebox.showerror("Error", f"No se ha podido registrar al usuario : {error}")

        finally:
            if 'conexion' in locals():
                conexion.close()

    def cancelar_registro(self):
        self.destroy()
        self.login_window.deiconify()
