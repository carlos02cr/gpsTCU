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

        # Campo para el nombre de usuario
        tk.Label(self.login_frame, text="USUARIO:").pack(pady=10)
        self.username_entry = tk.Entry(self.login_frame, textvariable=self.username)
        self.username_entry.pack(pady=10)

        # Campo para la contraseña
        tk.Label(self.login_frame, text="CONTRASEÑA:").pack(pady=10)
        self.password_entry = tk.Entry(self.login_frame, textvariable=self.password, show="*")
        self.password_entry.pack(pady=10)

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

        # Crear los campos de entrada para el registro
        tk.Label(self.registration_frame, text="ID Operador:").pack(pady=5)
        tk.Entry(self.registration_frame, textvariable=self.operator_id).pack(pady=5)

        tk.Label(self.registration_frame, text="Nombre:").pack(pady=5)
        tk.Entry(self.registration_frame, textvariable=self.name).pack(pady=5)

        tk.Label(self.registration_frame, text="Teléfono:").pack(pady=5)
        tk.Entry(self.registration_frame, textvariable=self.phone).pack(pady=5)

        tk.Label(self.registration_frame, text="Email:").pack(pady=5)
        tk.Entry(self.registration_frame, textvariable=self.email).pack(pady=5)

        tk.Label(self.registration_frame, text="Usuario:").pack(pady=5)
        tk.Entry(self.registration_frame, textvariable=self.register_username).pack(pady=5)

        tk.Label(self.registration_frame, text="Contraseña:").pack(pady=5)
        tk.Entry(self.registration_frame, textvariable=self.register_password, show="*").pack(pady=5)

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
        # Registrar un nuevo usuario, guardando los datos en un archivo CSV
        file_exists = os.path.isfile('usuarios_registrados.csv')

        # Crear un diccionario con los datos del usuario
        user_data = {
            "ID Operador": self.operator_id.get(),
            "Nombre": self.name.get(),
            "Teléfono": self.phone.get(),
            "Email": self.email.get(),
            "Usuario": self.register_username.get(),
            "Contraseña": self.register_password.get()
        }

        # Guardar los datos en un archivo CSV
        with open('usuarios_registrados.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=user_data.keys())

            # Si el archivo no existe, escribir los encabezados
            if not file_exists:
                writer.writeheader()

            # Escribir los datos del usuario
            writer.writerow(user_data)

        # Vaciar los campos después de registrar al usuario
        self.operator_id.set("")
        self.name.set("")
        self.phone.set("")
        self.email.set("")
        self.register_username.set("")
        self.register_password.set("")

        # Mostrar mensaje de éxito y volver al login
        self.status_message.set("Registrado exitosamente.")
        self.show_login()

    def start_gps(self):
        # Iniciar el GPS en un hilo separado
        if self.gps_thread and self.gps_thread.is_alive():
            print("La lectura de GPS ya está en progreso.")
            return

        # Limpiar el evento de parada antes de comenzar
        self.stop_event.clear()

        # Iniciar el hilo de GPS
        self.gps_thread = threading.Thread(target=manejarGPS, args=(self.stop_event,), daemon=True)
        self.gps_thread.start()
        self.status_message.set("Lectura de GPS iniciada.")
        print("Lectura de GPS iniciada.")

    def stop_gps(self):
        # Detener el hilo de GPS
        if self.gps_thread and self.gps_thread.is_alive():
            self.stop_event.set()  # Señalar que se detenga
            self.gps_thread.join()  # Esperar a que el hilo termine
            self.status_message.set("Lectura de GPS finalizada.")
            print("Lectura de GPS finalizada.")
        else:
            print("La lectura de GPS no está en ejecución.")

    def logout(self):
        # Función para cerrar sesión, detener el GPS y volver al login
        self.stop_gps()  # Detener el GPS si está activo
        self.username.set("")  # Limpiar el campo de usuario
        self.password.set("")  # Limpiar el campo de contraseña
        self.keyboard_frame.pack(pady=10)  # Volver a mostrar el teclado
        self.trip_frame.pack_forget()  # Ocultar el marco del viaje
        self.login_frame.pack(expand=True, fill='both')  # Mostrar el login nuevamente

    def on_closing(self):
        # Asegurarse de que el GPS se detenga antes de cerrar la aplicación
        self.stop_gps()
        self.destroy()

if __name__ == "__main__":
    app = VirtualKeyboard()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)  # Manejar el cierre de la ventana
    app.mainloop()
