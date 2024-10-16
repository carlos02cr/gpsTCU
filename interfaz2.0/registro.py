import tkinter as tk
import sqlite3

class RegistrationApp(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Registro de Operadores")
        self.geometry("800x480")  # Dimensiones ajustadas a la pantalla de la Raspberry Pi

        # Variables para campos de entrada
        self.operator_id = tk.StringVar()
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.register_username = tk.StringVar()
        self.register_password = tk.StringVar()
        self.registration_message = tk.StringVar()  # Mensaje de confirmación

        # Crear la base de datos y la tabla si no existen
        self.create_database()

        # Crear el diseño de los campos de entrada y el teclado
        self.create_widgets()

    def create_database(self):
        """
        Crea la base de datos y la tabla de operadores si no existen.
        """
        conn = sqlite3.connect("operadores.db")
        cursor = conn.cursor()
        # Crear la tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operadores (
                operator_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        # Crear un contenedor para los campos de registro y teclado
        container_frame = tk.Frame(self)
        container_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Crear dos columnas para los campos de entrada
        left_frame = tk.Frame(container_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="n")

        right_frame = tk.Frame(container_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=5, sticky="n")

        # Campos de la izquierda (ID, Nombre, Teléfono)
        tk.Label(left_frame, text="ID Operador:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=3, sticky='e')
        tk.Entry(left_frame, textvariable=self.operator_id, font=("Arial", 12), width=20).grid(row=0, column=1, padx=5, pady=3)

        tk.Label(left_frame, text="Nombre:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=3, sticky='e')
        tk.Entry(left_frame, textvariable=self.name, font=("Arial", 12), width=20).grid(row=1, column=1, padx=5, pady=3)

        tk.Label(left_frame, text="Teléfono:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=3, sticky='e')
        tk.Entry(left_frame, textvariable=self.phone, font=("Arial", 12), width=20).grid(row=2, column=1, padx=5, pady=3)

        # Campos de la derecha (Email, Usuario, Contraseña)
        tk.Label(right_frame, text="Email:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=3, sticky='e')
        tk.Entry(right_frame, textvariable=self.email, font=("Arial", 12), width=20).grid(row=0, column=1, padx=5, pady=3)

        tk.Label(right_frame, text="Usuario:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=3, sticky='e')
        tk.Entry(right_frame, textvariable=self.register_username, font=("Arial", 12), width=20).grid(row=1, column=1, padx=5, pady=3)

        tk.Label(right_frame, text="Contraseña:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=3, sticky='e')
        tk.Entry(right_frame, textvariable=self.register_password, show="*", font=("Arial", 12), width=20).grid(row=2, column=1, padx=5, pady=3)

        # Botones de acción centrados bajo los campos
        tk.Button(container_frame, text="Registrar", command=self.register_user, font=("Arial", 12), width=15).grid(row=1, column=0, columnspan=2, pady=2)
        tk.Button(container_frame, text="Volver al Login", command=self.close_window, font=("Arial", 12), width=15).grid(row=2, column=0, columnspan=2, pady=2)

        # Mensaje de confirmación
        self.success_label = tk.Label(container_frame, textvariable=self.registration_message, fg="green", font=("Arial", 12))
        self.success_label.grid(row=3, column=0, columnspan=2, pady=2)

        # Crear teclado virtual más compacto y centrado
        self.keyboard_frame = tk.Frame(container_frame)
        self.keyboard_frame.grid(row=4, column=0, columnspan=2, pady=5)

        self.create_keyboard()

    def create_keyboard(self):
        # Teclas dispuestas como un teclado convencional
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

    def register_user(self):
        # Verifica que los campos no estén vacíos antes de registrar
        if not all([self.operator_id.get(), self.name.get(), self.phone.get(), self.email.get(), self.register_username.get(), self.register_password.get()]):
            self.registration_message.set("Error: Todos los campos son obligatorios.")
            return

        conn = sqlite3.connect("operadores.db")
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO operadores (operator_id, name, phone, email, username, password) 
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (self.operator_id.get(), self.name.get(), self.phone.get(),
                            self.email.get(), self.register_username.get(), self.register_password.get()))
            conn.commit()
            self.registration_message.set("¡Registro exitoso!")
        except sqlite3.IntegrityError:
            self.registration_message.set("Error: ID del operador ya existe.")
        finally:
            conn.close()

    def close_window(self):
        self.destroy()
        self.master.return_to_main()
