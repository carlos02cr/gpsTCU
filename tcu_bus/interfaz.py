import tkinter as tk
import threading
import bcrypt
import db_manager  # Importamos las funciones desde el archivo db_manager.py
from funcionesGPS import manejarGPS

class VirtualKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INICIO DE SESION")
        self.geometry("800x480")  # Adjust to the dimensions of the touchscreen

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.gps_thread = None
        self.stop_event = threading.Event()

        # Conectar a la base de datos y crear tabla si no existe
        self.conn = db_manager.conectar_db()
        db_manager.crear_tabla(self.conn)

        self.create_widgets()

    def create_widgets(self):

        # Create a frame for login
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(expand=True, fill='both')

        tk.Label(self.login_frame, text="USUARIO:").pack(pady=10)
        tk.Entry(self.login_frame, textvariable=self.username).pack(pady=10)

        tk.Label(self.login_frame, text="CONTRASEÑA:").pack(pady=10)
        tk.Entry(self.login_frame, textvariable=self.password, show="*").pack(pady=10)

        # Create the keyboard and store it in self.keyboard_frame
        self.keyboard_frame = tk.Frame(self.login_frame)
        self.keyboard_frame.pack(pady=10)

        self.create_keyboard()

        tk.Button(self.login_frame, text="INICIAR", command=self.send_data).pack(pady=10)
        tk.Button(self.login_frame, text="REGISTRAR", command=self.registrar_operador).pack(pady=10)

        # Create a frame for the trip section (initially hidden)
        self.trip_frame = tk.Frame(self)

        tk.Button(self.trip_frame, text="Iniciar Viaje",
                  command=self.start_gps, width=20, height=3).pack(pady=50)
        tk.Button(self.trip_frame, text="Finalizar Viaje",
                  command=self.stop_gps, width=20, height=3).pack(pady=50)

    def create_keyboard(self):
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR'
        ]

        keyboard_frame = tk.Frame(self.keyboard_frame)
        keyboard_frame.pack(pady=20)

        for index, key in enumerate(keys):
            button = tk.Button(
                keyboard_frame, text=key, width=6,
                command=lambda k=key: self.key_press(k)
            )
            row, col = divmod(index, 10)
            button.grid(row=row, column=col, padx=2, pady=2)

    def key_press(self, key):
        focused_widget = self.focus_get()
        if isinstance(focused_widget, tk.Entry):
            if key == "BORRAR":
                current_text = focused_widget.get()
                focused_widget.delete(0, tk.END)
                focused_widget.insert(0, current_text[:-1])
            elif key == "ESPACIO":
                focused_widget.insert(tk.END, ' ')
            else:
                focused_widget.insert(tk.END, key)

    # Función para verificar las credenciales con la base de datos
    def send_data(self):
        usuario = self.username.get()
        contrasena = self.password.get()

        # Verificar credenciales con la base de datos
        if db_manager.verificar_operador(self.conn, usuario, contrasena):
            print(f"Usuario: {usuario}")
            print(f"Contraseña: {contrasena}")

            # Hide the login frame and show the trip frame
            self.login_frame.pack_forget()
            self.trip_frame.pack(expand=True, fill='both')

            # Hide the keyboard after login
            self.keyboard_frame.pack_forget()
        else:
            print("Error: Usuario o contraseña incorrectos")

    # Función para registrar nuevos operadores
    def registrar_operador(self):
        usuario = self.username.get()
        contrasena = self.password.get()

        # Insertar el nuevo operador en la base de datos
        db_manager.insertar_operador(self.conn, usuario, "555-1234", "email@example.com", contrasena)
        print(f"Usuario {usuario} registrado correctamente")

    def start_gps(self):
        if self.gps_thread and self.gps_thread.is_alive():
            print("La lectura de GPS ya está en progreso.")
            return

        # Clear the stop event before starting
        self.stop_event.clear()

        # Start the GPS reading in a separate thread
        self.gps_thread = threading.Thread(
            target=manejarGPS,
            args=(self.stop_event,),
            daemon=True  # Daemonize thread to exit when the main program exits
        )
        self.gps_thread.start()
        print("Lectura de GPS iniciada.")

    def stop_gps(self):
        if self.gps_thread and self.gps_thread.is_alive():
            # Signal the thread to stop
            self.stop_event.set()
            self.gps_thread.join()  # Wait for the thread to finish
            print("Lectura de GPS finalizada.")
        else:
            print("La lectura de GPS no está en ejecución.")

    def on_closing(self):
        # Ensure that the GPS thread is stopped before closing
        self.stop_gps()
        self.conn.close()  # Cerrar la conexión a la base de datos
        self.destroy()


if __name__ == "__main__":
    app = VirtualKeyboard()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
