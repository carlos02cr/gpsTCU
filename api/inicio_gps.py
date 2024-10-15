import serial
import json

# Configuración puerto serial
port = '/dev/serial0'  # Se define puerto
baudrate = 9600        # Frecuencia/velocidad de trabajo
output_file = 'gps_data.json'  # Archivo JSON donde se guardarán los datos

ser = serial.Serial(port, baudrate, timeout=10)  # Se abre puerto serial

try:
    with open(output_file, 'a') as file:  # Abre el archivo en modo 'append'
        print(f"Guardando datos en {output_file}. Presione CTRL+C para salir.")
        while True:
            line = ser.readline().decode('ascii', errors='replace').strip()  # Lee datos del puerto serial
            if line.startswith('$GPRMC'):  # Verifica si la línea comienza con $GPRMC
                print(line)  # Muestra los datos en la consola
                json_data = {"gps_data": line}  # Estructura los datos en un diccionario para JSON
                json.dump(json_data, file)  # Escribe los datos en formato JSON en el archivo
                file.write('\n')  # Añade una nueva línea después de cada entrada JSON
except KeyboardInterrupt:
    print("\nPrograma interrumpido. Cerrando...")
finally:
    ser.close()
