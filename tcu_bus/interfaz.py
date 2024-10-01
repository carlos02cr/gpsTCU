import tkinter as tk
import threading
import subprocess
from funcionesGPS import manejarGPS

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

        # Crear un marco para la sección del viaje (inicialmente oculta)
        self.trip_frame = tk.Frame(self)

        tk.Button(self.trip_frame, text="Iniciar Viaje",
                  command=self.start_gps, width=20, height=3).pack(pady=20)
        tk.Button(self.trip_frame, text="Finalizar Viaje",
                  command=self.stop_gps, width=20, height=3).pack(pady=20)

        # Label para mostrar mensajes de estado
        self.status_message = tk.StringVar()
        tk.Label(self.trip_frame, textvariable=self.status_message, fg="green").pack(pady=10)

        # Crear marco para la sección de registro (inicialmente oculta)
        self.registration_frame = tk.Frame(self)

        tk.Label(self.registration_frame, text="Registro").pack(pady=10)
        self.operator_id = tk.StringVar()
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.register_username = tk.StringVar()
        self.register_password = tk.StringVar()

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

        tk.Button(self.registration_frame, text="Registrar", command=self.register_user).pack(pady=10)
        tk.Button(self.registration_frame, text="Volver", command=self.show_login).pack(pady=5)

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
            else:
                focused_widget.insert(tk.END, key)

    def send_data(self):
        print(f"Usuario: {self.username.get()}")
        print(f"Contraseña: {self.password.get()}")

        # Ocultar el marco de inicio de sesión y mostrar el marco del viaje
        self.login_frame.pack_forget()
        self.trip_frame.pack(expand=True, fill='both')

        # Ocultar el teclado después del inicio de sesión
        self.keyboard_frame.pack_forget()

    def show_registration(self):
        self.login_frame.pack_forget()
        self.registration_frame.pack(expand=True, fill='both')

    def show_login(self):
        self.registration_frame.pack_forget()
        self.login_frame.pack(expand=True, fill='both')

    def register_user(self):
        # Aquí puedes agregar la lógica para guardar el usuario en la base de datos
        print(f"Registrando usuario: {self.register_username.get()}")
        print(f"ID Operador: {self.operator_id.get()}, Nombre: {self.name.get()}, Teléfono: {self.phone.get()}, Email: {self.email.get()}, Contraseña: {self.register_password.get()}")
        # Mensaje de éxito o lógica para agregar a la base de datos
        self.status_message.set("Registrado exitosamente.")
        self.show_login()  # Regresar al inicio de sesión después de registrar

    def start_gps(self):
        if self.gps_thread and self.gps_thread.is_alive():
            print("La lectura de GPS ya está en progreso.")
            return

        # Limpiar el evento de parada antes de comenzar
        self.stop_event.clear()

        # Iniciar la lectura de GPS en un hilo separado
        self.gps_thread = threading.Thread(
            target=manejarGPS,
            args=(self.stop_event,),
            daemon=True  # Hacer que el hilo se cierre cuando se cierra el programa principal
        )
        self.gps_thread.start()
        self.status_message.set("Lectura de GPS iniciada.")  # Actualizar el mensaje de estado
        print("Lectura de GPS iniciada.")

    def stop_gps(self):
        if self.gps_thread and self.gps_thread.is_alive():
            # Señalar al hilo que se detenga
            self.stop_event.set()
            self.gps_thread.join()  # Esperar a que el hilo termine
            self.status_message.set("Lectura de GPS finalizada.")  # Actualizar el mensaje de estado
            print("Lectura de GPS finalizada.")
        else:
            print("La lectura de GPS no está en ejecución.")

    def on_closing(self):
        # Asegurarse de que el hilo de GPS se detenga antes de cerrar
        self.stop_gps()
        self.destroy()


if __name__ == "__main__":
    app = VirtualKeyboard()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
