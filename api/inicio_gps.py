import serial
import json

# Configuración puerto serial
port = '/dev/serial0'  # Se define puerto
baudrate = 9600        # Frecuencia/velocidad de trabajo
output_file = 'gps_data.json'  # Archivo JSON donde se guardarán los datos

ser = serial.Serial(port, baudrate, timeout=10)  # Se abre puerto serial

try:
    print(f"Guardando datos en {output_file}. Presione CTRL+C para salir.")
    while True:
        line = ser.readline().decode('ascii', errors='replace').strip()  # Lee datos del puerto serial
        if line.startswith('$GPRMC'):  # Verifica si la línea comienza con $GPRMC
            print(line)  # Muestra los datos en la consola
            json_data = {"gps_data": line}  # Estructura los datos en un diccionario para JSON
            
            # Abre el archivo en modo 'w' para sobrescribir con la nueva línea
            with open(output_file, 'w') as file:
                json.dump(json_data, file)  # Escribe los datos en formato JSON en el archivo

except KeyboardInterrupt:
    print("\nPrograma interrumpido. Cerrando...")
finally:
    ser.close()
