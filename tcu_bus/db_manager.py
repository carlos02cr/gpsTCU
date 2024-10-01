import sqlite3
import bcrypt

def conectar_db():
    return sqlite3.connect('base_de_datos.db')

def crear_tabla(conn):
    cursor = conn.cursor()
    # Cambia la estructura de la tabla para incluir los nuevos campos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS operadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cedula TEXT NOT NULL UNIQUE,
        telefono TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        contrasena BLOB NOT NULL
    )
    ''')
    conn.commit()

def insertar_operador(conn, usuario, telefono, nombre, contrasena):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO operadores (usuario, telefono, nombre, contrasena)
    VALUES (?, ?, ?, ?)
    ''', (usuario, telefono, nombre, contrasena))
    conn.commit()

def verificar_operador(conn, usuario, contrasena):
    cursor = conn.cursor()
    cursor.execute('''
    SELECT contrasena FROM operadores WHERE usuario = ?
    ''', (usuario,))
    row = cursor.fetchone()
    if row:
        # Verificar la contraseña
        contrasena_hash = row[0]
        return bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_hash)
    return False

