import tkinter as tk
import sqlite3

class RegistrationApp(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Registro de Operadores")
        self.geometry("800x480")

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

        # Crear el diseño de los campos en dos columnas
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
        container_frame = tk.Frame(self)
        container_frame.pack(expand=True)

        left_frame = tk.Frame(container_frame)
        left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        right_frame = tk.Frame(container_frame)
        right_frame.grid(row=0, column=1, padx=20, pady=10, sticky="n")

        tk.Label(left_frame, text="ID Operador:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(left_frame, textvariable=self.operator_id).grid(row=0, column=1, padx=5, pady=5, sticky='we')

        tk.Label(left_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(left_frame, textvariable=self.name).grid(row=1, column=1, padx=5, pady=5, sticky='we')

        tk.Label(left_frame, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(left_frame, textvariable=self.phone).grid(row=2, column=1, padx=5, pady=5, sticky='we')

        tk.Label(right_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(right_frame, textvariable=self.email).grid(row=0, column=1, padx=5, pady=5, sticky='we')

        tk.Label(right_frame, text="Usuario:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(right_frame, textvariable=self.register_username).grid(row=1, column=1, padx=5, pady=5, sticky='we')

        tk.Label(right_frame, text="Contraseña:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(right_frame, textvariable=self.register_password, show="*").grid(row=2, column=1, padx=5, pady=5, sticky='we')

        tk.Button(container_frame, text="Registrar", command=self.register_user).grid(row=1, column=0, columnspan=2, pady=20)
        tk.Button(container_frame, text="Volver al Login", command=self.close_window).grid(row=2, column=0, columnspan=2, pady=10)

        self.success_label = tk.Label(self, textvariable=self.registration_message, fg="green")
        self.success_label.pack(pady=10)

        # Crear teclado virtual
        self.keyboard_frame = tk.Frame(self)
        self.keyboard_frame.pack(pady=20)
        self.create_keyboard()

    def create_keyboard(self):
        keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
                'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR', 'ESPACIO', '@', '.']

        keyboard_frame = tk.Frame(self.keyboard_frame)
        keyboard_frame.pack(pady=20)

        for index, key in enumerate(keys):
            if key == 'ESPACIO':
                button = tk.Button(keyboard_frame, text="Espacio", width=12, command=lambda k=' ': self.key_press(k))
            else:
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
