import serial
import requests
import csv
import os
import time

windows = False
if os.name == 'nt':
    windows = True


def guardar_csv(nombre_archivo, latitud, longitud):
    # Modo 'a' para agregar datos sin sobrescribir
    with open(nombre_archivo, mode='a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        # Escribir la fila con latitud y longitud
        escritor_csv.writerow([latitud, longitud])


def guardar_txt(nombre_archivo, latitud, longitud, save_count):
    # Modo 'a' para agregar datos sin sobrescribir
    with open(nombre_archivo, 'a') as txt_file:
        txt_file.write(
            f"{save_count}: Latitud: {latitud}, Longitud: {longitud}\n")


def conversion_latxlon(latitud, latitud_dir, longitud, longitud_dir):
    # Conversión de latitud (dos primeros dígitos son los grados)
    # Los primeros 2 caracteres son los grados para latitud
    lat_grados = int(latitud[:2])
    # Los minutos incluyen los decimales
    lat_minutos = float(latitud[2:])
    # Convertir latitud a grados decimales
    lat_decimal = lat_grados + (lat_minutos / 60)
    if latitud_dir == 'S':
        # Ajustar si está en el hemisferio sur
        lat_decimal = -lat_decimal

    # Conversión de longitud (tres primeros dígitos son los grados)
    # Los primeros 3 caracteres son los grados para longitud
    lon_grados = int(longitud[:3])
    # Los minutos incluyen los decimales
    lon_minutos = float(longitud[3:])
    # Convertir longitud a grados decimales
    lon_decimal = lon_grados + (lon_minutos / 60)
    if longitud_dir == 'W':
        # Ajustar si está en el hemisferio oeste
        lon_decimal = -lon_decimal

    return lat_decimal, lon_decimal


def enviar_api(latitud_decimal, longitud_decimal):
    # Datos que se enviarán a la API
    data = {
        "journey_id": 698453,
        "timestamp": 1710067980,
        "latitude": latitud_decimal,
        "longitude": longitud_decimal,
        "altitude": 1234.5,
        "speed": 12.5,
        "bearing": 135,
        "odometer": 12345.6
    }

    # URL de la API
    api_url = 'https://realtime.bucr.digital/api/position'

    try:
        # Enviar datos a la API
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            print(
                f"Datos enviados correctamente a la API. Latitud: "
                f"{latitud_decimal}, Longitud: {longitud_decimal}")
        else:
            print(
                f"Error al enviar los datos a la API. Código de estado:"
                f"{response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al intentar enviar los datos: {e}")


def manejarGPS(stop_event):
    # Configuración puerto serial
    port = '/dev/serial0'               # Se define puerto
    baudrate = 9600                     # Frecuencia/velocidad de trabajo
    # Archivo de texto donde se guardarán los datos con append
    archivo_txt = 'gps_data.txt'
    archivo_csv = 'datos_gps.csv'

    # Quitar el comentario para cuando se tenga el
    # api_url = 'https://realtime.bucr.digital/api/position'

    # Se abre puerto serial
    if not windows:
        ser = serial.Serial(port, baudrate, timeout=10)
    # Contador de guardados
    save_count = 1

    try:
        print(
            f"Guardando datos en {archivo_csv} y "
            f"{archivo_txt}. Presione CTRL+C para salir.")
        while not stop_event.is_set():
            if windows:
                print("Proceso corriendo...")
                time.sleep(0.5)
            else:
                line = ser.readline().decode('ascii', errors='replace').strip(
                )  # Lee datos del puerto serial
                # Verifica si la línea comienza con $GPRMC
                if line.startswith('$GPRMC'):
                    # Genera una lista de 13 elementos
                    lista = line.split(',')
                    # Si la lista contiene mas de 2 elementos
                    if len(lista) > 2:
                        # Si el elemento 3 es A (dato valido)
                        if lista[2] == 'A':
                            # Guardar elementos 4 al 8
                            # [latitud,latitud_dir,longitud,longitud_dir]
                            latxlon = lista[3:7]
                            latitud, longitud = conversion_latxlon(
                                latxlon[0], latxlon[1], latxlon[2], latxlon[3])
                            print(f"Latitud: {latitud} y Longitud: {longitud}")

                            with open(archivo_txt, 'a') as txt_file:
                                # Guarda la línea en el archivo de texto
                                txt_file.write(
                                    f"{save_count}: Latitud: {latitud},"
                                    f" Longitud: {longitud} \n")

                            guardar_csv(archivo_csv, latitud, longitud)
                            guardar_txt(archivo_txt, latitud, longitud,
                                        save_count)
                            # Incrementa el contador de guardados
                            save_count += 1

                        elif lista[2] == 'V':
                            print(
                                f"Linea completa: {line}\nLista:"
                                f" None\nLínea inválida (V)")

    except KeyboardInterrupt:
        print("\nPrograma interrumpido. Cerrando...")
    finally:
        if not windows:
            ser.close()
