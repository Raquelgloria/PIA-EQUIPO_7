import tkinter as tk
from tkinter import ttk  # Importa ttk para utilizar Treeview
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime


# Conectar a la base de datos MySQL
####BACKEND
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="agencia_pia"
    )

#FRONTEND
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

        # Crear un frame para la imagen
        image_frame = tk.Frame(self)
        image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Cargar la imagen
        image = Image.open("C:/Users/raque/OneDrive/Imágenes/AUTORUN.png")
        resized_image = image.resize((window_width, window_height // 2))

        photo = ImageTk.PhotoImage(resized_image)

        # Crear el widget Label para mostrar la imagen
        image_label = tk.Label(image_frame, image=photo)
        image_label.image = photo
        image_label.pack(fill=tk.BOTH, expand=True)

        # Crear un frame para los botones
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Crear label para el texto centrado
        label_home = tk.Label(button_frame, text="¡¡BIENVENIDO!!", font=("Arial", 24))
        label_home.pack()

        # Crear lista de acciones
        actions = ["Ingresar Venta", "Modificar Venta", "Eliminar Venta", "Reporte de Venta"]

        for action in actions:
            button = tk.Button(button_frame, text=action, command=lambda a=action: self.open_action_window(a))
            button.pack(pady=10)

        # Configurar propiedades de la ventana
        self.resizable(True, True)  # Permitir redimensionar la ventana tanto horizontal como verticalmente
        self.geometry(f"{window_width}x{window_height}+{screen_width//2 - window_width//2}+{margin_height}")

    def open_action_window(self, action):
        action_window = ActionWindow(self, action)
        action_window.grab_set()  # Bloquear la interacción con la ventana principal

class ActionWindow(tk.Toplevel):
####BACKEND
    def __init__(self, master, action):
        super().__init__(master)
        self.title(action)
        self.action = action

        label = tk.Label(self, text=f"Realizando acción: {action}", font=("Arial", 18))
        label.pack(pady=20)

        if action == "Ingresar Venta":
            self.create_ingresar_venta_form()
        elif action == "Modificar Venta":
            self.create_modificar_venta_form()
        elif action == "Eliminar Venta":
            self.create_eliminar_venta_form()
        elif action == "Reporte de Venta":
            self.generate_report()

    def create_ingresar_venta_form(self):
        self.client_id_entry = tk.Entry(self)
        self.client_id_entry.pack(pady=10)
        self.client_id_entry.insert(0, "ClienteID")

        self.employee_id_entry = tk.Entry(self)
        self.employee_id_entry.pack(pady=10)
        self.employee_id_entry.insert(0, "EmpleadoID")

        self.date_entry = tk.Entry(self)
        self.date_entry.pack(pady=10)
        self.date_entry.insert(0, "FechaVenta (YYYY-MM-DD)")

        self.total_price_entry = tk.Entry(self)
        self.total_price_entry.pack(pady=10)
        self.total_price_entry.insert(0, "PrecioTotal")

        confirm_button = tk.Button(self, text="Confirmar", command=self.ingresar_venta)
        confirm_button.pack(pady=20)

    def create_modificar_venta_form(self):
        self.sale_id_entry = tk.Entry(self)
        self.sale_id_entry.pack(pady=10)
        self.sale_id_entry.insert(0, "VentaID")

        self.total_price_entry = tk.Entry(self)
        self.total_price_entry.pack(pady=10)
        self.total_price_entry.insert(0, "Nuevo PrecioTotal")

        confirm_button = tk.Button(self, text="Confirmar", command=self.modificar_venta)
        confirm_button.pack(pady=20)

    def create_eliminar_venta_form(self):
        self.sale_id_entry = tk.Entry(self)
        self.sale_id_entry.pack(pady=10)
        self.sale_id_entry.insert(0, "VentaID")

        confirm_button = tk.Button(self, text="Confirmar", command=self.eliminar_venta)
        confirm_button.pack(pady=20)

    def generate_report(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Ventas")
        rows = cursor.fetchall()

        # Crear un Treeview para mostrar la tabla
        tree = ttk.Treeview(self)
        tree["columns"] = ("Cliente ID", "Empleado ID", "Fecha Venta", "Precio Total")
        tree.heading("#0", text="Venta ID")
        tree.heading("Cliente ID", text="Cliente ID")
        tree.heading("Empleado ID", text="Empleado ID")
        tree.heading("Fecha Venta", text="Fecha Venta")
        tree.heading("Precio Total", text="Precio Total")

        # Insertar filas en el Treeview
        for row in rows:
            tree.insert("", tk.END, text=row[0], values=(row[1], row[2], row[3], row[4]))

        # Ajustar columnas al contenido
        for column in tree["columns"]:
            tree.column(column, stretch=tk.YES)
            tree.column(column, width=100)  # Ajusta el ancho de las columnas según sea necesario

        tree.pack(pady=10)

        cursor.close()
        conn.close()


    def ingresar_venta(self):
        conn = connect_db()
        cursor = conn.cursor()

        client_id = self.client_id_entry.get()
        employee_id = self.employee_id_entry.get()
        date = self.date_entry.get()
        total_price = self.total_price_entry.get()

        try:
            cursor.execute(
                "INSERT INTO Ventas (ClienteID, EmpleadoID, FechaVenta, PrecioTotal) VALUES (%s, %s, %s, %s)",
                (client_id, employee_id, date, total_price)
            )
            conn.commit()
            messagebox.showinfo("Confirmación", "Venta ingresada con éxito")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se ha podido ingresar la venta: {error}")
        except Exception as error:
            messagebox.showerror("Error", f"No se ha podido ingresar la venta: {error}")
        finally:
            cursor.close()
            conn.close()
            self.destroy()

    def modificar_venta(self):
        conn = connect_db()
        cursor = conn.cursor()

        sale_id = self.sale_id_entry.get()
        new_total_price = self.total_price_entry.get()

        try:
            cursor.execute(
                "UPDATE Ventas SET PrecioTotal = %s WHERE VentaID = %s",
                (new_total_price, sale_id)
            )
            conn.commit()
            messagebox.showinfo("Confirmación", "Venta modificada con éxito")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se ha podido modificar la venta: {error}")
        except Exception as error:
            messagebox.showerror("Error", f"No se ha podido modificar la venta: {error}")
        finally:
            cursor.close()
            conn.close()
            self.destroy()

    def eliminar_venta(self):
        conn = connect_db()
        cursor = conn.cursor()

        sale_id = self.sale_id_entry.get()

        try:
            cursor.execute("DELETE FROM Ventas WHERE VentaID = %s", (sale_id,))
            conn.commit()
            messagebox.showinfo("Confirmación", "Venta eliminada con éxito")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se ha podido eliminar la venta: {error}")
        except Exception as error:
            messagebox.showerror("Error", f"No se ha podido eliminar la venta: {error}")
        finally:
            cursor.close()
            conn.close()
            self.destroy()

if __name__ == "__main__":
    home_window = HomeWindow()
    home_window.mainloop()








