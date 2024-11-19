import tkinter as tk
import sqlite3
import re
# import bcrypt

font = ("Helvetica", 12)


class funcRegistro:
    def __init__(self):
        pass

    def create_database(self):
        # Conectar a la base de datos (se crea si no existe)
        conn = sqlite3.connect("operadores.db")
        cursor = conn.cursor()
        # Crear tabla si no existe
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

    def verificarLogin(self, interface, nombre, password):
        # create_database()
        con = sqlite3.connect("operadores.db")
        cursor = con.cursor()
        cursor.execute("SELECT password FROM operadores" +
                       f" WHERE username = '{nombre}'")
        resultado = cursor.fetchone()
        if resultado:
            # hashed_password = resultado[0]
            # bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            if password == resultado[0]:
                interface.status_message.set("Usuario y contraseña correctos.")
                print("Usuario y contraseña correctos.")
                return True
            else:
                interface.status_login.set("Contraseña incorrecta.")
                print("Contraseña incorrecta.")
                return False
        else:
            interface.status_login.set("Usuario no encontrado.")
            print("Usuario no encontrado.")
            return False

    def verificarRegistro(self, operator_id, name,
                          phone, email, username, password):

        if not re.match("^[0-9]{1,8}$", operator_id):
            raise ValueError("ID inválido, debe ser "
                             "numérico.")

        if not re.match("^[0-9]{8}$", phone):
            raise ValueError("Número de teléfono inválido,"
                             " deben ser 8 números.")

        email_pattern = re.compile(
            r"^[a-zA-Z0-9_.+-]+@"      # Parte local del email
            r"[a-zA-Z0-9-]+\."         # Nombre del dominio
            r"[a-zA-Z0-9-.]+$"         # Extensión
        )

        if not re.match(email_pattern, email):
            raise ValueError("Correo electrónico inválido.")

        if not re.match("^[a-zA-Z0-9]{1,10}$", username):
            raise ValueError("Username inválido debe ser "
                             "menos de 10 letras o números.")

        if not re.match("^[a-zA-Z0-9]{1,10}$", username):
            raise ValueError("Username inválido debe ser "
                             "menos de 10 letras o números.")

        if not re.match("^[a-zA-Z\\s]{1,20}$", name):
            raise ValueError("Nombre inválido debe ser "
                             "letras o espacios y menos de 20 caracteres.")

        if not re.match("^[a-zA-Z0-9]{4,20}$", password):
            raise ValueError("Contraseña incorrecta, debe contener solo "
                             " letras y números y tener al menos 4 de estos.")


class InterfazRegistro(tk.Toplevel, funcRegistro):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app  # Store the reference to the main window

        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda event:
                  self.attributes("-fullscreen", False))

        self.title("Registro de Operadores")
        # Ajustar a las dimensiones de la pantalla táctil
        self.geometry("800x480")

        # Variables para los campos de entrada
        self.operator_id = tk.StringVar()
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.message = tk.StringVar()  # Variable para el mensaje de registro

        # Crear widgets de la interfaz
        self.create_widgets()
        self.keyboard_frame = None  # Inicializar el teclado

    def create_widgets(self):
        # Hace que las columnas se expandan
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        # Usar grid para colocar los campos en 3 columnas y 2 filas
        tk.Label(self, text="ID del Operador:", font=font).grid(
            row=0, column=0, padx=5, pady=7)
        tk.Entry(self, textvariable=self.operator_id, font=font).grid(
            row=0, column=1, padx=5, pady=7)

        tk.Label(self, text="Nombre y Apellido:", font=font).grid(
            row=0, column=2, padx=5, pady=7)
        tk.Entry(self, textvariable=self.name, font=font).grid(
            row=0, column=3, padx=5, pady=7)

        tk.Label(self, text="Teléfono:", font=font).grid(
            row=1, column=0, padx=5, pady=7)
        tk.Entry(self, textvariable=self.phone, font=font).grid(
            row=1, column=1, padx=5, pady=7)

        tk.Label(self, text="Email:", font=font).grid(
            row=1, column=2, padx=5, pady=7)
        tk.Entry(self, textvariable=self.email, font=font).grid(
            row=1, column=3, padx=5, pady=7)

        tk.Label(self, text="Nombre de usuario:", font=font).grid(
            row=2, column=0, padx=5, pady=7)
        tk.Entry(self, textvariable=self.username, font=font).grid(
            row=2, column=1, padx=5, pady=7)

        tk.Label(self, text="Contraseña:", font=font).grid(
            row=2, column=2, padx=5, pady=7)
        tk.Entry(self, textvariable=self.password, font=font,
                 show="*").grid(row=2, column=3, padx=5, pady=7)

        tk.Button(self, text="Registrar", command=self.register,
                  font=font).grid(row=3, column=1, columnspan=1, pady=10)

        tk.Button(self, text="Volver", command=self.volver,
                  font=font).grid(row=3, column=2, columnspan=1, pady=10)

        self.create_keyboard()

        # Label para mostrar el mensaje de registro
        self.success_label = tk.Label(
            self, textvariable=self.message, fg="green")
        self.success_label.grid(row=4, column=0, columnspan=4)

    def create_keyboard(self):
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR']

        self.keyboard_frame = tk.Frame(self)
        # Posiciona el teclado debajo de los campos
        self.keyboard_frame.grid(row=5, column=0, columnspan=4, pady=20)

        for key in keys:
            button = tk.Button(self.keyboard_frame, text=key,
                               width=5, font=font,
                               command=lambda k=key: self.key_press(k))
            row, col = divmod(keys.index(key), 10)

            if key == 'BORRAR':
                button.grid(row=row, column=col, columnspan=2, sticky="we")
                button.config(width=10)  # Adjust the width as needed
            else:
                button.grid(row=row, column=col)

    def key_press(self, key):
        focused_widget = self.focus_get()
        if isinstance(focused_widget, tk.Entry):
            if key == "BORRAR":
                current_text = focused_widget.get()
                focused_widget.delete(0, tk.END)
                focused_widget.insert(0, current_text[:-1])
            else:
                focused_widget.insert(tk.END, key)

    def register(self):
        # Obtener los datos de los campos
        operator_id = self.operator_id.get()
        name = self.name.get()
        phone = self.phone.get()
        email = self.email.get()
        username = self.username.get()
        password = self.password.get()

        # Guardar en la base de datos
        conn = sqlite3.connect("operadores.db")
        cursor = conn.cursor()
        try:
            self.verificarRegistro(operator_id, name, phone,
                                   email, username, password)
            cursor.execute('''
                INSERT INTO operadores (operator_id, name, \
                           phone, email, username, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (operator_id, name, phone, email, username, password))
            conn.commit()
            self.message.set("Registro exitoso.")  # Actualizar el mensaje

            # Limpiar campos después del registro
            self.operator_id.set("")
            self.name.set("")
            self.phone.set("")
            self.email.set("")
            self.username.set("")
            self.password.set("")

        except sqlite3.IntegrityError:
            # Mensaje de error
            self.message.set("Error: ID del operador ya existe.")

        # Mensaje de error cuando los datos a registrar no son apropiados.
        except ValueError as e:
            self.message.set(str(e))

        finally:
            conn.close()

    def volver(self):
        self.destroy()  # Close the registration window
        self.main_app.return_to_main()


if __name__ == "__main__":
    pass
