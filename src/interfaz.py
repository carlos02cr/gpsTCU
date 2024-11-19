import tkinter as tk
import threading
from funcionesGPS import manejarGPS
from registro import InterfazRegistro, funcRegistro
import sqlite3
import requests

font = ("Helvetica", 12)


class InterfazMain(tk.Tk, funcRegistro):
    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda event:
                  self.attributes("-fullscreen", False))

        self.title("INICIO DE SESION")

        # Ajustar a las dimensiones de la pantalla táctil
        self.geometry("800x480")

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.gps_thread = None
        self.stop_event = threading.Event()

        self.create_database()
        self.create_widgets()

    def create_widgets(self):
        # Crear un marco para el inicio de sesión
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(fill='both')

        # Frame para entradas de usuario y contraseña
        self.user_pass_frame = tk.Frame(self.login_frame)
        self.user_pass_frame.pack(pady=20)

        tk.Label(self.user_pass_frame, text="USUARIO:",
                 font=font).pack(side=tk.LEFT, padx=5)
        tk.Entry(self.user_pass_frame, textvariable=self.username,
                 font=font).pack(side=tk.LEFT, padx=5)

        tk.Label(self.user_pass_frame, text="CONTRASEÑA:",
                 font=font).pack(side=tk.LEFT, padx=5)
        tk.Entry(self.user_pass_frame, textvariable=self.password,
                 show="*", font=font).pack(side=tk.LEFT, padx=5)

        # Frame para botones de registrar e iniciar
        self.inic_reg_frame = tk.Frame(self.login_frame)
        self.inic_reg_frame.pack(pady=5)

        tk.Button(self.inic_reg_frame, text="INICIAR", font=font,
                  command=self.login).pack(side=tk.LEFT, padx=80)
        tk.Button(self.inic_reg_frame, text="REGISTRARSE", font=font,
                  command=self.show_registration).pack(side=tk.LEFT, padx=80)

        # Label para mostrar mensajes de estado de inicio
        self.status_login = tk.StringVar()
        tk.Label(self.login_frame, textvariable=self.status_login,
                 fg="red", font=font).pack(expand=True, pady=1)

        # Crear el teclado y almacenarlo en self.keyboard_frame
        self.keyboard_frame = tk.Frame(self.login_frame)
        self.keyboard_frame.pack(expand=True, pady=10)
        self.create_keyboard()

        # Crear un marco para la sección del viaje (inicialmente oculta)
        self.trip_frame = tk.Frame(self)

        # Se hacen botones que cambian de color
        self.botonIniciar = tk.Button(self.trip_frame, text="Iniciar Viaje",
                                      font=font, command=self.start_gps,
                                      width=20, height=3)
        self.botonIniciar.pack(pady=20)

        self.botonFinalizar = tk.Button(self.trip_frame, text="Parar Viaje",
                                        font=font, command=self.stop_gps,
                                        width=20, height=3)
        self.botonFinalizar.pack(pady=20)

        self.botonLogout = tk.Button(self.trip_frame, text="Cerrar sesión",
                                     font=font, command=self.logout,
                                     width=20, height=3)
        self.botonLogout.pack(pady=20)

        # Label para mostrar mensajes de estado
        self.status_message = tk.StringVar()
        tk.Label(self.trip_frame, textvariable=self.status_message,
                 font=font, fg="green").pack(expand=True, pady=10)

    def create_keyboard(self):
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', '@', 'BORRAR'
        ]

        keyboard_frame = tk.Frame(self.keyboard_frame)
        keyboard_frame.pack(expand=True, pady=20)

        for index, key in enumerate(keys):
            button = tk.Button(
                keyboard_frame, text=key, width=5, font=font,
                command=lambda k=key: self.key_press(k)
            )
            row, col = divmod(index, 10)

            # Check if the key is "BORRAR" and apply columnspan and width
            if key == 'BORRAR':
                button.grid(row=row, column=col, columnspan=2,
                            sticky="we", padx=2, pady=2)
                button.config(width=10)  # Adjust the width as needed
            else:
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

    def verificar_operador(self, usuario, contraseña):
        conn = sqlite3.connect('operadores.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operadores WHERE username = ? \
                       AND password = ?", (usuario, contraseña))
        # Si se encuentra un resultado, se devolverá una fila
        operador = cursor.fetchone()
        conn.close()

        if operador:  # Si se encontró un operador
            return operador  # Devuelve los datos del operador
        return None

    def login(self):

        usuario = self.username.get()
        contraseña = self.password.get()
        operador = self.verificar_operador(usuario, contraseña)

        # Una vez se use solo el login con el API se debe quitar este IF
        # y dejar solo el de operador.
        if self.verificarLogin(self, usuario, contraseña):
            print(f"Usuario: {usuario}")
            print(f"Contraseña: {contraseña}")

            if operador:
                # Si la verificación es exitosa, enviar los datos
                # del operador a la API
                data = {
                    "operator_id": operador[0],
                    "name": operador[1],
                    "phone": operador[2],
                    "email": operador[3]
                }
                try:
                    response = requests.post(
                        "https://realtime.bucr.digital/api/operator",
                        json=data)
                    print(response.status_code)
                    if response.status_code == 200:
                        print("Datos enviados exitosamente a la API.")
                    else:
                        print(f"Error al enviar \
                              datos: {response.status_code} - {response.text}")
                except requests.RequestException as e:
                    print(f"Excepción al enviar datos a la API: {e}")

            # Ocultar el marco de inicio de sesión y mostrar el marco del viaje
            self.login_frame.pack_forget()
            self.trip_frame.pack(expand=True, fill='both')

            # Ocultar el teclado después del inicio de sesión
            self.keyboard_frame.pack_forget()
        else:
            print("Error: Usuario o contraseña incorrectos.")

    def logout(self):
        # Ocultar el marco del viaje y mostrar el marco de inicio de sesión
        self.trip_frame.pack_forget()
        self.login_frame.pack(expand=True, fill='both')
        self.keyboard_frame.pack(expand=True, fill='both')

    def show_registration(self):
        self.withdraw()
        # Pass the main window as an argument
        registration_app = InterfazRegistro(self)
        registration_app.protocol("WM_DELETE_WINDOW", self.on_closing)
        registration_app.mainloop()

    def return_to_main(self):
        self.deiconify()

    def start_gps(self):
        self.botonFinalizar.config(bg="gray")
        self.botonIniciar.config(bg="green")
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
        self.botonFinalizar.config(bg="red")
        self.botonIniciar.config(bg="gray")
        if self.gps_thread and self.gps_thread.is_alive():
            # Señalar al hilo que se detenga
            self.stop_event.set()
            self.gps_thread.join()  # Esperar a que el hilo termine
            # Actualizar el mensaje de estado
            self.status_message.set("Lectura de GPS finalizada.")
            print("Lectura de GPS finalizada.")
        else:
            self.status_message.set("La lectura de GPS no está en ejecución.")
            print("La lectura de GPS no está en ejecución.")

    def on_closing(self):
        # Asegurarse de que el hilo de GPS se detenga antes de cerrar
        self.stop_gps()
        self.destroy()


if __name__ == "__main__":
    app = InterfazMain()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
