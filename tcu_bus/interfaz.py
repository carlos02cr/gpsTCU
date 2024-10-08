import tkinter as tk
import threading
import csv
import os
from funcionesGPS import manejarGPS


# Función para verificar las credenciales del operador en el archivo CSV
# Función para verificar las credenciales del operador en el archivo CSV
def verificar_operador(usuario, contraseña):
    # Verifica si el archivo de usuarios existe
    if not os.path.exists('usuarios.csv'):
        return False

    # Leer el archivo CSV y verificar las credenciales
    with open('usuarios.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Usuario'] == usuario and row['Contraseña'] == contraseña:
                return True
    return False


class RegistrationApp(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Registro de Operadores")
        self.geometry("800x480")

        self.operator_id = tk.StringVar()
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.register_username = tk.StringVar()
        self.register_password = tk.StringVar()

        self.registration_message = tk.StringVar()  # Variable para el mensaje de éxito

        # Crear la interfaz de registro
        self.create_widgets()

    def create_widgets(self):
        # Configuramos una cuadrícula con dos columnas para los campos de entrada y etiquetas

        # Primera columna (etiquetas)
        tk.Label(self, text="ID Operador:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self, text="Teléfono:").grid(row=2, column=1, padx=10, pady=5, sticky="e")
        tk.Label(self, text="Email:").grid(row=3, column=1, padx=10, pady=5, sticky="e")
        tk.Label(self, text="Usuario:").grid(row=4, column=2, padx=10, pady=5, sticky="e")
        tk.Label(self, text="Contraseña:").grid(row=5, column=2, padx=10, pady=5, sticky="e")

        # Segunda columna (campos de entrada)
        self.id_entry = tk.Entry(self, textvariable=self.operator_id)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5)

        self.name_entry = tk.Entry(self, textvariable=self.name)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.phone_entry = tk.Entry(self, textvariable=self.phone)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5)

        self.email_entry = tk.Entry(self, textvariable=self.email)
        self.email_entry.grid(row=3, column=1, padx=10, pady=5)

        self.user_entry = tk.Entry(self, textvariable=self.register_username)
        self.user_entry.grid(row=4, column=1, padx=10, pady=5)

        self.pass_entry = tk.Entry(self, textvariable=self.register_password, show="*")
        self.pass_entry.grid(row=5, column=1, padx=10, pady=5)

        # Botón para registrar el usuario (ocupa ambas columnas)
        tk.Button(self, text="Registrar", command=self.register_user).grid(row=6, column=0, columnspan=2, pady=10)

        # Botón para volver atrás al login (ocupa ambas columnas)
        tk.Button(self, text="Volver al Login", command=self.close_window).grid(row=7, column=0, columnspan=2, pady=10)

        # Label para mostrar el mensaje de éxito
        self.success_label = tk.Label(self, textvariable=self.registration_message, fg="green")
        self.success_label.grid(row=8, column=0, columnspan=2, pady=10)

        # Añadir el teclado en la ventana de registro
        self.create_keyboard()

    def create_keyboard(self):
        # Crear el teclado para la ventana de registro
        keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
                'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR']

    # Mover el teclado a la fila 7 para que esté más cerca de los campos de entrada
        keyboard_frame = tk.Frame(self)
        keyboard_frame.grid(row=8, column=0, columnspan=2, pady=10)

        for index, key in enumerate(keys):
            button = tk.Button(keyboard_frame, text=key, width=6, command=lambda k=key: self.key_press(k))
            row, col = divmod(index, 10)
            button.grid(row=row, column=col, padx=2, pady=2)


   


    def key_press(self, key):
        # Insertar caracteres en el campo de entrada enfocado
        focused_widget = self.focus_get()
        if isinstance(focused_widget, tk.Entry):
            if key == "BORRAR":
                current_text = focused_widget.get()
                focused_widget.delete(0, tk.END)
                focused_widget.insert(0, current_text[:-1])
            else:
                focused_widget.insert(tk.END, key)

    def register_user(self):
        # Registrar un nuevo usuario y guardar en un archivo CSV
        file_exists = os.path.isfile('usuarios.csv')

        user_data = {
            "ID Operador": self.operator_id.get(),
            "Nombre": self.name.get(),
            "Teléfono": self.phone.get(),
            "Email": self.email.get(),
            "Usuario": self.register_username.get(),
            "Contraseña": self.register_password.get()
        }

        with open('usuarios.csv', mode='a', newline='') as file:
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

        # Mostrar mensaje de éxito
        self.registration_message.set("¡Se ha registrado exitosamente!")

    def close_window(self):
        self.destroy()
        self.master.return_to_main()


class VirtualKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INICIO DE SESION")
        self.geometry("800x480")  # Ajustar a las dimensiones de la pantalla táctil

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.gps_thread = None
        self.stop_event = threading.Event()

        self.create_widgets()

    def create_widgets(self):
        # Columna izquierda (ID Operador, Nombre, Teléfono)
        tk.Label(self, text="ID Operador:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.id_entry = tk.Entry(self, textvariable=self.operator_id)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = tk.Entry(self, textvariable=self.name)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Teléfono:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.phone_entry = tk.Entry(self, textvariable=self.phone)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Columna derecha (Email, Usuario, Contraseña)
        tk.Label(self, text="Email:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.email_entry = tk.Entry(self, textvariable=self.email)
        self.email_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Usuario:").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.user_entry = tk.Entry(self, textvariable=self.register_username)
        self.user_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Contraseña:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.pass_entry = tk.Entry(self, textvariable=self.register_password, show="*")
        self.pass_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # Botón para registrar el usuario (ocupa ambas columnas)
        tk.Button(self, text="Registrar", command=self.register_user).grid(row=3, column=0, columnspan=4, pady=10)

        # Botón para volver atrás al login (ocupa ambas columnas)
        tk.Button(self, text="Volver al Login", command=self.close_window).grid(row=4, column=0, columnspan=4, pady=10)

        # Label para mostrar el mensaje de éxito
        self.success_label = tk.Label(self, textvariable=self.registration_message, fg="green")
        self.success_label.grid(row=5, column=0, columnspan=4, pady=10)

        # Añadir el teclado en la ventana de registro
        self.create_keyboard()



    def create_keyboard(self):
        keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
                'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR']

        keyboard_frame = tk.Frame(self.keyboard_frame)
        keyboard_frame.pack(pady=20)

        for index, key in enumerate(keys):
            button = tk.Button(keyboard_frame, text=key, width=6, command=lambda k=key: self.key_press(k))
            row, col = divmod(index, 10)
            button.grid(row=row, column=col, padx=2, pady=2)

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

 
# Función para verificar las credenciales del operador en el archivo CSV
def verificar_operador(usuario, contraseña):
    # Verifica si el archivo de usuarios existe
    if not os.path.exists('usuarios.csv'):
        return False

    # Leer el archivo CSV y verificar las credenciales
    with open('usuarios.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Usuario'] == usuario and row['Contraseña'] == contraseña:
                return True
    return False


class VirtualKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INICIO DE SESION")
        self.geometry("800x480")  # Ajustar a las dimensiones de la pantalla táctil

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.gps_thread = None
        self.stop_event = threading.Event()

        self.create_widgets()

    def create_widgets(self):
        # Crear un marco para el inicio de sesión
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(expand=True, fill='both')

        tk.Label(self.login_frame, text="USUARIO:").pack(pady=10)
        tk.Entry(self.login_frame, textvariable=self.username).pack(pady=10)

        tk.Label(self.login_frame, text="CONTRASEÑA:").pack(pady=10)
        tk.Entry(self.login_frame, textvariable=self.password, show="*").pack(pady=10)

        # Crear el teclado y almacenarlo en self.keyboard_frame
        self.keyboard_frame = tk.Frame(self.login_frame)
        self.keyboard_frame.pack(pady=10)

        self.create_keyboard()

        tk.Button(self.login_frame, text="INICIAR", command=self.send_data).pack(pady=5)
        tk.Button(self.login_frame, text="REGISTRARSE", command=self.show_registration).pack(pady=5)

        self.trip_frame = tk.Frame(self)

        tk.Button(self.trip_frame, text="Iniciar Viaje", command=self.start_gps, width=20, height=3).pack(pady=20)
        tk.Button(self.trip_frame, text="Finalizar Viaje", command=self.stop_gps, width=20, height=3).pack(pady=20)

        # Agregar el botón de "Cerrar Sesión"
        tk.Button(self.trip_frame, text="Cerrar Sesión", command=self.logout, width=20, height=3).pack(pady=20)

        self.status_message = tk.StringVar()
        tk.Label(self.trip_frame, textvariable=self.status_message, fg="green").pack(pady=10)

    def create_keyboard(self):
        keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
                'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR']

        keyboard_frame = tk.Frame(self.keyboard_frame)
        keyboard_frame.pack(pady=20)

        for index, key in enumerate(keys):
            button = tk.Button(keyboard_frame, text=key, width=6, command=lambda k=key: self.key_press(k))
            row, col = divmod(index, 10)
            button.grid(row=row, column=col, padx=2, pady=2)

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

        # Verificar si las credenciales son correctas
        if verificar_operador(usuario, contraseña):
            print(f"Usuario: {usuario}")
            print(f"Contraseña: {contraseña}")

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
            print("La lectura de GPS ya está en progreso.")
            return

        self.stop_event.clear()

        self.gps_thread = threading.Thread(
            target=manejarGPS,
            args=(self.stop_event,),
            daemon=True
        )
        self.gps_thread.start()
        self.status_message.set("Lectura de GPS iniciada.")
        print("Lectura de GPS iniciada.")

    def stop_gps(self):
        if self.gps_thread and self.gps_thread.is_alive():
            self.stop_event.set()
            self.gps_thread.join()
            self.status_message.set("Lectura de GPS finalizada.")
            print("Lectura de GPS finalizada.")
        else:
            print("La lectura de GPS no está en ejecución.")

    # Función para cerrar sesión y regresar a la pantalla de login
    def logout(self):
        self.trip_frame.pack_forget()  # Ocultar la pantalla de viaje
        self.username.set("")  # Limpiar el campo de usuario
        self.password.set("")  # Limpiar el campo de contraseña

        # Mostrar el teclado y la pantalla de login nuevamente
        self.keyboard_frame.pack(pady=10)
        self.login_frame.pack(expand=True, fill='both')

    def on_closing(self):
        self.stop_gps()
        self.destroy()


if __name__ == "__main__":
    app = VirtualKeyboard()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
