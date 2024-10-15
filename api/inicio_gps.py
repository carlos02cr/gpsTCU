import serial
import json

# Configuración puerto serial
port = '/dev/serial0'               # Se define puerto
baudrate = 9600                     # Frecuencia/velocidad de trabajo
json_output_file = 'gps_data.json'  # Archivo JSON donde se sobrescriben los datos
txt_output_file = 'gps_data.txt'    # Archivo de texto donde se guardarán los datos con append

ser = serial.Serial(port, baudrate, timeout=10)  # Se abre puerto serial

try:
    print(f"Guardando datos en {json_output_file} y {txt_output_file}. Presione CTRL+C para salir.")
    while True:
        line = ser.readline().decode('ascii', errors='replace').strip() # Lee datos del puerto serial
        if line.startswith('$GPRMC'):                                   # Verifica si la línea comienza con $GPRMC
            print(line)                                                 # Muestra los datos en la consola
            json_data = {"gps_data": line}                              # Estructura los datos en un diccionario para JSON
            
            # Guardar en archivo JSON (sobrescribiendo)
            with open(json_output_file, 'w') as json_file:
                json.dump(json_data, json_file)                         # Escribe los datos en formato JSON en el archivo

            # Guardar en archivo de texto (append)
            with open(txt_output_file, 'a') as txt_file:
                txt_file.write(line + '\n')                             # Guarda la línea en el archivo de texto

except KeyboardInterrupt:
    print("\nPrograma interrumpido. Cerrando...")
finally:
    ser.close()
