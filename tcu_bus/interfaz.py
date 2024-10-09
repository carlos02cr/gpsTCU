import tkinter as tk
import threading
from funcionesGPS import manejarGPS
from registro import RegistrationApp, verificar_operador


class VirtualKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INICIO DE SESION")
        # Ajustar a las dimensiones de la pantalla táctil
        self.geometry("800x480")

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
        tk.Entry(self.login_frame, textvariable=self.password,
                 show="*").pack(pady=10)

        # Crear el teclado y almacenarlo en self.keyboard_frame
        self.keyboard_frame = tk.Frame(self.login_frame)
        self.keyboard_frame.pack(pady=10)

        self.create_keyboard()

        tk.Button(self.login_frame, text="INICIAR",
                  command=self.send_data).pack(pady=5)
        tk.Button(self.login_frame, text="REGISTRARSE",
                  command=self.show_registration).pack(pady=5)

        # Crear un marco para la sección del viaje (inicialmente oculta)
        self.trip_frame = tk.Frame(self)

        tk.Button(self.trip_frame, text="Iniciar Viaje",
                  command=self.start_gps, width=20, height=3).pack(pady=20)
        tk.Button(self.trip_frame, text="Finalizar Viaje",
                  command=self.stop_gps, width=20, height=3).pack(pady=20)

        # Label para mostrar mensajes de estado
        self.status_message = tk.StringVar()
        tk.Label(self.trip_frame, textvariable=self.status_message,
                 fg="green").pack(pady=10)

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

        usuario = self.username.get()
        contraseña = self.password.get()

        if verificar_operador(usuario, contraseña):
            print(f"Usuario: {usuario}")
            print(f"Contraseña: {contraseña}")

            # Ocultar el marco de inicio de sesión y mostrar el marco del viaje
            self.login_frame.pack_forget()
            self.trip_frame.pack(expand=True, fill='both')

            # Ocultar el teclado después del inicio de sesión
            self.keyboard_frame.pack_forget()
        else:
            print("Error: Usuario o contraseña incorrectos.")

    def show_registration(self):
        self.withdraw()
        # Pass the main window as an argument
        registration_app = RegistrationApp(self)
        registration_app.mainloop()
        # self.login_frame.pack_forget()
        # self.registration_frame.pack(expand=True, fill='both')

    def return_to_main(self):
        # Show the main window again when returning from registration
        self.deiconify()

    def show_login(self):
        self.registration_frame.pack_forget()
        self.login_frame.pack(expand=True, fill='both')

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
            # Hacer que el hilo se cierre
            # cuando se cierra el programa principal
            daemon=True
        )
        self.gps_thread.start()
        # Actualizar el mensaje de estado
        self.status_message.set("Lectura de GPS iniciada.")
        print("Lectura de GPS iniciada.")

    def stop_gps(self):
        if self.gps_thread and self.gps_thread.is_alive():
            # Señalar al hilo que se detenga
            self.stop_event.set()
            self.gps_thread.join()  # Esperar a que el hilo termine
            # Actualizar el mensaje de estado
            self.status_message.set("Lectura de GPS finalizada.")
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
