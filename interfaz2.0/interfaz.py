import tkinter as tk
import threading
import sqlite3
import os
from registro import RegistrationApp
from funcionesGPS import manejarGPS

# Función para verificar las credenciales del operador en la base de datos SQLite
def verificar_operador(usuario, contraseña):
    conn = sqlite3.connect('operadores.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM operadores WHERE username = ? AND password = ?", (usuario, contraseña))
    operador = cursor.fetchone()  # Si se encuentra un resultado, se devolverá una fila
    conn.close()

    if operador:  # Si se encontró un operador
        return True
    return False

class VirtualKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INICIO DE SESION")
        self.geometry("800x480")  # Dimensiones ajustadas a la pantalla de la Raspberry Pi

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.gps_thread = None
        self.stop_event = threading.Event()

        self.create_widgets()

    def create_widgets(self):
        # Crear un marco para el inicio de sesión, más compacto
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(expand=True, fill='both', padx=5, pady=5)

        # Etiqueta y campo de usuario
        tk.Label(self.login_frame, text="USUARIO:", font=("Arial", 12)).pack(pady=3)
        tk.Entry(self.login_frame, textvariable=self.username, font=("Arial", 12), width=25).pack(pady=3)

        # Etiqueta y campo de contraseña
        tk.Label(self.login_frame, text="CONTRASEÑA:", font=("Arial", 12)).pack(pady=3)
        tk.Entry(self.login_frame, textvariable=self.password, show="*", font=("Arial", 12), width=25).pack(pady=3)

        # Crear el teclado y almacenarlo en self.keyboard_frame
        self.keyboard_frame = tk.Frame(self.login_frame)
        self.keyboard_frame.pack(pady=5)

        self.create_keyboard()

        # Botones para iniciar y registrarse
        tk.Button(self.login_frame, text="INICIAR", command=self.send_data, font=("Arial", 12), width=15).pack(pady=3)
        tk.Button(self.login_frame, text="REGISTRARSE", command=self.show_registration, font=("Arial", 12), width=15).pack(pady=3)

        # Marco de acciones de viaje
        self.trip_frame = tk.Frame(self)

        tk.Button(self.trip_frame, text="Iniciar Viaje", command=self.start_gps, width=20, height=3).pack(pady=5)
        tk.Button(self.trip_frame, text="Finalizar Viaje", command=self.stop_gps, width=20, height=3).pack(pady=5)

        # Botón para cerrar sesión
        tk.Button(self.trip_frame, text="Cerrar Sesión", command=self.logout, width=20, height=3).pack(pady=5)

        # Etiqueta para mostrar el estado
        self.status_message = tk.StringVar()
        tk.Label(self.trip_frame, textvariable=self.status_message, fg="green", font=("Arial", 12)).pack(pady=5)

    def create_keyboard(self):
        # Teclas agrupadas en un diseño compacto
        keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', '@']
        ]

        keyboard_frame = tk.Frame(self.keyboard_frame)
        keyboard_frame.pack(pady=5)

        # Crear botón "BORRAR" que ocupe el lado derecho de la tercera y cuarta fila
        button_borrar = tk.Button(keyboard_frame, text="<-", width=3, height=4, font=("Arial", 8), command=lambda k="BORRAR": self.key_press(k))
        button_borrar.grid(row=2, column=9, rowspan=2, padx=1, pady=1)  # Botón en la tercera y cuarta fila, justo al lado de la "L" y "@"

        # Colocar las teclas en la disposición correcta
        for row_index, row in enumerate(keys):
            for col_index, key in enumerate(row):
                button = tk.Button(keyboard_frame, text=key, width=4, command=lambda k=key: self.key_press(k))
                button.grid(row=row_index, column=col_index, padx=1, pady=1)

        # Tecla "Espacio" larga en la última fila
        button_space = tk.Button(keyboard_frame, text="Espacio", width=40, command=lambda k=' ': self.key_press(k))
        button_space.grid(row=5, column=0, columnspan=11, padx=1, pady=1)

    def key_press(self, key):
        focused_widget = self.focus_get()
        if isinstance(focused_widget, tk.Entry):
            if key == "BORRAR":
                current_text = focused_widget.get()
                focused_widget.delete(0, tk.END)
                focused_widget.insert(0, current_text[:-1])
            else:
                focused_widget.insert(tk.END, key)

    def send_data(self):
        usuario = self.username.get()
        contraseña = self.password.get()

        if verificar_operador(usuario, contraseña):
            self.login_frame.pack_forget()
            self.trip_frame.pack(expand=True, fill='both')
            self.keyboard_frame.pack_forget()
        else:
            print("Error: Usuario o contraseña incorrectos.")

    def show_registration(self):
        self.withdraw()
        registration_app = RegistrationApp(self)
        registration_app.mainloop()

    def return_to_main(self):
        self.deiconify()

    def start_gps(self):
        if self.gps_thread and self.gps_thread.is_alive():
            return

        self.stop_event.clear()
        self.gps_thread = threading.Thread(target=manejarGPS, daemon=True)
        self.gps_thread.start()
        self.status_message.set("Lectura de GPS iniciada.")

    def stop_gps(self):
        if self.gps_thread and self.gps_thread.is_alive():
            self.stop_event.set()
            self.gps_thread.join()
            self.status_message.set("Lectura de GPS finalizada.")

    def process_gps_data(self, gps_data):
        # Aquí puedes mostrar los datos en la interfaz
        self.status_message.set(f"Datos GPS: {gps_data}")

    def logout(self):
        if self.gps_thread and self.gps_thread.is_alive():
            self.stop_gps()

        self.trip_frame.pack_forget()
        self.username.set("")
        self.password.set("")

        self.keyboard_frame.pack(pady=5)
        self.login_frame.pack(expand=True, fill='both')

    def on_closing(self):
        if self.gps_thread and self.gps_thread.is_alive():
            self.stop_gps()
        self.destroy()

if __name__ == "__main__":
    app = VirtualKeyboard()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
