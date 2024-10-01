import tkinter as tk
import threading
import bcrypt
import db_manager  # Importamos las funciones desde el archivo db_manager.py
from funcionesGPS import manejarGPS

class VirtualKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INICIO DE SESION")
        self.geometry("800x480")  # Ajusta a las dimensiones de la pantalla táctil

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # Variables para el registro
        self.nombre = tk.StringVar()
        self.cedula = tk.StringVar()
        self.telefono = tk.StringVar()
        self.usuario_registro = tk.StringVar()
        self.contrasena_registro = tk.StringVar()

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

        tk.Button(self.login_frame, text="INICIAR", command=self.send_data).pack(pady=10)
        tk.Button(self.login_frame, text="REGISTRAR", command=self.mostrar_registro).pack(pady=10)

        # Create a frame for registration (initially hidden)
        self.registration_frame = tk.Frame(self)

        tk.Label(self.registration_frame, text="NOMBRE:").pack(pady=10)
        tk.Entry(self.registration_frame, textvariable=self.nombre).pack(pady=10)

        tk.Label(self.registration_frame, text="CÉDULA:").pack(pady=10)
        tk.Entry(self.registration_frame, textvariable=self.cedula).pack(pady=10)

        tk.Label(self.registration_frame, text="TELÉFONO:").pack(pady=10)
        tk.Entry(self.registration_frame, textvariable=self.telefono).pack(pady=10)

        tk.Label(self.registration_frame, text="USUARIO:").pack(pady=10)
        tk.Entry(self.registration_frame, textvariable=self.usuario_registro).pack(pady=10)

        tk.Label(self.registration_frame, text="CONTRASEÑA:").pack(pady=10)
        tk.Entry(self.registration_frame, textvariable=self.contrasena_registro, show="*").pack(pady=10)

        tk.Button(self.registration_frame, text="REGISTRAR USUARIO", command=self.registrar_operador).pack(pady=10)
        tk.Button(self.registration_frame, text="VOLVER", command=self.volver_login).pack(pady=10)

        # Create a frame for the trip section (initially hidden)
        self.trip_frame = tk.Frame(self)

        tk.Button(self.trip_frame, text="Iniciar Viaje",
                  command=self.start_gps, width=20, height=3).pack(pady=50)
        tk.Button(self.trip_frame, text="Finalizar Viaje",
                  command=self.stop_gps, width=20, height=3).pack(pady=50)

    def mostrar_registro(self):
        # Ocultar la pantalla de inicio de sesión y mostrar el formulario de registro
        self.login_frame.pack_forget()
        self.registration_frame.pack(expand=True, fill='both')

    def volver_login(self):
        # Ocultar el formulario de registro y volver a la pantalla de inicio de sesión
        self.registration_frame.pack_forget()
        self.login_frame.pack(expand=True, fill='both')

    def send_data(self):
        usuario = self.username.get()
        contrasena = self.password.get()

        # Verificar credenciales con la base de datos
        if db_manager.verificar_operador(self.conn, usuario, contrasena):
            print(f"Usuario: {usuario}")
            print(f"Contraseña: {contrasena}")

            # Ocultar la pantalla de inicio de sesión y mostrar la sección de viaje
            self.login_frame.pack_forget()
            self.trip_frame.pack(expand=True, fill='both')
        else:
            print("Error: Usuario o contraseña incorrectos")

    # Función para registrar nuevos operadores
    def registrar_operador(self):
        nombre = self.nombre.get()
        cedula = self.cedula.get()
        telefono = self.telefono.get()
        usuario = self.usuario_registro.get()
        contrasena = self.contrasena_registro.get()

        # Hashear la contraseña
        contrasena_hash = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

        # Insertar el nuevo operador en la base de datos
        db_manager.insertar_operador(self.conn, usuario, telefono, nombre, contrasena_hash)
        print(f"Usuario {usuario} registrado correctamente")
        self.volver_login()  # Volver a la pantalla de inicio de sesión después de registrar

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
