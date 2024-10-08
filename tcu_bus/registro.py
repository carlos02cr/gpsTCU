import tkinter as tk
import sqlite3

class RegistrationFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Reference to the main application

        # Create the database and table if they don't exist
        self.create_database()

        # Variables for input fields
        self.operator_id = tk.StringVar()
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.message = tk.StringVar()  # Variable for registration messages

        # Create widgets for the registration frame
        self.create_widgets()

    def create_database(self):
        # Connect to the database (creates it if it doesn't exist)
        conn = sqlite3.connect("operadores.db")
        cursor = conn.cursor()
        # Create the table if it doesn't exist
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
        # Configure grid columns for proper alignment
        for i in range(2):  # Assuming 2 columns: labels and entries
            self.grid_columnconfigure(i, weight=1, pad=10)

        # Labels and Entry widgets
        tk.Label(self, text="ID del Operador:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self, textvariable=self.operator_id).grid(row=0, column=1, padx=5, pady=5, sticky='we')

        tk.Label(self, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self, textvariable=self.name).grid(row=1, column=1, padx=5, pady=5, sticky='we')

        tk.Label(self, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self, textvariable=self.phone).grid(row=2, column=1, padx=5, pady=5, sticky='we')

        tk.Label(self, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self, textvariable=self.email).grid(row=3, column=1, padx=5, pady=5, sticky='we')

        tk.Label(self, text="Usuario:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self, textvariable=self.username).grid(row=4, column=1, padx=5, pady=5, sticky='we')

        tk.Label(self, text="Contraseña:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self, textvariable=self.password, show="*").grid(row=5, column=1, padx=5, pady=5, sticky='we')

        # Register and Back buttons
        tk.Button(self, text="Registrar", command=self.register).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Volver", command=self.volver).grid(row=7, column=0, columnspan=2, pady=5)

        # Create the keyboard within the registration frame
        self.create_keyboard()

        # Label to display registration messages
        self.success_label = tk.Label(self, textvariable=self.message, fg="green")
        self.success_label.grid(row=8, column=0, columnspan=2, pady=10)

    def create_keyboard(self):
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR'
        ]

        keyboard_frame = tk.Frame(self)
        keyboard_frame.grid(row=9, column=0, columnspan=2, pady=20)

        for index, key in enumerate(keys):
            button = tk.Button(keyboard_frame, text=key, width=5,
                               command=lambda k=key: self.key_press(k))
            row, col = divmod(index, 10)
            button.grid(row=row, column=col, padx=2, pady=2)

    def key_press(self, key):
        focused_widget = self.focus_get()
        if key == "BORRAR" and focused_widget:
            current_text = focused_widget.get()
            focused_widget.delete(0, tk.END)
            focused_widget.insert(0, current_text[:-1])
        else:
            if focused_widget and isinstance(focused_widget, tk.Entry):
                focused_widget.insert(tk.END, key)

    def register(self):
        # Retrieve data from input fields
        operator_id = self.operator_id.get()
        name = self.name.get()
        phone = self.phone.get()
        email = self.email.get()
        username = self.username.get()
        password = self.password.get()

        # Save to the database
        conn = sqlite3.connect("operadores.db")
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO operadores (operator_id, name, phone, email, username, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (operator_id, name, phone, email, username, password))
            conn.commit()
            self.message.set("Registro exitoso.")  # Update the message
        except sqlite3.IntegrityError:
            # Error message if operator_id already exists
            self.message.set("Error: ID del operador ya existe.")
        finally:
            conn.close()

        # Clear input fields after registration
        self.operator_id.set("")
        self.name.set("")
        self.phone.set("")
        self.email.set("")
        self.username.set("")
        self.password.set("")

    def volver(self):
        self.parent.return_to_main()

