import sqlite3
import bcrypt

# Conectar o crear la base de datos
def conectar_db():
    conn = sqlite3.connect('operadores.db')
    return conn

# Crear la tabla de operadores si no existe
def crear_tabla(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS operadores (
                        operador_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL
                      )''')
    conn.commit()

# Función para insertar datos en la tabla con contraseña cifrada
def insertar_operador(conn, nombre, phone, email, password):
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO operadores (nombre, phone, email, password) VALUES (?, ?, ?, ?)", 
                   (nombre, phone, email, hashed_password))
    conn.commit()
    print("Datos insertados correctamente.")

# Función para verificar usuario y contraseña
def verificar_operador(conn, nombre, password):
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM operadores WHERE nombre=?", (nombre,))
    resultado = cursor.fetchone()
    if resultado:
        hashed_password = resultado[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            print("Usuario y contraseña correctos.")
            return True
        else:
            print("Contraseña incorrecta.")
            return False
    else:
        print("Usuario no encontrado.")
        return False
