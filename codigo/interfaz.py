import tkinter as tk
from tkinter import ttk
import pexpect
import serial
import subprocess
from funcionesGPS import manejarGPS


class VirtualKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INICIO DE SESION")
        self.geometry("800x480")  # Ajustar a las dimensiones de la pantalla táctil

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):

        # Se crea un frame para el inicio de sesión
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(expand=True, fill='both')

        tk.Label(self.login_frame, text="USUARIO:").pack(pady=10)
        tk.Entry(self.login_frame, textvariable=self.username).pack(pady=10)

        tk.Label(self.login_frame, text="CONTRASEÑA:").pack(pady=10)
        tk.Entry(self.login_frame, textvariable=self.password, show="*").pack(pady=10)
        # Se crea el teclado y se almacena en self.keyboard_frame
        self.keyboard_frame = tk.Frame(self.login_frame)
        self.keyboard_frame.pack(pady=10)

        self.create_keyboard()

        tk.Button(self.login_frame, text="INICIAR", command=self.send_data).pack(pady=0.1)

        # Se crea un frame para la sección de viaje(inicialmente oculto)
        self.trip_frame = tk.Frame(self)

        tk.Button(self.trip_frame, text="Iniciar Viaje", command=self.read_gps).pack(pady=20)
        tk.Button(self.trip_frame, text="Finalizar Viaje", command=self.stop_gps).pack(pady=20)

    def create_keyboard(self):
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR'        ]

        keyboard_frame = tk.Frame(self)
        keyboard_frame.pack(pady=20)

        for key in keys:
             button = tk.Button(keyboard_frame, text=key, width=6, command=lambda k=key: self.key_press(k))
             row, col = divmod(keys.index(key), 10)
             button.grid(row=row, column=col)

    def key_press(self, key):
        if key == "BORRAR":
            current_text = self.focus_get().get()
            self.focus_get().delete(0, tk.END)
            self.focus_get().insert(0, current_text[:-1])
        elif key == "ESPACIO":
            self.focus_get().insert(tk.END, ' ')
        else:
            if self.focus_get():
                self.focus_get().insert(tk.END, key)

    def send_data(self):
        print(f"Usuario: {self.username.get()}")
        print(f"Contraseña: {self.password.get()}")

        # Se oculta el frame de inicio de sesión y se muestra el de viaje
        self.login_frame.pack_forget()    # Oculta el frame de inicio de sesión
        # Muestra el frame de viaje
        self.trip_frame.pack(expand=True, fill='both')

        # Se oculta el teclado después de iniciar sesión
        self.keyboard_frame.pack_forget()
        self.login_frame.update()

    def read_gps(self):
        # Se inicia la lectura de datos del GPS
        # self.gps_process = pexpect.spawn('sudo minicom -b 9600 -o -D /dev/serial0')
        manejarGPS()

    def stop_gps(self):
        # Implementar el comando para finalizar la lectura del GPS
        manejarGPS(flagDetener=True)
        print("Lectura de GPS finalizada")


if __name__ == "__main__":
    start = VirtualKeyboard()
    start.mainloop()
