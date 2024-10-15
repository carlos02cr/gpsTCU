import serial
import requests
import csv

# Configuración puerto serial
port = '/dev/serial0'               # Se define puerto
baudrate = 9600                     # Frecuencia/velocidad de trabajo
archivo_txt = 'gps_data.txt'    # Archivo de texto donde se guardarán los datos con append
archivo_csv = 'datos_gps.csv'
api_url = 'https://realtime.bucr.digital/api/position'

ser = serial.Serial(port, baudrate, timeout=10)             # Se abre puerto serial
save_count = 1                                              # Contador de guardados

def guardar_csv(nombre_archivo, latitud, longitud):
    with open(nombre_archivo, mode='a', newline='') as archivo_csv: # Modo 'a' para agregar datos sin sobrescribir
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([latitud, longitud])                  # Escribir la fila con latitud y longitud
        
def guardar_txt(nombre_archivo, latitud, longitud, save_count):
    with open(nombre_archivo, 'a') as txt_file:                     # Modo 'a' para agregar datos sin sobrescribir
        txt_file.write(f"{save_count}: Latitud: {latitud}, Longitud: {longitud}\n")

def conversion_latxlon(latitud, latitud_dir, longitud, longitud_dir):
    # Conversión de latitud (dos primeros dígitos son los grados)
    lat_grados = int(latitud[:2])                           # Los primeros 2 caracteres son los grados para latitud
    lat_minutos = float(latitud[2:])                        # Los minutos incluyen los decimales
    lat_decimal = lat_grados + (lat_minutos / 60)           # Convertir latitud a grados decimales
    if latitud_dir == 'S':
        lat_decimal = -lat_decimal                          # Ajustar si está en el hemisferio sur

    # Conversión de longitud (tres primeros dígitos son los grados)
    lon_grados = int(longitud[:3])                          # Los primeros 3 caracteres son los grados para longitud
    lon_minutos = float(longitud[3:])                       # Los minutos incluyen los decimales
    lon_decimal = lon_grados + (lon_minutos / 60)           # Convertir longitud a grados decimales
    if longitud_dir == 'W':
        lon_decimal = -lon_decimal                          # Ajustar si está en el hemisferio oeste
        
    return lat_decimal, lon_decimal
    
def enviar_api(latitud_decimal, longitud_decimal):
    """
    Recibe la latitud y longitud en grados decimales y envía los datos a la API.
    """
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
            print(f"Datos enviados correctamente a la API. Latitud: {latitud_decimal}, Longitud: {longitud_decimal}")
        else:
            print(f"Error al enviar los datos a la API. Código de estado: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al intentar enviar los datos: {e}")
    
try:
    print(f"Guardando datos en {archivo_csv} y {archivo_txt}. Presione CTRL+C para salir.")
    while True:
        line = ser.readline().decode('ascii', errors='replace').strip()                         # Lee datos del puerto serial
        if line.startswith('$GPRMC'):                                                           # Verifica si la línea comienza con $GPRMC
            lista = line.split(',')                                                             # Genera una lista de 13 elementos 
            if len(lista) > 2:                                                                  # Si la lista contiene mas de 2 elementos
                    if lista[2] == 'A':                                                         # Si el elemento 3 es A (dato valido)
                        latxlon = lista[3:7]                                                    # Guardar elementos 4 al 8 [latitud,latitud_dir,longitud,longitud_dir]
                        latitud,longitud = conversion_latxlon(latxlon[0], latxlon[1], latxlon[2],latxlon[3])
                        print(f"Linea completa: {line}\Latitud: {latitud}\nLongitud: {longitud}")
                        
                        with open(archivo_txt, 'a') as txt_file:
                            txt_file.write(f"{save_count}: Latitud: {latitud}, Longitud: {longitud} \n")                        # Guarda la línea en el archivo de texto
                        
                        guardar_csv(archivo_csv, latitud, longitud)
                        guardar_txt(archivo_txt, latitud, longitud, save_count)
                        save_count += 1                                                         # Incrementa el contador de guardados
                        
                    elif lista[2] == 'V':
                        print(f"Linea completa: {line}\nLista: None\nLínea inválida (V)")
                
except KeyboardInterrupt:
    print("\nPrograma interrumpido. Cerrando...")
finally:
    ser.close()
