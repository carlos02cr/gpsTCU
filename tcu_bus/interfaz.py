import tkinter as tk
import threading
import subprocess
from funcionesGPS import manejarGPS
import csv
import os

class VirtualKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INICIO DE SESION")
        self.geometry("800x480")  # Ajustar a las dimensiones de la pantalla táctil

        # Variables para el nombre de usuario y contraseña
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # Variables para el hilo del GPS
        self.gps_thread = None
        self.stop_event = threading.Event()

        # Crear los widgets de la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Crear el marco para la pantalla de inicio de sesión
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(expand=True, fill='both')

        # Crear un marco para los campos de inicio de sesión
        self.login_inputs_frame = tk.Frame(self.login_frame)
        self.login_inputs_frame.pack(pady=10)

        # Campos de inicio de sesión organizados en 3 columnas y 2 filas
        tk.Label(self.login_inputs_frame, text="USUARIO:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_inputs_frame, textvariable=self.username)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        tk.Label(self.login_inputs_frame, text="CONTRASEÑA:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_inputs_frame, textvariable=self.password, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        # Crear el teclado virtual y mostrarlo en el login_frame
        self.keyboard_frame = tk.Frame(self.login_frame)
        self.keyboard_frame.pack(pady=10)

        self.create_keyboard()  # Llamar a la función para crear el teclado

        # Botones para iniciar sesión y registrarse
        tk.Button(self.login_frame, text="INICIAR", command=self.send_data).pack(pady=5)
        tk.Button(self.login_frame, text="REGISTRARSE", command=self.show_registration).pack(pady=5)

        # Crear el marco para la sección del viaje (inicialmente oculto)
        self.trip_frame = tk.Frame(self)

        # Botones dentro de la sección del viaje
        tk.Button(self.trip_frame, text="Iniciar Viaje", command=self.start_gps, width=20, height=3).pack(pady=20)
        tk.Button(self.trip_frame, text="Finalizar Viaje", command=self.stop_gps, width=20, height=3).pack(pady=20)

        # Botón "Cerrar Sesión"
        tk.Button(self.trip_frame, text="Cerrar Sesión", command=self.logout, width=20, height=3).pack(pady=20)

        # Etiqueta para mostrar mensajes de estado
        self.status_message = tk.StringVar()
        tk.Label(self.trip_frame, textvariable=self.status_message, fg="green").pack(pady=10)

        # Crear el marco para la sección de registro (inicialmente oculta)
        self.registration_frame = tk.Frame(self)

        # Campos para la sección de registro
        tk.Label(self.registration_frame, text="Registro").pack(pady=10)
        self.operator_id = tk.StringVar()
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.register_username = tk.StringVar()
        self.register_password = tk.StringVar()

        # Crear el marco para los campos de registro
        self.registration_inputs_frame = tk.Frame(self.registration_frame)
        self.registration_inputs_frame.pack(pady=5)

        # Campos de registro organizados en 3 columnas y 2 filas
        tk.Label(self.registration_inputs_frame, text="ID Operador:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.registration_inputs_frame, textvariable=self.operator_id).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.registration_inputs_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.registration_inputs_frame, textvariable=self.name).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.registration_inputs_frame, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self.registration_inputs_frame, textvariable=self.phone).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.registration_inputs_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(self.registration_inputs_frame, textvariable=self.email).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.registration_inputs_frame, text="Usuario:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(self.registration_inputs_frame, textvariable=self.register_username).grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.registration_inputs_frame, text="Contraseña:").grid(row=5, column=0, padx=5, pady=5)
        tk.Entry(self.registration_inputs_frame, textvariable=self.register_password, show="*").grid(row=5, column=1, padx=5, pady=5)

        # Botón para registrar el usuario
        tk.Button(self.registration_frame, text="Registrar", command=self.register_user).pack(pady=10)

        # Botón para volver atrás al login, ubicado en la esquina superior izquierda
        tk.Button(self.registration_frame, text="Volver Atrás", command=self.show_login).place(x=10, y=10)

    def create_keyboard(self):
        # Definir las teclas para el teclado virtual
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR'
        ]

        # Crear el marco para el teclado dentro del keyboard_frame
        keyboard_frame = tk.Frame(self.keyboard_frame)
        keyboard_frame.pack(pady=20)

        # Colocar las teclas en una cuadrícula
        for index, key in enumerate(keys):
            button = tk.Button(keyboard_frame, text=key, width=6, command=lambda k=key: self.key_press(k))
            row, col = divmod(index, 10)
            button.grid(row=row, column=col, padx=2, pady=2)

    def key_press(self, key):
        # Manejar los eventos de las teclas del teclado virtual
        focused_widget = self.focus_get()
        if isinstance(focused_widget, tk.Entry):
            if key == "BORRAR":
                # Borrar el último carácter
                current_text = focused_widget.get()
                focused_widget.delete(0, tk.END)
                focused_widget.insert(0, current_text[:-1])
            else:
                # Insertar la tecla presionada
                focused_widget.insert(tk.END, key)

    def send_data(self):
        # Validar el inicio de sesión, verificando usuario y contraseña en el CSV
        entered_username = self.username.get()
        entered_password = self.password.get()

        # Verificar si el archivo CSV existe
        if not os.path.isfile('usuarios_registrados.csv'):
            self.status_message.set("Error: No se ha encontrado el archivo CSV.")
            return

        # Leer el archivo CSV y verificar credenciales
        with open('usuarios_registrados.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Usuario'] == entered_username and row['Contraseña'] == entered_password:
                    # Si las credenciales son correctas, mostrar la pantalla de viaje
                    self.status_message.set("Inicio de sesión exitoso.")
                    self.login_frame.pack_forget()  # Ocultar pantalla de login
                    self.trip_frame.pack(expand=True, fill='both')  # Mostrar pantalla de viaje
                    self.keyboard_frame.pack_forget()  # Ocultar teclado
                    return

        # Si no coincide, mostrar un mensaje de error
        self.status_message.set("Usuario o contraseña incorrectos.")

    def show_registration(self):
        # Ocultar la pantalla de login y mostrar la de registro
        self.login_frame.pack_forget()
        self.registration_frame.pack(expand=True, fill='both')

    def show_login(self):
        # Ocultar la pantalla de registro y volver a mostrar la de login
        self.registration_frame.pack_forget()
        self.login_frame.pack(expand=True, fill='both')

    def register_user(self):
        # Registrar un
